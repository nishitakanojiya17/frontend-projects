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
    # Show only notes for this student's branch + ALL-branch notes
    branch = profile.branch if profile else None
    if branch:
        recent_notes = Note.objects.filter(is_active=True, branch__in=[branch, 'ALL'])[:8]
    else:
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

    selected_date_str = request.GET.get('att_date', str(today))
    try:
        selected_date = dt.fromisoformat(selected_date_str)
    except ValueError:
        selected_date = today

    selected_day = day_map.get(selected_date.weekday(), 'MON')

    # All slots (theory + practical) for this faculty
    all_slots = TimetableSlot.objects.filter(
        faculty=request.user
    ).order_by('day', 'start_time')

    # Slots for selected date
    date_slots = all_slots.filter(day=selected_day)

    # Determine branch from faculty's slots
    branch = 'AIML'
    if all_slots.exists():
        branch = all_slots.first().branch

    # Get students for this branch
    students = StudentProfile.objects.filter(
        branch=branch, semester=6
    ).select_related('user').order_by('enroll_no')

    # Handle attendance submission
    if request.method == 'POST':
        slot_id   = request.POST.get('slot_id')
        date_str  = request.POST.get('date', str(today))
        post_date = dt.fromisoformat(date_str)

        slot = TimetableSlot.objects.get(pk=slot_id, faculty=request.user)

        # For batch slots, filter students accordingly
        if slot.batch == 'B1':
            slot_students = students[:len(students)//2]
        elif slot.batch == 'B2':
            slot_students = students[len(students)//2:]
        else:
            slot_students = students

        session, _ = AttendanceSession.objects.get_or_create(
            slot=slot, date=post_date,
            defaults={'marked_by': request.user}
        )

        for student in slot_students:
            status = request.POST.get(f'status_{student.id}', 'absent')
            AttendanceRecord.objects.update_or_create(
                session=session, student=student,
                defaults={'status': status}
            )

        if 'finalize' in request.POST:
            session.is_finalized = True
            session.save()
            from attendance.views import _update_summaries
            _update_summaries(slot.subject, slot_students)

        messages.success(request, f'Attendance saved for {post_date}.')
        return redirect(f'/dashboard/faculty/?att_date={post_date.isoformat()}')

    # Build slot data for selected date
    marked_sessions = {
        s.slot_id: s for s in AttendanceSession.objects.filter(
            slot__in=date_slots, date=selected_date
        ).prefetch_related('records')
    }

    date_slot_data = []
    for slot in date_slots:
        # Batch-specific students
        if slot.batch == 'B1':
            slot_students = list(students[:len(students)//2])
        elif slot.batch == 'B2':
            slot_students = list(students[len(students)//2:])
        else:
            slot_students = list(students)

        session = marked_sessions.get(slot.id)
        records = {}
        if session:
            records = {r.student_id: r.status for r in session.records.all()}
        date_slot_data.append({
            'slot': slot,
            'session': session,
            'records': records,
            'is_finalized': session.is_finalized if session else False,
            'slot_students': slot_students,
        })

    # Separate theory and practical for sidebar display
    theory_slots  = all_slots.filter(type='theory')
    practical_slots = all_slots.filter(type__in=['practical', 'project'])

    return render(request, 'accounts/faculty_dashboard.html', {
        'profile':          profile,
        'theory_slots':     theory_slots,
        'practical_slots':  practical_slots,
        'today_slots':      date_slot_data,
        'students':         students,
        'today':            today,
        'selected_date':    selected_date,
        'is_past':          selected_date < today,
        'branch':           branch,
    })


@login_required
def parent_dashboard(request):
    if request.user.role != 'parent':
        return redirect('dashboard')
    profile = getattr(request.user, 'parent_profile', None)

    child_summaries = []
    recent_sessions = []
    if profile and profile.child:
        from attendance.models import AttendanceSummary, AttendanceRecord
        child_summaries = AttendanceSummary.objects.filter(
            student=profile.child
        ).order_by('subject')
        # Last 10 attendance records for the child
        recent_sessions = AttendanceRecord.objects.filter(
            student=profile.child,
            session__is_finalized=True
        ).select_related('session__slot').order_by('-session__date')[:10]

    return render(request, 'accounts/parent_dashboard.html', {
        'profile': profile,
        'child_summaries': child_summaries,
        'recent_sessions': recent_sessions,
    })


@login_required
def admin_dashboard(request):
    if request.user.role != 'admin':
        return redirect('dashboard')

    from accounts.models import StudentProfile, FacultyProfile, ParentProfile
    from attendance.models import AttendanceSummary, AttendanceSession
    from notes.models import Note

    total_students = StudentProfile.objects.count()
    total_faculty  = FacultyProfile.objects.count()
    total_parents  = ParentProfile.objects.count()
    total_notes    = Note.objects.filter(is_active=True).count()

    # Students with attendance shortage (< 75%)
    all_summaries = AttendanceSummary.objects.select_related('student__user')
    shortage_students = []
    seen = set()
    for s in all_summaries:
        if s.is_shortage and s.student_id not in seen:
            shortage_students.append(s.student)
            seen.add(s.student_id)

    recent_sessions = AttendanceSession.objects.select_related(
        'slot', 'marked_by'
    ).order_by('-date', '-created_at')[:10]

    recent_notes = Note.objects.select_related('uploaded_by').order_by('-uploaded_at')[:5]

    students = StudentProfile.objects.select_related('user').order_by('enroll_no')

    return render(request, 'accounts/admin_dashboard.html', {
        'total_students':   total_students,
        'total_faculty':    total_faculty,
        'total_parents':    total_parents,
        'total_notes':      total_notes,
        'shortage_students': shortage_students,
        'recent_sessions':  recent_sessions,
        'recent_notes':     recent_notes,
        'students':         students,
    })
