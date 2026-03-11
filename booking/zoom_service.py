# zoom_service.py
import requests
import base64
from django.conf import settings
from datetime import datetime
from django.utils import timezone

def combine_booking_datetime(booking):
    """Combine booking date and time into timezone-aware datetime."""
    naive_dt = datetime.combine(booking.day, booking.time)
    aware_dt = timezone.make_aware(naive_dt, timezone.get_current_timezone())
    return aware_dt

def get_zoom_access_token():
    """
    Generate an access token using Account-Level OAuth (Account Credentials Grant)
    Make sure your Zoom app has scopes:
    - meeting:write
    - meeting:write:admin
    """
    url = f"https://zoom.us/oauth/token?grant_type=account_credentials&account_id={settings.ZOOM_ACCOUNT_ID}"
    credentials = f"{settings.ZOOM_CLIENT_ID}:{settings.ZOOM_CLIENT_SECRET}"
    encoded = base64.b64encode(credentials.encode()).decode()
    headers = {"Authorization": f"Basic {encoded}"}

    response = requests.post(url, headers=headers)
    data = response.json()
    
    if "access_token" not in data:
        print("Failed to get Zoom access token:", data)
        raise Exception("Zoom access token not received. Check client ID, secret, and app scopes.")

    return data["access_token"]

def create_zoom_meeting(booking):
    """
    Create a Zoom meeting for a booking.
    Returns dict: {"id": ..., "join_url": ...}
    """
    try:
        token = get_zoom_access_token()
    except Exception as e:
        print("Zoom token error:", e)
        return {"id": None, "join_url": None}

    start_time = combine_booking_datetime(booking).isoformat()

    url = f"https://api.zoom.us/v2/users/{booking.staff.email}/meetings"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    # Use full name with prefix if available, fallback to username
    staff_name = getattr(booking.staff, "full_name_with_prefix", booking.staff.username)

    payload = {
        "topic": f"Consultation with {staff_name}",
        "type": 2,  # scheduled meeting
        "start_time": start_time,
        "duration": 30,
        "timezone": "Asia/Kabul",  # Afghanistan timezone
        "settings": {
            "waiting_room": True,
            "join_before_host": False
        }
    }

    response = requests.post(url, json=payload, headers=headers)
    data = response.json()

    if "join_url" not in data or not data.get("id"):
        print("Zoom meeting creation failed. Response:", data)
        return {"id": None, "join_url": None}

    return {
        "id": data.get("id"),
        "join_url": data.get("join_url")
    }