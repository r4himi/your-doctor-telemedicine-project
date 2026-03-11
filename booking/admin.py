from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from .models import Staff, Booking, generate_staff_code
from .forms import StaffCreationForm, StaffUpdateForm  # you can rename forms later for Staff

# ------------------------
# Staff Admin
# ------------------------
@admin.register(Staff)
class StaffAdmin(UserAdmin):
    add_form = StaffCreationForm  # can rename later to StaffCreationForm
    form = StaffUpdateForm        # can rename later to StaffUpdateForm
    model = Staff

    list_display = ('username', 'email', 'staff_id', 'role', 'experience', 'is_staff')
    readonly_fields = ('staff_id', 'username')

    fieldsets = (
        (None, {'fields': ('first_name', 'email', 'role', 'speciality', 'language', 'bio', 'image', 'experience')}),
        ('Availability', {'fields': ('available_day_start', 'available_day_end','available_time_start','available_time_end')}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('first_name', 'email', 'role', 'speciality', 'experience', 'language', 'bio', 'available_day_start', 'available_day_end','available_time_start','available_time_end')}
        ),
    )

    list_filter = ('role', 'is_staff', 'is_superuser')
    search_fields = ('username', 'first_name', 'last_name', 'email')

    def save_model(self, request, obj, form, change):
        is_new = not obj.pk

        if is_new:
            if not obj.username:
                obj.username = f"{obj.role}_" + get_random_string(6).lower()

            if not obj.staff_id:
                obj.staff_id = generate_staff_code(obj.role)

            raw_password = get_random_string(10)
            obj.set_password(raw_password)

        super().save_model(request, obj, form, change)

        if is_new and obj.email:
            role_display = dict(Staff.ROLE_CHOICES).get(obj.role)

            send_mail(
                subject="Your Account",
                message=(
                    f"Hello {role_display} {obj.first_name},\n\n"
                    f"ID: {obj.staff_id}\n"
                    f"Username: {obj.username}\n"
                    f"Password: {raw_password}\n\n"
                    f"Login here: http://127.0.0.1:8000/login/\n"
                    f"Please change your password after first login."
                ),
                from_email=None,
                recipient_list=[obj.email],
                fail_silently=False
            )


# ------------------------
# Booking Admin
# ------------------------
@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('patient_name', 'patient_email', 'staff', 'day', 'time', 'status')
    list_filter = ('status', 'day')
    search_fields = ('patient_name', 'patient_email', 'staff__first_name', 'staff__last_name')