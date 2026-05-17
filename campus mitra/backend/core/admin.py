from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import (User, Department, Student, Faculty, Parent,
                     Subject, Timetable, Attendance, Note, Announcement)


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_active')
    list_filter = ('role', 'is_active')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Campus Mitra', {'fields': ('role', 'phone')}),
    )


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('enrollment_no', 'get_name', 'department', 'semester', 'section', 'cgpa')
    list_filter = ('department', 'semester', 'section')
    search_fields = ('enrollment_no', 'user__first_name', 'user__last_name', 'user__email')

    def get_name(self, obj):
        return obj.user.get_full_name()
    get_name.short_description = 'Name'


@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = ('faculty_id', 'get_name', 'department', 'designation')
    list_filter = ('department',)
    search_fields = ('faculty_id', 'user__first_name', 'user__last_name', 'user__email')

    def get_name(self, obj):
        return obj.user.get_full_name()
    get_name.short_description = 'Name'


@admin.register(Parent)
class ParentAdmin(admin.ModelAdmin):
    list_display = ('get_name',)

    def get_name(self, obj):
        return obj.user.get_full_name()
    get_name.short_description = 'Name'


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'department', 'semester', 'faculty')
    list_filter = ('department', 'semester')


@admin.register(Timetable)
class TimetableAdmin(admin.ModelAdmin):
    list_display = ('subject', 'department', 'section', 'day', 'start_time', 'end_time', 'room')
    list_filter = ('department', 'day', 'section')


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'subject', 'date', 'status', 'marked_by')
    list_filter = ('status', 'date', 'subject__department')
    date_hierarchy = 'date'


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject', 'uploaded_by', 'uploaded_at')
    list_filter = ('subject__department',)


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'audience', 'urgency', 'posted_by', 'created_at')
    list_filter = ('audience', 'urgency')
