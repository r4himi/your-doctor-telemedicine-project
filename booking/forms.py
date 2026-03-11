from django import forms
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from .models import Staff

DAYS_OF_WEEK = [
    ('Sat', 'Saturday'),
    ('Sun', 'Sunday'),
    ('Mon', 'Monday'),
    ('Tue', 'Tuesday'),
    ('Wed', 'Wednesday'),
    ('Thu', 'Thursday'),
    ('Fri', 'Friday'),
]

# ------------------------
# Staff Creation Form
# ------------------------
class StaffCreationForm(forms.ModelForm):
    available_day_start = forms.ChoiceField(
        choices=DAYS_OF_WEEK,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    available_day_end = forms.ChoiceField(
        choices=DAYS_OF_WEEK,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Staff
        fields = (
            'first_name',
            'email',
            'role',
            'speciality',
            'language',
            'bio',
            'available_day_start',
            'available_day_end',
            'available_time_start',
            'available_time_end',
            'image',
        )

# ------------------------
# Staff Update Form
# ------------------------
class StaffUpdateForm(UserChangeForm):
    password = None
    available_day_start = forms.ChoiceField(
        choices=DAYS_OF_WEEK,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    available_day_end = forms.ChoiceField(
        choices=DAYS_OF_WEEK,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Staff
        fields = [
            'username',
            'email',
            'role',
            'speciality',
            'experience',
            'language',
            'bio',
            'image',
            'available_day_start',
            'available_day_end',
            'available_time_start',
            'available_time_end',
        ]
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'role': forms.Select(attrs={'class': 'form-control'}),
            'speciality': forms.TextInput(attrs={'class': 'form-control'}),
            'experience': forms.NumberInput(attrs={'class': 'form-control'}),
            'language': forms.TextInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'available_time_start': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'available_time_end': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }

# ------------------------
# Staff Password Change Form
# ------------------------
class StaffPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}), label="Current Password")
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}), label="New Password")
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}), label="Confirm New Password")