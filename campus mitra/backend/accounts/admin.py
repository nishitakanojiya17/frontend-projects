from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, StudentProfile, FacultyProfile, ParentProfile


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Campus Mitra', {'fields': ('role', 'phone')}),
    )
    list_display = ('username', 'email', 'get_full_name', 'role', 'is_active')
    list_filter  = ('role', 'is_active')


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'enroll_no', 'branch', 'semester', 'section', 'cgpa')
    search_fields = ('enroll_no', 'user__first_name', 'user__last_name')


@admin.register(FacultyProfile)
class FacultyProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'faculty_id', 'department', 'subjects')


@admin.register(ParentProfile)
class ParentProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'child')
