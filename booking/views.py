from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from .models import Staff, Booking
from .forms import StaffUpdateForm, StaffPasswordChangeForm
from django.core.mail import send_mail
from django.conf import settings
from datetime import datetime
from datetime import datetime, timedelta
from django.db import transaction
from django.utils import timezone
# from .zoom_service import create_zoom_meeting
from .tasks import send_zoom_reminder


def admin_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_staff:  # ✅ only admins allowed
                login(request, user)
                return redirect(reverse('admin:index'))  # go to admin panel
            else:
                messages.error(request, "Not an admin user.")
        else:
            messages.error(request, "Invalid credentials.")

    return render(request, "booking/admin_login.html")



# ------------------------
# Logout
# ------------------------
@login_required
def staff_logout(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('login')

# ------------------------
# Profile (Update + Password Change)
# ------------------------
@login_required
def staff_profile(request):
    user = request.user

    if request.method == "POST":
        if 'update_profile' in request.POST:
            form = StaffUpdateForm(request.POST, request.FILES, instance=user)
            pwd_form = StaffPasswordChangeForm(user=user)
            if form.is_valid():
                form.save()
                messages.success(request, "Profile updated successfully.")
                return redirect('staff_profile')
            else:
                messages.error(request, "Please fix the errors in your profile form.")

        elif 'change_password' in request.POST:
            form = StaffUpdateForm(instance=user)
            pwd_form = StaffPasswordChangeForm(user=user, data=request.POST)
            if pwd_form.is_valid():
                user = pwd_form.save()
                update_session_auth_hash(request, user)  # keep user logged in
                messages.success(request, "Password changed successfully.")
                return redirect('staff_profile')
            else:
                messages.error(request, "Please fix the errors in your password form.")
    else:
        form = StaffUpdateForm(instance=user)
        pwd_form = StaffPasswordChangeForm(user=user)

    return render(request, 'booking/staff_profile.html', {
        'form': form,
        'pwd_form': pwd_form,
        'user': user
    })


# ------------------------
# Staff Login (fixed)
# ------------------------
def staff_login(request):
    if request.method == "POST":
        staff_id = request.POST.get('staff_id')  
        username = request.POST.get('username')
        password = request.POST.get('password')

        # authenticate user using username + password
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # check staff_id matches
            if hasattr(user, 'staff_id') and str(user.staff_id) == str(staff_id):
                login(request, user)  
                messages.success(request, f"Welcome {user.first_name}, you are logged in.")
                return redirect('staff_dashboard') 
            else:
                messages.error(request, "Invalid Staff ID")
        else:
            messages.error(request, "Invalid username or password")

    # GET request or failed POST
    return render(request, 'booking/login.html')



@login_required
def enter_zoom_link(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    if request.method == "POST":
        zoom_link = request.POST.get("zoom_link")
        if zoom_link:
            booking.zoom_link = zoom_link
            booking.status = "Accepted"
            booking.reminder_sent = False  # reset reminder for this booking
            booking.save()
            messages.success(request, "Zoom link saved and booking accepted!")

            # Email patient
            send_mail(
                subject="Your Appointment Zoom Link",
                message=(
                    f"Dear {booking.patient_name},\n\n"
                    f"Your appointment with {booking.staff.full_name_with_prefix} is confirmed.\n"
                    f"📅 Date: {booking.day}\n"
                    f"⏰ Time: {booking.time}\n"
                    f"🔗 Zoom Link: {booking.zoom_link}\n\n"
                    f"Best regards,\nClinic Team"
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[booking.patient_email],
            )

            # Email staff
            send_mail(
                subject="Zoom Link Entered for Appointment",
                message=(
                    f"Dear {booking.staff.first_name},\n\n"
                    f"You entered a Zoom link for the appointment with {booking.patient_name}.\n"
                    f"Zoom Link: {booking.zoom_link}"
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[booking.staff.email],
            )
            
            appointment_dt = timezone.make_aware(
                datetime.combine(booking.day, booking.time),
                timezone.get_current_timezone()
            )
            reminder_time = appointment_dt - timedelta(minutes=15)

            send_zoom_reminder.apply_async(
                args=[booking.id],
                eta=reminder_time
            )

        else:
            messages.error(request, "Please enter a valid Zoom link.")

    return redirect("staff_dashboard")


@login_required
def accept_booking_manual(request, booking_id):
    """
    Marks the booking as Accepted and opens a place to enter Zoom link.
    """
    booking = get_object_or_404(Booking, id=booking_id)

    # Only pending bookings can be accepted
    if booking.status != "Pending":
        messages.error(request, "This booking is already processed.")
        return redirect("staff_dashboard")

    booking.status = "Accepted"
    booking.save()
    messages.success(request, "Booking accepted. Please enter the Zoom link below.")

    return redirect("staff_dashboard")

# @login_required
# def accept_booking(request, booking_id):
#     booking = get_object_or_404(Booking, id=booking_id)

#     if booking.status != "Accepted":

#         meeting = create_zoom_meeting(booking)

#     if meeting["join_url"]:
#         booking.status = "Accepted"
#         booking.zoom_link = meeting["join_url"]
#         booking.zoom_meeting_id = meeting["id"]
#         booking.save()

#         try:
#             # Create Zoom meeting
#             meeting = create_zoom_meeting(booking)
#             zoom_link = meeting.get("join_url")
#             zoom_id = meeting.get("id")

#             if not zoom_link:
#                 raise Exception(f"Zoom meeting not created. Response: {meeting}")

#             booking.zoom_link = zoom_link
#             booking.zoom_meeting_id = zoom_id
#             booking.save()

#             appointment_datetime = timezone.make_aware(
#                 datetime.combine(booking.day, booking.time),
#                 timezone.get_current_timezone()
#             )

#             send_zoom_reminders.apply_async(
#                 eta=appointment_datetime - timedelta(minutes=30)
#             )

#         except Exception as e:
#             messages.error(request, f"Zoom meeting creation failed: {e}")
#             # You can still notify doctor/patient manually if you want
#             return redirect("staff_dashboard")

#         # Email patient
#         send_mail(
#             subject="Your Zoom Appointment Link",
#             message=(f"Dear {booking.patient_name},\n\n"
#                      f"Your appointment has been accepted.\n"
#                      f"📅 Date: {booking.day}\n"
#                      f"⏰ Time: {booking.time}\n"
#                      f"🔗 Zoom Link: {booking.zoom_link}\n\n"
#                      f"Best regards,\nClinic Team"),
#             from_email=settings.DEFAULT_FROM_EMAIL,
#             recipient_list=[booking.patient_email],
#         )

#         # Email doctor
#         send_mail(
#             subject="Appointment Accepted",
#             message=(f"You accepted the appointment with {booking.patient_name}.\n\n"
#                      f"Zoom Link: {booking.zoom_link}"),
#             from_email=settings.DEFAULT_FROM_EMAIL,
#             recipient_list=[booking.staff.email],
#         )

#     return redirect("staff_dashboard")

def cancel_booking(request, booking_id):
    if request.method == "POST":
        reason = request.POST.get("cancel_reason")
        booking = get_object_or_404(Booking, id=booking_id)

        # Update booking status
        booking.status = "Rejected"
        booking.notes = f"Cancelled: {reason}"
        booking.save()

        # Email to patient
        send_mail(
            subject="Your Appointment Has Been Cancelled",
            message=f"Dear {booking.patient_name},\n\nYour appointment on {booking.day} at {booking.time} has been cancelled.\nReason: {reason}\n\nBest regards,\nClinic Team",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[booking.patient_email],
        )

        # Email to staff (doctor)
        staff_email = booking.staff.email
        send_mail(
            subject="Booking Cancellation Confirmation",
            message=f"Dear {booking.staff.first_name},\n\nYou cancelled the appointment with {booking.patient_name} ({booking.patient_email}).\nReason: {reason}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[staff_email],
        )

    return redirect("staff_dashboard")  # adjust to your dashboard view name



def submit_appointment(request, staff_id):
    staff = get_object_or_404(Staff, id=staff_id)

    if request.method != 'POST':
        return redirect('staff_detail', id=staff_id)

    # Normalize types
    day = datetime.strptime(request.POST['date'], "%Y-%m-%d").date()
    time = datetime.strptime(request.POST['time'], "%H:%M").time()


    patient_name = request.POST['name']
    patient_email = request.POST['email']
    notes = request.POST.get('reason', '')

    try:
        with transaction.atomic():
            exists = Booking.objects.select_for_update().filter(
                staff=staff,
                day=day,
                time=time
            ).exclude(status='Rejected').exists()

            if exists:
                messages.error(request, "This time slot is already booked. Please choose another time.")
                return redirect('appointment_page', staff_id=staff_id)

            booking = Booking.objects.create(
                staff=staff,
                patient_name=patient_name,
                patient_email=patient_email,
                notes=notes,
                day=day,
                time=time
            )

    except Exception:
        messages.error(request, "An error occurred while booking. Please try again.")
        return redirect('staff_detail', staff_id=staff_id)

    # Notify staff
    send_mail(
        subject="New Appointment Scheduled",
        message=f"Dear {staff.first_name},\n\n"
                f"You have a new appointment:\n"
                f"Patient: {booking.patient_name}\n"
                f"Date: {booking.day}\n"
                f"Time: {booking.time}\n"
                f"Notes: {booking.notes}\n\n"
                f"Best regards,\nYour Booking System",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[staff.email],
        fail_silently=False,
    )

    # Confirm to patient
    send_mail(
        subject="Appointment Confirmation",
        message=(f"Dear {booking.patient_name},\n\n"
                 f"Your appointment with {staff.role} {staff.first_name} is pending.\n"
                 f"📅 Date: {booking.day}\n"
                 f"⏰ Time: {booking.time}\n"
                 f"📝 Notes: {booking.notes if booking.notes else 'No notes'}\n\n"
                 f"Best regards,\nClinic Team"),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[booking.patient_email],
        fail_silently=False,
    )

    messages.success(request, "Appointment booked successfully!")
    return redirect('appointment_success')


def appointment_page(request, staff_id):
    staff = get_object_or_404(Staff, id=staff_id)
    selected_date = request.GET.get('date')
    available_slots = []

    if selected_date:
        try:
            day = datetime.strptime(selected_date, "%Y-%m-%d").date()
            available_slots = get_available_slots(staff, day)
        except ValueError:
            selected_date = None

    return render(request, 'booking/appointment_page.html', {
        'staff': staff,
        'available_slots': available_slots,
        'selected_date': selected_date
    })



def get_available_slots(staff, day):
    start = datetime.combine(day, staff.available_time_start)
    end = datetime.combine(day, staff.available_time_end)

    slots = []
    while start < end:
        slots.append(start.time())
        start += timedelta(minutes=40)

    booked = list(
        Booking.objects.filter(staff=staff, day=day).values_list('time', flat=True)
    )

    available = [slot for slot in slots if slot not in booked]

    # Format for dropdown display
    return [slot.strftime("%H:%M") for slot in available]



# ------------------------
# Doctor Dashboard
# ------------------------
@login_required
def staff_dashboard(request):
    staff = request.user # already a Staff instance
    today = timezone.localdate()   
    appointments = Booking.objects.filter(staff=staff).order_by('day', 'time')

    return render(request, 'booking/staff_dashboard.html', {
        'staff': staff,
        'appointments': appointments,
        'today' : today
    })



# ------------------------
# Public Pages
# ------------------------
def home(request):
    return render(request, 'booking/home.html')

def about(request):
    return render(request, 'booking/about.html')

def booking_page(request):
    return render(request, 'booking/booking.html')

def contact(request):
    return render(request, 'booking/contactus.html')

def appointment_success(request):
    return render(request, 'booking/appointment_success.html')



# ------------------------
# Doctors Page
# ------------------------
def care_team(request):
    staff_members = Staff.objects.all()
    return render(request, 'booking/care_team.html', {'care_team': staff_members})


def staff_detail(request, id):
    # Show any staff member by ID
    staff_member = get_object_or_404(Staff, id=id)
    return render(request, 'booking/staff_detail.html', {'staff': staff_member})


# views.py
def patient_dashboard(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        return redirect('patient_dashboard_email', email=email)

    return render(request, 'booking/patient_dashboard_form.html')


def patient_dashboard_email(request, email):
    today = timezone.localdate()  # current date

    # Get all bookings for this patient, ordered by date and time
    bookings = Booking.objects.filter(
        patient_email=email
    ).order_by('day', 'time')

    patient_name = bookings.first().patient_name if bookings.exists() else "Patient"

    return render(request, 'booking/patient_dashboard.html', {
        'bookings': bookings,
        'patient_name': patient_name,
        'email': email,
        'today': today
    })

