from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('faculty', 'Faculty'),
        ('parent', 'Parent'),
        ('admin', 'Admin'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')
    phone = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return f"{self.get_full_name()} ({self.role})"


class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    enroll_no = models.CharField(max_length=20, unique=True)
    branch = models.CharField(max_length=50, default='AIML')
    semester = models.PositiveSmallIntegerField(default=6)
    section = models.CharField(max_length=5, default='B')
    cgpa = models.DecimalField(max_digits=4, decimal_places=2, default=0.0)

    def __str__(self):
        return f"{self.user.get_full_name()} — {self.enroll_no}"


class FacultyProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='faculty_profile')
    faculty_id = models.CharField(max_length=20, unique=True)
    department = models.CharField(max_length=100)
    subjects = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.user.get_full_name()} — {self.faculty_id}"


class ParentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='parent_profile')
    child = models.ForeignKey(
        StudentProfile, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='parents'
    )

    def __str__(self):
        return f"{self.user.get_full_name()} → {self.child}"
