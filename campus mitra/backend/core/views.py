from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.db.models import Q

from .models import (User, Student, Faculty, Parent, Department,
                     Subject, Timetable, Attendance, Note, Announcement,
                     Assignment, AssignmentSubmission)
from .serializers import (UserSerializer, StudentSerializer, FacultySerializer,
                          SubjectSerializer, TimetableSerializer, AttendanceSerializer,
                          NoteSerializer, AnnouncementSerializer, DepartmentSerializer,
                          AssignmentSerializer, AssignmentSubmissionSerializer)
from .permissions import IsFaculty, IsStudent, IsParent, IsAdminUser, IsFacultyOrAdmin


# ── Auth ──────────────────────────────────────────────────────────────────────

class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get('email', '').strip().lower()
        password = request.data.get('password', '').strip()
        if not email or not password:
            return Response({'error': 'Email and password are required.'}, status=400)
        user = authenticate(request, username=email, password=password)
        if not user:
            return Response({'error': 'Invalid credentials. Please check your email and password.'}, status=400)
        if not user.is_active:
            return Response({'error': 'Your account has been deactivated. Contact admin.'}, status=403)
        refresh = RefreshToken.for_user(user)
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
    """POST /api/attendance/mark/ — faculty marks attendance"""
    permission_classes = [IsFaculty]

    def post(self, request):
        records = request.data.get('records', [])
        if not records:
            return Response({'error': 'No records provided.'}, status=400)
        count = 0
        errors = []
        for r in records:
            try:
                # student_id is the DB Student.id (integer)
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
    """GET /api/attendance/my/ — student views subject-wise attendance"""
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
    """GET /api/attendance/subject/<id>/ — faculty views attendance for a subject"""
    permission_classes = [IsFaculty]

    def get(self, request, subject_id):
        try:
            subject = Subject.objects.get(pk=subject_id)
        except Subject.DoesNotExist:
            return Response({'error': 'Subject not found.'}, status=404)
        records = Attendance.objects.filter(subject=subject).select_related('student__user')
        return Response(AttendanceSerializer(records, many=True, context={'request': request}).data)


# ── Notes ─────────────────────────────────────────────────────────────────────

class NoteUploadView(generics.CreateAPIView):
    """POST /api/notes/upload/ — faculty uploads a note (multipart)"""
    serializer_class = NoteSerializer
    permission_classes = [IsFaculty]
    parser_classes = [MultiPartParser, FormParser]

    def perform_create(self, serializer):
        serializer.save(uploaded_by=self.request.user.faculty)

    def get_serializer_context(self):
        return {'request': self.request}


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

    def get_serializer_context(self):
        return {'request': self.request}


class FacultyNoteListView(generics.ListAPIView):
    """GET /api/notes/my/ — faculty lists their own uploaded notes"""
    serializer_class = NoteSerializer
    permission_classes = [IsFaculty]

    def get_queryset(self):
        return Note.objects.filter(
            uploaded_by=self.request.user.faculty
        ).order_by('-uploaded_at')

    def get_serializer_context(self):
        return {'request': self.request}


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

    def get_serializer_context(self):
        return {'request': self.request}


class AssignmentCreateView(generics.CreateAPIView):
    """POST /api/assignments/create/ — faculty creates an assignment"""
    serializer_class = AssignmentSerializer
    permission_classes = [IsFaculty]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def perform_create(self, serializer):
        serializer.save(uploaded_by=self.request.user.faculty)

    def get_serializer_context(self):
        return {'request': self.request}


class FacultyAssignmentListView(generics.ListAPIView):
    """GET /api/assignments/my/ — faculty lists their own assignments"""
    serializer_class = AssignmentSerializer
    permission_classes = [IsFaculty]

    def get_queryset(self):
        return Assignment.objects.filter(
            uploaded_by=self.request.user.faculty
        ).order_by('-created_at')

    def get_serializer_context(self):
        return {'request': self.request}


class AssignmentSubmitView(APIView):
    """POST /api/assignments/<id>/submit/ — student submits an assignment"""
    permission_classes = [IsStudent]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, assignment_id):
        try:
            assignment = Assignment.objects.get(pk=assignment_id)
        except Assignment.DoesNotExist:
            return Response({'error': 'Assignment not found.'}, status=404)

        student = request.user.student
        file = request.FILES.get('file')
        if not file:
            return Response({'error': 'No file provided.'}, status=400)

        # Validate file type
        allowed = ['.pdf', '.doc', '.docx', '.ppt', '.pptx']
        import os
        ext = os.path.splitext(file.name)[1].lower()
        if ext not in allowed:
            return Response({'error': f'File type {ext} not allowed. Use PDF, DOC, DOCX, PPT, or PPTX.'}, status=400)

        submission, created = AssignmentSubmission.objects.update_or_create(
            assignment=assignment,
            student=student,
            defaults={'file': file, 'remarks': request.data.get('remarks', '')}
        )
        action = 'submitted' if created else 'resubmitted'
        return Response({
            'status': action,
            'assignment': assignment.title,
            'submitted_at': submission.submitted_at.isoformat(),
        })


class AssignmentSubmissionsView(generics.ListAPIView):
    """GET /api/assignments/<id>/submissions/ — faculty views all submissions"""
    serializer_class = AssignmentSubmissionSerializer
    permission_classes = [IsFaculty]

    def get_queryset(self):
        return AssignmentSubmission.objects.filter(
            assignment_id=self.kwargs['assignment_id']
        ).select_related('student__user')

    def get_serializer_context(self):
        return {'request': self.request}


class StudentSubmissionsView(generics.ListAPIView):
    """GET /api/assignments/my-submissions/ — student views their own submissions"""
    serializer_class = AssignmentSubmissionSerializer
    permission_classes = [IsStudent]

    def get_queryset(self):
        return AssignmentSubmission.objects.filter(
            student=self.request.user.student
        ).select_related('assignment')

    def get_serializer_context(self):
        return {'request': self.request}


# ── Announcements ─────────────────────────────────────────────────────────────

class AnnouncementListView(generics.ListAPIView):
    serializer_class = AnnouncementSerializer

    def get_queryset(self):
        role = self.request.user.role
        audience_map = {
            'student': 'students', 'faculty': 'faculty',
            'parent': 'parents', 'admin': 'all',
        }
        target = audience_map.get(role, 'all')
        qs = Announcement.objects.filter(Q(audience='all') | Q(audience=target))
        if hasattr(self.request.user, 'student'):
            dept = self.request.user.student.department
            qs = qs.filter(Q(department__isnull=True) | Q(department=dept))
        elif hasattr(self.request.user, 'faculty'):
            dept = self.request.user.faculty.department
            qs = qs.filter(Q(department__isnull=True) | Q(department=dept))
        return qs.order_by('-created_at')


class AnnouncementCreateView(generics.CreateAPIView):
    serializer_class = AnnouncementSerializer
    permission_classes = [IsFacultyOrAdmin]

    def perform_create(self, serializer):
        dept = None
        if hasattr(self.request.user, 'faculty'):
            dept = self.request.user.faculty.department
        serializer.save(posted_by=self.request.user, department=dept)


# ── Timetable ─────────────────────────────────────────────────────────────────

class TimetableView(APIView):
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
    serializer_class = SubjectSerializer

    def get_queryset(self):
        user = self.request.user
        dept = self.request.query_params.get('dept')
        if hasattr(user, 'student'):
            s = user.student
            return Subject.objects.filter(department=s.department, semester=s.semester)
        elif hasattr(user, 'faculty'):
            # Faculty can query any branch (for cross-branch teaching)
            if dept:
                return Subject.objects.filter(department__code=dept)
            return Subject.objects.filter(department=user.faculty.department)
        if dept:
            return Subject.objects.filter(department__code=dept)
        return Subject.objects.all()


# ── Faculty ───────────────────────────────────────────────────────────────────

class StudentFacultyListView(generics.ListAPIView):
    serializer_class = FacultySerializer
    permission_classes = [IsStudent]

    def get_queryset(self):
        student = self.request.user.student
        return Faculty.objects.filter(department=student.department)


# ── Students (for faculty attendance) ────────────────────────────────────────

class FacultyStudentListView(generics.ListAPIView):
    """GET /api/students/by-dept/?dept=AIML — faculty gets student list for attendance"""
    serializer_class = StudentSerializer
    permission_classes = [IsFaculty]

    def get_queryset(self):
        dept = self.request.query_params.get('dept', '')
        if dept:
            return Student.objects.filter(
                department__code=dept
            ).select_related('user', 'department').order_by('enrollment_no')
        return Student.objects.filter(
            department=self.request.user.faculty.department
        ).select_related('user', 'department').order_by('enrollment_no')


class FacultyStatsView(APIView):
    """GET /api/faculty/stats/ — real-time stats for faculty dashboard hero"""
    permission_classes = [IsFaculty]

    def get(self, request):
        faculty = request.user.faculty
        dept = faculty.department

        # Notes uploaded by this faculty
        notes_count = Note.objects.filter(uploaded_by=faculty).count()

        # Students in this department
        students_count = Student.objects.filter(department=dept).count()

        # Assignments created by this faculty
        assignments_count = Assignment.objects.filter(uploaded_by=faculty).count()

        # Average attendance across all subjects taught by this faculty
        subjects = Subject.objects.filter(faculty=faculty)
        avg_att = 0
        if subjects.exists():
            total_pct = 0
            sub_count = 0
            for sub in subjects:
                total = Attendance.objects.filter(subject=sub).count()
                present = Attendance.objects.filter(subject=sub, status='P').count()
                if total > 0:
                    total_pct += round((present / total * 100), 1)
                    sub_count += 1
            avg_att = round(total_pct / sub_count, 1) if sub_count else 0

        return Response({
            'notes_uploaded': notes_count,
            'students_count': students_count,
            'assignments_count': assignments_count,
            'avg_attendance': avg_att,
            'subjects_count': subjects.count(),
        })


class FacultyStudentAttendanceView(APIView):
    """GET /api/students/attendance/?dept=AIML — faculty views student list with attendance"""
    permission_classes = [IsFaculty]

    def get(self, request):
        dept_code = request.query_params.get('dept', '')
        faculty = request.user.faculty
        dept = faculty.department

        if dept_code:
            students = Student.objects.filter(
                department__code=dept_code
            ).select_related('user', 'department')
        else:
            students = Student.objects.filter(
                department=dept
            ).select_related('user', 'department')

        data = []
        for s in students:
            total = Attendance.objects.filter(student=s).count()
            present = Attendance.objects.filter(student=s, status='P').count()
            pct = round((present / total * 100), 1) if total else 0
            data.append({
                'id': s.id,
                'name': s.user.get_full_name(),
                'enrollment_no': s.enrollment_no,
                'department': s.department.name if s.department else '',
                'branch_code': s.department.code if s.department else '',
                'attendance_pct': pct,
                'shortage': pct < 75,
                'total_classes': total,
                'present': present,
            })
        return Response(data)


# ── Parent ────────────────────────────────────────────────────────────────────

class ParentChildView(APIView):
    permission_classes = [IsParent]

    def get(self, request):
        children = Student.objects.filter(parent=request.user.parent)
        return Response(StudentSerializer(children, many=True).data)


# ── Departments ───────────────────────────────────────────────────────────────

class DepartmentListView(generics.ListAPIView):
    serializer_class = DepartmentSerializer
    permission_classes = [permissions.AllowAny]
    queryset = Department.objects.all()


# ── Admin ─────────────────────────────────────────────────────────────────────

class UserListView(generics.ListCreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]
    queryset = User.objects.all()


class AttendanceAlertView(APIView):
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
    serializer_class = StudentSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        dept = self.request.query_params.get('dept')
        qs = Student.objects.select_related('user', 'department').all()
        if dept:
            qs = qs.filter(department__code=dept)
        return qs


class AdminFacultyListView(generics.ListAPIView):
    serializer_class = FacultySerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        dept = self.request.query_params.get('dept')
        qs = Faculty.objects.select_related('user', 'department').all()
        if dept:
            qs = qs.filter(department__code=dept)
        return qs
