# 🩺 YourDoctor

**YourDoctor** is a Django-based staff and appointment management system designed for clinics, hospitals, and telemedicine platforms.  
It provides a structured backend and a clean, user-friendly interface to manage appointments, staff workflows, and patient communication.

---

## 📸 Screenshots

### 🏠 Home Page
![Home](UI and UX/home.jpg)

### 👨‍⚕️ Care Team Page
Displays available medical staff with filtering by speciality, role, and language.
![Care Team](UI and UX/care-team-page.jpg)

### 📅 Booking Page
Users can schedule and manage appointments easily.
![Booking](UI and UX/booking.jpg)

---

## ✨ Features

### 👨‍⚕️ Staff & Patient Management
- Secure authentication system  
- Role-based access control  
- Customizable staff profiles  
- Patient record management  

### 📅 Booking System
- Appointment scheduling and cancellation  
- Cancellation reason tracking  
- Email notifications via Django `send_mail`  
- Zoom link integration for telemedicine sessions  

### ⚙️ Workflow Automation
- Background task processing prepared with Celery  
- Redis configured as a message broker  
- Designed for asynchronous tasks such as email reminders and notifications  

> ⚠️ *Note: Celery and Redis require additional configuration and may not be fully active in the current setup.*

### 🎨 Frontend & UI
- Responsive and mobile-friendly layout  
- Clean and intuitive user interface  
- Built using Bootstrap  
- HTML, CSS, and JavaScript frontend  
- Multilingual support  

### 🚀 Deployment Ready
- Production-ready structure  
- Scalable architecture  
- Optional Redis integration for background processing  

---

## 🛠️ Tech Stack

| Technology | Purpose |
|-----------|--------|
| Python | Core programming language |
| Django | Backend web framework |
| HTML | Frontend structure |
| CSS | Styling |
| JavaScript | Interactivity |
| Bootstrap | UI components |
| Celery | Background task processing (optional) |
| Redis | Message broker |
| Django `send_mail` | Email notifications |

---

## 🚀 Getting Started

### 📋 Prerequisites
- Python 3.10+  
- pip  
- Redis server *(optional for background tasks)*  

---

### ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/r4himi/yourdoctor.git
cd yourdoctor