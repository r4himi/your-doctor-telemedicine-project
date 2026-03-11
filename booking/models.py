import random
import string
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
import uuid


# ------------------------
# Staff ID generator
# ------------------------
def generate_staff_code(role):
    prefix_map = {
        'doctor': 'DR',
        'nurse': 'NR',
        'psychologist': 'PS',
    }
    prefix = prefix_map.get(role, 'ST')
    return f"{prefix}-{uuid.uuid4().hex[:6].upper()}"

def generate_doctor_code():
    # Keep for backward migration compatibility
    return generate_staff_code('doctor')

# ------------------------
# Password generator
# ------------------------
def generate_password(length=12):
    chars = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(chars) for _ in range(length))


# ------------------------
# Base Staff Model
# ------------------------
class Staff(AbstractUser):
    ROLE_CHOICES = [
        ('doctor', 'Doctor'),
        ('nurse', 'Nurse'),
        ('psychologist', 'Psychologist'),
        # add more roles later
    ]
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='doctor')
    
    staff_id = models.CharField(max_length=10, unique=True, editable=False)
    language = models.CharField(max_length=50, default='English')
    bio = models.TextField(blank=True)
    experience = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='staff/', default='default-doctor.jpg', blank=True, null=True)
    
    speciality = models.CharField(max_length=100, default='General')  # useful for doctors, optional for other roles
    available_day_start = models.CharField(max_length=10, default="Sat")
    available_day_end = models.CharField(max_length=10, default="Wed")

    available_time_start = models.TimeField(null=True, blank=True)
    available_time_end = models.TimeField(null=True, blank=True)

    
    def save(self, *args, **kwargs):
        if not self.staff_id:
            self.staff_id = generate_staff_code(self.role)
        super().save(*args, **kwargs)
    
    def __str__(self):
        role_display = dict(self.ROLE_CHOICES).get(self.role, 'Staff')
        if self.first_name:
            return f"{role_display} {self.first_name} ({self.staff_id})"
        return f"{role_display} {self.username} ({self.staff_id})"
    

    @property
    def prefix(self):
        """Return the title prefix based on role."""
        if self.role == 'doctor':
            return 'Dr.'
        elif self.role == 'nurse':
            return 'Nurse'
        elif self.role == 'psychologist':
            return 'Psychologist'
        return 'Staff'

    @property
    def full_name_with_prefix(self):
        """Return full name with prefix."""
        if self.first_name and self.last_name:
            return f"{self.prefix} {self.first_name} {self.last_name}"
        elif self.first_name:
            return f"{self.prefix} {self.first_name}"
        return f"{self.prefix} {self.username}"


# ------------------------

# ------------------------
# models.py
class Booking(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
    ]
    
    staff = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='bookings',
    )
    
    patient_name = models.CharField(max_length=100)
    patient_email = models.EmailField()
    notes = models.TextField(blank=True, null=True)
    
    day = models.DateField()
    time = models.TimeField()
    
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    zoom_link = models.URLField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    reminder_sent = models.BooleanField(default=False)
    zoom_meeting_id = models.CharField(max_length=50, blank=True, null=True)
    
    def __str__(self):
        return f"Booking with {self.staff.first_name} by {self.patient_name} on {self.day} at {self.time}"


# models.py, inside Staff class
    