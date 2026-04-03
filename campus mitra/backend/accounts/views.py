from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        role     = request.POST.get('role', 'student')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.role == role:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request, f'This account is not registered as {role}.')
        else:
            messages.error(request, 'Invalid email/ID or password.')

    return render(request, 'accounts/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def dashboard_redirect(request):
    role = request.user.role
    redirects = {
        'student': 'student_dashboard',
        'faculty': 'faculty_dashboard',
        'parent':  'parent_dashboard',
        'admin':   'admin_dashboard',
    }
    return redirect(redirects.get(role, 'login'))


@login_required
def student_dashboard(request):
    if request.user.role != 'student':
        return redirect('dashboard')
    profile = getattr(request.user, 'student_profile', None)
    
    from attendance.models import AttendanceSummary
    from notes.models import Note
    
    summaries = AttendanceSummary.objects.filter(student=profile).order_by('subject') if profile else []
    recent_notes = Note.objects.filter(is_active=True)[:8]
    
    return render(request, 'accounts/student_dashboard.html', {
        'profile': profile,
        'summaries': summaries,
        'recent_notes': recent_notes,
    })


@login_required
def faculty_dashboard(request):
    if request.user.role != 'faculty':
        return redirect('dashboard')
    profile = getattr(request.user, 'faculty_profile', None)

    from attendance.models import TimetableSlot, AttendanceSession, AttendanceRecord
    from accounts.models import StudentProfile
    from django.utils import timezone
    from datetime import date as dt

    today = timezone.localdate()
    day_map = {0:'MON',1:'TUE',2:'WED',3:'THU',4:'FRI',5:'SAT',6:'SUN'}

    # Selected date — default today, can be changed via GET param
    selected_date_str = request.GET.get('att_date', str(today))
    try:
        selected_date = dt.fromisoformat(selected_date_str)
    except ValueError:
        selected_date = today

    selected_day = day_map.get(selected_date.weekday(), 'MON')

    # All theory slots for this faculty
    theory_slots = TimetableSlot.objects.filter(
        faculty=request.user, type='theory'
    ).order_by('day', 'start_time')

    # Slots for selected date
    date_slots = theory_slots.filter(day=selected_day)

    # All students AIML sem 6
    students = StudentProfile.objects.filter(
        branch='AIML', semester=6
    ).select_related('user').order_by('enroll_no')

    # Handle attendance submission
    if request.method == 'POST':
        slot_id   = request.POST.get('slot_id')
        date_str  = request.POST.get('date', str(today))
        post_date = dt.fromisoformat(date_str)
        post_day  = day_map.get(post_date.weekday(), 'MON')

        slot = TimetableSlot.objects.get(pk=slot_id, faculty=request.user)
        session, _ = AttendanceSession.objects.get_or_create(
            slot=slot, date=post_date,
            defaults={'marked_by': request.user}
        )

        for student in students:
            status = request.POST.get(f'status_{student.id}', 'absent')
            AttendanceRecord.objects.update_or_create(
                session=session, student=student,
                defaults={'status': status}
            )

        if 'finalize' in request.POST:
            session.is_finalized = True
            session.save()
            from attendance.views import _update_summaries
            _update_summaries(slot.subject, students)

        from django.contrib import messages
        messages.success(request, f'Attendance saved for {post_date}.')
        return redirect(f'/dashboard/faculty/?att_date={post_date.isoformat()}')

    # Get already marked sessions for selected date
    marked_sessions = {
        s.slot_id: s for s in AttendanceSession.objects.filter(
            slot__in=date_slots, date=selected_date
        ).prefetch_related('records')
    }

    date_slot_data = []
    for slot in date_slots:
        session = marked_sessions.get(slot.id)
        records = {}
        if session:
            records = {r.student_id: r.status for r in session.records.all()}
        date_slot_data.append({
            'slot': slot,
            'session': session,
            'records': records,
            'is_finalized': session.is_finalized if session else False,
        })

    return render(request, 'accounts/faculty_dashboard.html', {
        'profile': profile,
        'theory_slots': theory_slots,
        'today_slots': date_slot_data,
        'students': students,
        'today': today,
        'selected_date': selected_date,
        'is_past': selected_date < today,
    })


@login_required
def parent_dashboard(request):
    if request.user.role != 'parent':
        return redirect('dashboard')
    profile = getattr(request.user, 'parent_profile', None)
    return render(request, 'accounts/parent_dashboard.html', {'profile': profile})


@login_required
def admin_dashboard(request):
    if request.user.role != 'admin':
        return redirect('dashboard')
    return render(request, 'accounts/admin_dashboard.html')
