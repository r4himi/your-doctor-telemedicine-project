from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import datetime
from booking.models import Booking
from django.core.mail import send_mail
from django.conf import settings


class Command(BaseCommand):
    help = "Send Zoom reminder emails 15 minutes before appointment"

    def handle(self, *args, **kwargs):

        now = timezone.now()

        bookings = Booking.objects.filter(
            status="Accepted",
            reminder_sent=False
        ).exclude(zoom_link__isnull=True).exclude(zoom_link="")

        for booking in bookings:

            appointment_dt = timezone.make_aware(
                datetime.combine(booking.day, booking.time),
                timezone.get_current_timezone()
            )

            minutes_until = (appointment_dt - now).total_seconds() / 60

            if minutes_until < 0:
                continue

            if 10 <= minutes_until <= 15:

                send_mail(
                    subject="Reminder: Your Appointment Starts in 15 Minutes",
                    message=(
                        f"Dear {booking.patient_name},\n\n"
                        f"Your appointment starts in 15 minutes.\n"
                        f"📅 Date: {booking.day}\n"
                        f"⏰ Time: {booking.time}\n"
                        f"🔗 Zoom Link: {booking.zoom_link}\n\n"
                        f"Best regards,\nClinic Team"
                    ),
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[booking.patient_email],
                )

                send_mail(
                    subject="Upcoming Appointment Reminder",
                    message=(
                        f"You have an appointment with {booking.patient_name} in 15 minutes.\n"
                        f"Zoom Link: {booking.zoom_link}"
                    ),
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[booking.staff.email],
                )

                booking.reminder_sent = True
                booking.save()

                self.stdout.write(self.style.SUCCESS(
                    f"Reminder sent for booking {booking.id}"
                ))