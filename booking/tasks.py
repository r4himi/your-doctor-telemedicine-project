# tasks.py
from celery import shared_task
from datetime import datetime
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from .models import Booking

@shared_task
def send_zoom_reminder(booking_id):
    
    booking = Booking.objects.get(id=booking_id)

    appointment_dt = timezone.make_aware(
        datetime.combine(booking.day, booking.time),
        timezone.get_current_timezone()
    )

    send_mail(
        subject="Reminder: Your Appointment in 15 Minutes",
        message=f"Your appointment with {booking.staff.full_name_with_prefix} starts in 15 minutes. Zoom: {booking.zoom_link}",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[booking.patient_email],
    )

    send_mail(
        subject="Upcoming Appointment Reminder",
        message=f"You have an appointment with {booking.patient_name} in 15 minutes. Zoom: {booking.zoom_link}",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[booking.staff.email],
    )

    booking.reminder_sent = True
    booking.save()