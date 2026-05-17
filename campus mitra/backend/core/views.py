from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.db.models import Q

from .models import (User, Student, Faculty, Parent, Department,
                     Subject, Timetable, Attendance, Note, Announcement, Assignment)
from .serializers import (UserSerializer, StudentSerializer, FacultySerializer,
                          SubjectSerializer, TimetableSerializer, AttendanceSerializer,
                          NoteSerializer, AnnouncementSerializer, DepartmentSerializer, AssignmentSerializer)
from .permissions import IsFaculty, IsStudent, IsParent, IsAdminUser, IsFacultyOrAdmin


# ── Auth ──────────────────────────────────────────────────────────────────────

class LoginView(APIView):
    """
    POST /api/auth/login/
    Body: { "email": "...", "password": "..." }
    Returns: { access, refresh, role, name, department, branch_code }
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get('email', '').strip().lower()
        password = request.data.get('password', '').strip()

        if not email or not password:
            return Response({'error': 'Email and password are required.'}, status=400)

        # Django's authenticate uses username field; our users have email == username
        user = authenticate(request, username=email, password=password)

        if not user:
            return Response({'error': 'Invalid credentials. Please check your email and password.'}, status=400)

        if not user.is_active:
            return Response({'error': 'Your account has been deactivated. Contact admin.'}, status=403)

        refresh = RefreshToken.for_user(user)

        # Build role-specific extra info
        extra = {}
        if hasattr(user, 'student'):
            s = user.student
            extra['enrollment_no'] = s.enrollment_no
            extra['semester'] = s.semester
            extra['section'] = s.section
            if s.department:
                extra['department'] = s.department.name
                extra['branch_code'] = s.department.code
        elif hasattr(user, 'faculty'):
            f = user.faculty
            extra['faculty_id'] = f.faculty_id
            extra['designation'] = f.designation
            if f.department:
                extra['department'] = f.department.name
                extra['branch_code'] = f.department.code
        elif hasattr(user, 'parent'):
            children = Student.objects.filter(parent=user.parent)
            extra['children'] = [
                {'name': c.user.get_full_name(), 'enrollment_no': c.enrollment_no}
                for c in children
            ]

        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'role': user.role,
            'name': user.get_full_name(),
            'email': user.email,
            **extra,
        })


class MeView(APIView):
    """GET /api/auth/me/ — returns current user profile"""

    def get(self, request):
        user = request.user
        data = UserSerializer(user).data
        if hasattr(user, 'student'):
            data['profile'] = StudentSerializer(user.student).data
        elif hasattr(user, 'faculty'):
            data['profile'] = FacultySerializer(user.faculty).data
        return Response(data)


# ── Attendance ────────────────────────────────────────────────────────────────

class MarkAttendanceView(APIView):
    """
    POST /api/attendance/mark/
    Faculty marks attendance for a class.
    Body: { "records": [{ "student": id, "subject": id, "date": "YYYY-MM-DD", "status": "P/A/L" }] }
    """
    permission_classes = [IsFaculty]

    def post(self, request):
        records = request.data.get('records', [])
        if not records:
            return Response({'error': 'No records provided.'}, status=400)

        count = 0
        errors = []
        for r in records:
            try:
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
            except Exception as e:
                errors.append(str(e))

        return Response({'marked': count, 'errors': errors})


class StudentAttendanceView(APIView):
    """GET /api/attendance/my/ — student views their subject-wise attendance"""
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
                'shortage': pct < 75,
            })
        return Response(data)


class AttendanceBySubjectView(APIView):
    """
    GET /api/attendance/subject/<subject_id>/
    Faculty views attendance for a specific subject.
    """
    permission_classes = [IsFaculty]

    def get(self, request, subject_id):
        try:
            subject = Subject.objects.get(pk=subject_id)
        except Subject.DoesNotExist:
            return Response({'error': 'Subject not found.'}, status=404)

        records = Attendance.objects.filter(subject=subject).select_related('student__user')
        return Response(AttendanceSerializer(records, many=True).data)


# ── Notes ─────────────────────────────────────────────────────────────────────

class NoteUploadView(generics.CreateAPIView):
    """POST /api/notes/upload/ — faculty uploads a note"""
    serializer_class = NoteSerializer
    permission_classes = [IsFaculty]

    def perform_create(self, serializer):
        serializer.save(uploaded_by=self.request.user.faculty)


class NoteListView(generics.ListAPIView):
    """GET /api/notes/ — student lists notes for their dept/semester"""
    serializer_class = NoteSerializer
    permission_classes = [IsStudent]

    def get_queryset(self):
        student = self.request.user.student
        return Note.objects.filter(
            subject__department=student.department,
            subject__semester=student.semester
        ).order_by('-uploaded_at')


# ── Assignments ───────────────────────────────────────────────────────────────

class AssignmentListView(generics.ListAPIView):
    """GET /api/assignments/ — student lists assignments for their dept/semester"""
    serializer_class = AssignmentSerializer
    permission_classes = [IsStudent]

    def get_queryset(self):
        student = self.request.user.student
        return Assignment.objects.filter(
            subject__department=student.department,
            subject__semester=student.semester
        ).order_by('deadline')


# ── Announcements ─────────────────────────────────────────────────────────────

class AnnouncementListView(generics.ListAPIView):
    """GET /api/announcements/ — role-filtered announcements"""
    serializer_class = AnnouncementSerializer

    def get_queryset(self):
        role = self.request.user.role
        # 'all' audience is visible to everyone; role-specific ones filter by role
        audience_map = {
            'student': 'students',
            'faculty': 'faculty',
            'parent': 'parents',
            'admin': 'all',
        }
        target = audience_map.get(role, 'all')
        
        qs = Announcement.objects.filter(
            Q(audience='all') | Q(audience=target)
        )
        
        if hasattr(self.request.user, 'student'):
            dept = self.request.user.student.department
            qs = qs.filter(Q(department__isnull=True) | Q(department=dept))
        elif hasattr(self.request.user, 'faculty'):
            dept = self.request.user.faculty.department
            qs = qs.filter(Q(department__isnull=True) | Q(department=dept))

        return qs.order_by('-created_at')


class AnnouncementCreateView(generics.CreateAPIView):
    """POST /api/announcements/new/ — faculty or admin posts announcement"""
    serializer_class = AnnouncementSerializer
    permission_classes = [IsFacultyOrAdmin]

    def perform_create(self, serializer):
        serializer.save(posted_by=self.request.user)


# ── Timetable ─────────────────────────────────────────────────────────────────

class TimetableView(APIView):
    """GET /api/timetable/ — student or faculty views their timetable"""

    def get(self, request):
        user = request.user
        if hasattr(user, 'student'):
            s = user.student
            slots = Timetable.objects.filter(
                department=s.department, section=s.section
            ).select_related('subject', 'department')
        elif hasattr(user, 'faculty'):
            slots = Timetable.objects.filter(
                subject__faculty=user.faculty
            ).select_related('subject', 'department')
        else:
            slots = Timetable.objects.all().select_related('subject', 'department')
        return Response(TimetableSerializer(slots, many=True).data)


# ── Subjects ──────────────────────────────────────────────────────────────────

class SubjectListView(generics.ListAPIView):
    """GET /api/subjects/ — list subjects (filtered by dept/semester for students)"""
    serializer_class = SubjectSerializer

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'student'):
            s = user.student
            return Subject.objects.filter(department=s.department, semester=s.semester)
        elif hasattr(user, 'faculty'):
            return Subject.objects.filter(faculty=user.faculty)
        return Subject.objects.all()


# ── Faculty ───────────────────────────────────────────────────────────────────

class StudentFacultyListView(generics.ListAPIView):
    """GET /api/faculty/my/ — student lists faculty for their dept"""
    serializer_class = FacultySerializer
    permission_classes = [IsStudent]

    def get_queryset(self):
        student = self.request.user.student
        return Faculty.objects.filter(department=student.department)


# ── Parent ────────────────────────────────────────────────────────────────────

class ParentChildView(APIView):
    """GET /api/parent/children/ — parent views their child's profile"""
    permission_classes = [IsParent]

    def get(self, request):
        children = Student.objects.filter(parent=request.user.parent)
        return Response(StudentSerializer(children, many=True).data)


# ── Departments ───────────────────────────────────────────────────────────────

class DepartmentListView(generics.ListAPIView):
    """GET /api/departments/ — list all departments"""
    serializer_class = DepartmentSerializer
    permission_classes = [permissions.AllowAny]
    queryset = Department.objects.all()


# ── Admin ─────────────────────────────────────────────────────────────────────

class UserListView(generics.ListCreateAPIView):
    """GET/POST /api/admin/users/ — admin manages users"""
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]
    queryset = User.objects.all()


class AttendanceAlertView(APIView):
    """GET /api/admin/alerts/ — students below 75% attendance"""
    permission_classes = [IsAdminUser]

    def get(self, request):
        students = Student.objects.select_related('user', 'department').all()
        alerts = []
        for s in students:
            total = Attendance.objects.filter(student=s).count()
            present = Attendance.objects.filter(student=s, status='P').count()
            pct = round((present / total * 100), 1) if total else 0
            if pct < 75:
                alerts.append({
                    'student': s.user.get_full_name(),
                    'enrollment': s.enrollment_no,
                    'department': s.department.name if s.department else '',
                    'percentage': pct,
                })
        return Response(alerts)


class AdminStudentListView(generics.ListAPIView):
    """GET /api/admin/students/?dept=AIML — admin lists students by dept"""
    serializer_class = StudentSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        dept = self.request.query_params.get('dept')
        qs = Student.objects.select_related('user', 'department').all()
        if dept:
            qs = qs.filter(department__code=dept)
        return qs


class AdminFacultyListView(generics.ListAPIView):
    """GET /api/admin/faculty/?dept=AIML — admin lists faculty by dept"""
    serializer_class = FacultySerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        dept = self.request.query_params.get('dept')
        qs = Faculty.objects.select_related('user', 'department').all()
        if dept:
            qs = qs.filter(department__code=dept)
        return qs
