from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import TimetableSlot, AttendanceSession, AttendanceRecord, AttendanceSummary
from accounts.models import StudentProfile


@login_required
def mark_attendance(request, slot_id):
    """Faculty marks attendance for a timetable slot on today's date."""
    if request.user.role != 'faculty':
        return redirect('dashboard')

    slot = get_object_or_404(TimetableSlot, pk=slot_id, faculty=request.user)
    today = timezone.localdate()

    # Get or create today's session
    session, created = AttendanceSession.objects.get_or_create(
        slot=slot, date=today,
        defaults={'marked_by': request.user}
    )

    if session.is_finalized:
        messages.warning(request, 'Attendance already finalized for this session.')
        return redirect('faculty_attendance_list')

    # Get students for this batch
    if slot.batch == 'ALL':
        students = StudentProfile.objects.filter(semester=6, branch='AIML').order_by('enroll_no')
    elif slot.batch == 'B1':
        students = StudentProfile.objects.filter(semester=6, branch='AIML').order_by('enroll_no')[:10]
    else:
        students = StudentProfile.objects.filter(semester=6, branch='AIML').order_by('enroll_no')[10:]

    # Pre-create absent records if new session
    if created:
        AttendanceRecord.objects.bulk_create([
            AttendanceRecord(session=session, student=s, status='absent')
            for s in students
        ])

    if request.method == 'POST':
        for student in students:
            status = request.POST.get(f'status_{student.id}', 'absent')
            AttendanceRecord.objects.filter(session=session, student=student).update(status=status)

        if 'finalize' in request.POST:
            session.is_finalized = True
            session.save()
            _update_summaries(slot.subject, students)
            messages.success(request, 'Attendance finalized successfully.')
            return redirect('faculty_attendance_list')

        messages.success(request, 'Attendance saved (not finalized yet).')

    records = {r.student_id: r.status for r in session.records.all()}
    return render(request, 'attendance/mark_attendance.html', {
        'slot': slot, 'session': session,
        'students': students, 'records': records, 'today': today,
    })


@login_required
def faculty_attendance_list(request):
    """Faculty sees their today's slots to mark attendance."""
    if request.user.role != 'faculty':
        return redirect('dashboard')

    today = timezone.localdate()
    day_map = {0:'MON',1:'TUE',2:'WED',3:'THU',4:'FRI',5:'SAT',6:'SUN'}
    today_day = day_map.get(today.weekday(), 'MON')

    slots = TimetableSlot.objects.filter(faculty=request.user)
    today_slots = slots.filter(day=today_day)

    # Check which sessions are already marked today
    marked_today = AttendanceSession.objects.filter(
        slot__in=today_slots, date=today
    ).values_list('slot_id', flat=True)

    return render(request, 'attendance/faculty_attendance_list.html', {
        'today_slots': today_slots,
        'all_slots': slots,
        'marked_today': list(marked_today),
        'today': today,
    })


@login_required
def student_attendance_view(request):
    """Student sees their own attendance summary."""
    if request.user.role != 'student':
        return redirect('dashboard')

    profile = get_object_or_404(StudentProfile, user=request.user)
    summaries = AttendanceSummary.objects.filter(student=profile).order_by('subject')

    return render(request, 'attendance/student_attendance.html', {
        'summaries': summaries,
        'profile': profile,
    })


@login_required
def admin_attendance_report(request):
    """Admin sees all students' attendance summary."""
    if request.user.role != 'admin':
        return redirect('dashboard')

    summaries = AttendanceSummary.objects.select_related('student__user').order_by(
        'student__enroll_no', 'subject'
    )
    shortage = summaries.filter(present_count__lt=1)  # will use percentage property in template

    return render(request, 'attendance/admin_report.html', {
        'summaries': summaries,
    })


def _update_summaries(subject, students):
    """Recalculate AttendanceSummary for given subject and students."""
    for student in students:
        total = AttendanceRecord.objects.filter(
            session__slot__subject=subject,
            session__is_finalized=True,
            student=student
        ).count()
        present = AttendanceRecord.objects.filter(
            session__slot__subject=subject,
            session__is_finalized=True,
            student=student,
            status='present'
        ).count()
        AttendanceSummary.objects.update_or_create(
            student=student, subject=subject,
            defaults={'total_classes': total, 'present_count': present}
        )
