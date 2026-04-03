from django.contrib import admin
from .models import TimetableSlot, AttendanceSession, AttendanceRecord, AttendanceSummary


@admin.register(TimetableSlot)
class TimetableSlotAdmin(admin.ModelAdmin):
    list_display = ('day', 'start_time', 'end_time', 'subject', 'type', 'batch', 'faculty', 'room')
    list_filter  = ('day', 'subject', 'type', 'batch')


@admin.register(AttendanceSession)
class AttendanceSessionAdmin(admin.ModelAdmin):
    list_display = ('date', 'slot', 'marked_by', 'is_finalized')
    list_filter  = ('is_finalized', 'slot__subject')


@admin.register(AttendanceRecord)
class AttendanceRecordAdmin(admin.ModelAdmin):
    list_display = ('session', 'student', 'status')
    list_filter  = ('status',)


@admin.register(AttendanceSummary)
class AttendanceSummaryAdmin(admin.ModelAdmin):
    list_display = ('student', 'subject', 'total_classes', 'present_count', 'percentage')
    list_filter  = ('subject',)
