from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('booking/', views.booking_page, name='booking'),
    path('patient-dashboard/', views.patient_dashboard, name='patient_dashboard'),
    path('patient-dashboard/<str:email>/', views.patient_dashboard_email, name='patient_dashboard_email'),
    path('care-team/', views.care_team, name='care_team'),
    path('care-team/<int:id>/', views.staff_detail, name='staff_detail'),
    path('submit-appointment/<int:staff_id>/', views.submit_appointment, name='submit_appointment'),
    path('appointment-success/', views.appointment_success, name='appointment_success'),
    path('appointment/<int:staff_id>/', views.appointment_page, name='appointment_page'),
    path('login/', views.staff_login, name='login'),
    path('logout/', views.staff_logout, name='logout'),
    #path('booking/<int:booking_id>/send-zoom/', views.send_zoom_link, name='send_zoom_link'),
    path('booking/<int:booking_id>/cancel/', views.cancel_booking, name='cancel_booking'),
    path('dashboard/', views.staff_dashboard, name='staff_dashboard'),  
    path('profile/', views.staff_profile, name='staff_profile'),
    # path('booking/<int:booking_id>/accept/', views.accept_booking, name='accept_booking'),
    path('contact/', views.contact, name='contactus'),
    path(
        'booking/<int:booking_id>/enter-zoom/',
        views.enter_zoom_link,
        name='enter_zoom_link'
    ),

    path(
        "staff/booking/<int:booking_id>/accept/",
        views.accept_booking_manual,
        name="accept_booking_manual"
    ),
    path('admin-login/', views.admin_login, name='admin_login'),
]