# Campus Mitra — Backend Implementation Guide

> Stack: Python 3.x · Django · MySQL 8.0 · Django REST Framework

---

## 1. Project Setup

```bash
pip install django mysqlclient djangorestframework djangorestframework-simplejwt pillow python-decouple

django-admin startproject campusmitra .
python manage.py startapp core
```

Final folder structure:
```
campusmitra/
├── campusmitra/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── core/
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   ├── urls.py
│   ├── permissions.py
│   └── admin.py
├── media/
├── manage.py
└── .env
```

---

## 2. Environment File (.env)

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
DB_NAME=campus_mitra_db
DB_USER=root
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=3306
```

---

## 3. settings.py

```python
from decouple import config
from datetime import timedelta

SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', cast=bool)

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_simplejwt',
    'core',
]

AUTH_USER_MODEL = 'core.User'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT'),
    }
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=8),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
}

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

---

## 4. MySQL Database Setup

Run these in your MySQL shell:

```sql
CREATE DATABASE campus_mitra_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'campusmitra'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON campus_mitra_db.* TO 'campusmitra'@'localhost';
FLUSH PRIVILEGES;
```

---

## 5. Models (core/models.py)

```python
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLES = [
        ('student', 'Student'),
        ('faculty', 'Faculty'),
        ('parent', 'Parent'),
        ('admin', 'Admin'),
    ]
    role = models.CharField(max_length=10, choices=ROLES)
    phone = models.CharField(max_length=15, blank=True)


class Department(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.name


class Parent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.get_full_name()


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    enrollment_no = models.CharField(max_length=20, unique=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    semester = models.IntegerField()
    section = models.CharField(max_length=5)
    cgpa = models.DecimalField(max_digits=4, decimal_places=2, default=0.0)
    parent = models.ForeignKey(Parent, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.enrollment_no})"


class Faculty(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    faculty_id = models.CharField(max_length=20, unique=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    designation = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.faculty_id})"


class Subject(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    semester = models.IntegerField()
    faculty = models.ForeignKey(Faculty, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.code} - {self.name}"


class Timetable(models.Model):
    DAYS = [
        ('Mon', 'Monday'), ('Tue', 'Tuesday'), ('Wed', 'Wednesday'),
        ('Thu', 'Thursday'), ('Fri', 'Friday'), ('Sat', 'Saturday'),
    ]
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    section = models.CharField(max_length=5)
    day = models.CharField(max_length=3, choices=DAYS)
    start_time = models.TimeField()
    end_time = models.TimeField()
    room = models.CharField(max_length=20)


class Attendance(models.Model):
    STATUS = [('P', 'Present'), ('A', 'Absent'), ('L', 'Late')]
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=1, choices=STATUS)
    marked_by = models.ForeignKey(Faculty, on_delete=models.SET_NULL, null=True)

    class Meta:
        unique_together = ('student', 'subject', 'date')


class Note(models.Model):
    title = models.CharField(max_length=200)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    uploaded_by = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    file = models.FileField(upload_to='notes/')
    uploaded_at = models.DateTimeField(auto_now_add=True)


class Announcement(models.Model):
    AUDIENCE = [
        ('all', 'All'), ('students', 'Students'),
        ('faculty', 'Faculty'), ('parents', 'Parents'),
    ]
    URGENCY = [('general', 'General'), ('urgent', 'Urgent'), ('event', 'Event')]
    title = models.CharField(max_length=200)
    content = models.TextField()
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE)
    audience = models.CharField(max_length=10, choices=AUDIENCE)
    urgency = models.CharField(max_length=10, choices=URGENCY, default='general')
    created_at = models.DateTimeField(auto_now_add=True)
```

---

## 6. Serializers (core/serializers.py)

```python
from rest_framework import serializers
from .models import (User, Student, Faculty, Parent, Subject,
                     Timetable, Attendance, Note, Announcement)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'first_name', 'last_name']


class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Student
        fields = '__all__'


class FacultySerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Faculty
        fields = '__all__'


class TimetableSerializer(serializers.ModelSerializer):
    subject_name = serializers.CharField(source='subject.name', read_only=True)
    class Meta:
        model = Timetable
        fields = '__all__'


class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = '__all__'


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = '__all__'


class AnnouncementSerializer(serializers.ModelSerializer):
    posted_by_name = serializers.CharField(source='posted_by.get_full_name', read_only=True)
    class Meta:
        model = Announcement
        fields = '__all__'
```

---

## 7. Permissions (core/permissions.py)

```python
from rest_framework.permissions import BasePermission


class IsStudent(BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user, 'student')


class IsFaculty(BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user, 'faculty')


class IsParent(BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user, 'parent')


class IsAdminUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'admin'
```

---

## 8. Views (core/views.py)

```python
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import *
from .serializers import *
from .permissions import IsFaculty, IsStudent, IsParent, IsAdminUser


# ── Auth ──────────────────────────────────────────────────────────────────────

class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(username=email, password=password)
        if not user:
            return Response({'error': 'Invalid credentials'}, status=400)
        refresh = RefreshToken.for_user(user)
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'role': user.role,
            'name': user.get_full_name(),
        })


# ── Attendance ────────────────────────────────────────────────────────────────

class MarkAttendanceView(APIView):
    """Faculty marks attendance — expects list of records"""
    permission_classes = [IsFaculty]

    def post(self, request):
        records = request.data.get('records', [])
        # records = [{ student, subject, date, status }, ...]
        count = 0
        for r in records:
            Attendance.objects.update_or_create(
                student_id=r['student'],
                subject_id=r['subject'],
                date=r['date'],
                defaults={
                    'status': r['status'],
                    'marked_by': request.user.faculty
                }
            )
            count += 1
        return Response({'marked': count})


class StudentAttendanceView(APIView):
    """Student views their subject-wise attendance"""
    permission_classes = [IsStudent]

    def get(self, request):
        student = request.user.student
        subjects = Subject.objects.filter(
            department=student.department,
            semester=student.semester
        )
        data = []
        for sub in subjects:
            total = Attendance.objects.filter(student=student, subject=sub).count()
            present = Attendance.objects.filter(student=student, subject=sub, status='P').count()
            pct = round((present / total * 100), 1) if total else 0
            data.append({
                'subject': sub.name,
                'code': sub.code,
                'total': total,
                'present': present,
                'percentage': pct,
                'shortage': pct < 75
            })
        return Response(data)


# ── Notes ─────────────────────────────────────────────────────────────────────

class NoteUploadView(generics.CreateAPIView):
    serializer_class = NoteSerializer
    permission_classes = [IsFaculty]

    def perform_create(self, serializer):
        serializer.save(uploaded_by=self.request.user.faculty)


class NoteListView(generics.ListAPIView):
    serializer_class = NoteSerializer
    permission_classes = [IsStudent]

    def get_queryset(self):
        student = self.request.user.student
        return Note.objects.filter(
            subject__department=student.department,
            subject__semester=student.semester
        ).order_by('-uploaded_at')


# ── Announcements ─────────────────────────────────────────────────────────────

class AnnouncementListView(generics.ListAPIView):
    serializer_class = AnnouncementSerializer

    def get_queryset(self):
        role = self.request.user.role
        return Announcement.objects.filter(
            audience__in=['all', f'{role}s']
        ).order_by('-created_at')


class AnnouncementCreateView(generics.CreateAPIView):
    serializer_class = AnnouncementSerializer

    def perform_create(self, serializer):
        serializer.save(posted_by=self.request.user)


# ── Timetable ─────────────────────────────────────────────────────────────────

class TimetableView(APIView):
    def get(self, request):
        user = request.user
        if hasattr(user, 'student'):
            s = user.student
            slots = Timetable.objects.filter(
                department=s.department, section=s.section
            )
        elif hasattr(user, 'faculty'):
            slots = Timetable.objects.filter(
                subject__faculty=user.faculty
            )
        else:
            slots = Timetable.objects.all()
        return Response(TimetableSerializer(slots, many=True).data)


# ── Parent ────────────────────────────────────────────────────────────────────

class ParentChildView(APIView):
    """Parent views their child's profile"""
    permission_classes = [IsParent]

    def get(self, request):
        children = Student.objects.filter(parent=request.user.parent)
        return Response(StudentSerializer(children, many=True).data)


# ── Admin ─────────────────────────────────────────────────────────────────────

class UserListView(generics.ListCreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]
    queryset = User.objects.all()


class AttendanceAlertView(APIView):
    """Admin gets list of students with attendance below 75%"""
    permission_classes = [IsAdminUser]

    def get(self, request):
        students = Student.objects.all()
        alerts = []
        for s in students:
            total = Attendance.objects.filter(student=s).count()
            present = Attendance.objects.filter(student=s, status='P').count()
            pct = round((present / total * 100), 1) if total else 0
            if pct < 75:
                alerts.append({
                    'student': s.user.get_full_name(),
                    'enrollment': s.enrollment_no,
                    'percentage': pct
                })
        return Response(alerts)
```

---

## 9. URLs

**core/urls.py**
```python
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

urlpatterns = [
    # Auth
    path('auth/login/',         views.LoginView.as_view()),
    path('auth/refresh/',       TokenRefreshView.as_view()),

    # Attendance
    path('attendance/mark/',    views.MarkAttendanceView.as_view()),
    path('attendance/my/',      views.StudentAttendanceView.as_view()),

    # Notes
    path('notes/',              views.NoteListView.as_view()),
    path('notes/upload/',       views.NoteUploadView.as_view()),

    # Announcements
    path('announcements/',      views.AnnouncementListView.as_view()),
    path('announcements/new/',  views.AnnouncementCreateView.as_view()),

    # Timetable
    path('timetable/',          views.TimetableView.as_view()),

    # Parent
    path('parent/children/',    views.ParentChildView.as_view()),

    # Admin
    path('admin/users/',        views.UserListView.as_view()),
    path('admin/alerts/',       views.AttendanceAlertView.as_view()),
]
```

**campusmitra/urls.py**
```python
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('core.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

---

## 10. Run Migrations & Start Server

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

- API base: `http://127.0.0.1:8000/api/`
- Django admin: `http://127.0.0.1:8000/admin/`

---

## 11. Connect Frontend (login.html)

Replace the demo redirect in `login.html` with this:

```javascript
async function handleLogin(email, password) {
    const res = await fetch('http://127.0.0.1:8000/api/auth/login/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
    });
    const data = await res.json();
    if (res.ok) {
        localStorage.setItem('access_token', data.access);
        localStorage.setItem('role', data.role);
        const routes = {
            student: 'student.html',
            faculty: 'faculty.html',
            parent: 'parent.html',
            admin:   'admin.html'
        };
        window.location.href = routes[data.role];
    } else {
        alert('Invalid credentials');
    }
}
```

Reusable API helper for all dashboards:

```javascript
async function apiFetch(endpoint, options = {}) {
    const token = localStorage.getItem('access_token');
    const res = await fetch(`http://127.0.0.1:8000/api/${endpoint}`, {
        ...options,
        headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
            ...options.headers
        }
    });
    if (res.status === 401) {
        localStorage.clear();
        window.location.href = 'login.html';
    }
    return res.json();
}

// Usage examples:
const attendance = await apiFetch('attendance/my/');
const notices    = await apiFetch('announcements/');
const timetable  = await apiFetch('timetable/');
```

---

## 12. API Reference

| Method | Endpoint | Who Can Call | What It Does |
|--------|----------|--------------|--------------|
| POST | `/api/auth/login/` | Anyone | Login, returns JWT + role |
| POST | `/api/auth/refresh/` | Anyone | Refresh access token |
| POST | `/api/attendance/mark/` | Faculty | Mark attendance for a class |
| GET | `/api/attendance/my/` | Student | Subject-wise attendance % |
| GET | `/api/notes/` | Student | List downloadable notes |
| POST | `/api/notes/upload/` | Faculty | Upload PDF/PPT/DOCX |
| GET | `/api/announcements/` | All | Role-filtered announcements |
| POST | `/api/announcements/new/` | Faculty / Admin | Post announcement |
| GET | `/api/timetable/` | Student / Faculty | View timetable |
| GET | `/api/parent/children/` | Parent | Child profile + stats |
| GET | `/api/admin/users/` | Admin | List all users |
| GET | `/api/admin/alerts/` | Admin | Students below 75% attendance |

---

*Campus Mitra — VisionX | IIST Indore*
