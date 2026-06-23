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
        note = serializer.save(uploaded_by=self.request.user.faculty)
        # Auto-index the note for RAG
        try:
            from .rag_utils import index_note
            count = index_note(note)
            print(f'[RAG] Indexed {count} chunks for note: {note.title}')
        except Exception as e:
            print(f'[RAG] Indexing failed: {e}')

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


class ParentChildDetailView(APIView):
    """GET /api/parent/child-detail/ — full child data: profile, attendance, assignments, announcements"""
    permission_classes = [IsParent]

    def get(self, request):
        children = Student.objects.filter(
            parent=request.user.parent
        ).select_related('user', 'department')

        if not children.exists():
            return Response({'error': 'No linked student found.'}, status=404)

        result = []
        for student in children:
            # Subject-wise attendance
            subjects = Subject.objects.filter(
                department=student.department,
                semester=student.semester
            ).select_related('faculty__user')

            attendance = []
            for sub in subjects:
                total   = Attendance.objects.filter(student=student, subject=sub).count()
                present = Attendance.objects.filter(student=student, subject=sub, status='P').count()
                pct     = round((present / total * 100), 1) if total else 0
                attendance.append({
                    'subject':    sub.name,
                    'code':       sub.code,
                    'faculty':    sub.faculty.user.get_full_name() if sub.faculty else '',
                    'total':      total,
                    'present':    present,
                    'percentage': pct,
                    'shortage':   pct < 75,
                })

            # Assignments (pending / submitted status)
            assignments_qs = Assignment.objects.filter(
                subject__department=student.department,
                subject__semester=student.semester
            ).order_by('deadline')
            submitted_ids = set(
                AssignmentSubmission.objects.filter(
                    student=student
                ).values_list('assignment_id', flat=True)
            )
            assignments_data = [{
                'id':        a.id,
                'title':     a.title,
                'subject':   a.subject.name,
                'deadline':  a.deadline.isoformat(),
                'submitted': a.id in submitted_ids,
            } for a in assignments_qs]

            # Announcements visible to parents/all for this branch
            ann_qs = Announcement.objects.filter(
                Q(audience='all') | Q(audience='students') | Q(audience='parents')
            ).filter(
                Q(department__isnull=True) | Q(department=student.department)
            ).order_by('-created_at')[:15]
            ann_data = [{
                'title':          a.title,
                'content':        a.content,
                'urgency':        a.urgency,
                'posted_by_name': a.posted_by.get_full_name(),
                'created_at':     a.created_at.isoformat(),
            } for a in ann_qs]

            result.append({
                'student': {
                    'id':            student.id,
                    'name':          student.user.get_full_name(),
                    'email':         student.user.email,
                    'enrollment_no': student.enrollment_no,
                    'semester':      student.semester,
                    'section':       student.section,
                    'cgpa':          str(student.cgpa),
                    'department':    student.department.name if student.department else '',
                    'branch_code':   student.department.code if student.department else '',
                },
                'subjects':      [{'name': s.name, 'code': s.code,
                                   'faculty': s.faculty.user.get_full_name() if s.faculty else ''}
                                  for s in subjects],
                'attendance':    attendance,
                'assignments':   assignments_data,
                'announcements': ann_data,
            })

        return Response(result)


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


class AdminStatsView(APIView):
    """GET /api/admin/stats/ — system-wide stats for dashboard hero"""
    permission_classes = [IsAdminUser]

    def get(self, request):
        total_students   = Student.objects.count()
        total_faculty    = Faculty.objects.count()
        total_parents    = Parent.objects.count()
        total_attendance = Attendance.objects.count()
        total_notes      = Note.objects.count()
        total_assignments = Assignment.objects.count()
        total_announcements = Announcement.objects.count()

        # Branch-wise student count
        from django.db.models import Count
        branch_counts = list(
            Student.objects.values('department__code', 'department__name')
            .annotate(count=Count('id'))
            .order_by('department__code')
        )

        # Attendance alerts count
        alerts_count = 0
        for s in Student.objects.all():
            total = Attendance.objects.filter(student=s).count()
            present = Attendance.objects.filter(student=s, status='P').count()
            pct = round((present / total * 100), 1) if total else 0
            if 0 < pct < 75:
                alerts_count += 1

        return Response({
            'students':     total_students,
            'faculty':      total_faculty,
            'parents':      total_parents,
            'attendance_records': total_attendance,
            'notes':        total_notes,
            'assignments':  total_assignments,
            'announcements': total_announcements,
            'alerts':       alerts_count,
            'branch_counts': branch_counts,
        })


class AdminUserCreateView(APIView):
    """POST /api/admin/users/create/ — admin creates a new user"""
    permission_classes = [IsAdminUser]

    def post(self, request):
        role        = request.data.get('role', 'student')
        first_name  = request.data.get('first_name', '').strip()
        last_name   = request.data.get('last_name', '').strip()
        email       = request.data.get('email', '').strip().lower()
        password    = request.data.get('password', f"{first_name.lower()}@123")
        dept_code   = request.data.get('department', '')

        if not email or not first_name:
            return Response({'error': 'Email and first name are required.'}, status=400)

        if User.objects.filter(username=email).exists():
            return Response({'error': 'A user with this email already exists.'}, status=400)

        user = User.objects.create(
            username=email, email=email,
            first_name=first_name, last_name=last_name,
            role=role
        )
        user.set_password(password)
        user.save()

        # Create role-specific profile
        dept = None
        if dept_code:
            try:
                dept = Department.objects.get(code=dept_code)
            except Department.DoesNotExist:
                pass

        if role == 'student':
            enroll = request.data.get('enrollment_no', f"TEMP{user.id:04d}")
            sem    = request.data.get('semester', 6)
            Student.objects.create(
                user=user, enrollment_no=enroll,
                department=dept, semester=sem
            )
        elif role == 'faculty':
            fac_id = request.data.get('faculty_id', f"FAC-TEMP-{user.id:04d}")
            desig  = request.data.get('designation', 'Assistant Professor')
            Faculty.objects.create(
                user=user, faculty_id=fac_id,
                department=dept, designation=desig
            )
        elif role == 'parent':
            Parent.objects.create(user=user)

        return Response({
            'id':       user.id,
            'username': user.username,
            'name':     user.get_full_name(),
            'role':     user.role,
            'password': password,
            'message':  f'User {user.get_full_name()} created successfully.',
        }, status=201)


class AdminUserUpdateView(APIView):
    """PATCH /api/admin/users/<id>/ — admin updates a user"""
    permission_classes = [IsAdminUser]

    def patch(self, request, user_id):
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found.'}, status=404)

        for field in ['first_name', 'last_name', 'email', 'role']:
            if field in request.data:
                setattr(user, field, request.data[field])
        if 'password' in request.data:
            user.set_password(request.data['password'])
        if 'is_active' in request.data:
            user.is_active = request.data['is_active']
        user.save()
        return Response({'message': f'User {user.get_full_name()} updated.', 'id': user.id})


class AdminUserDeleteView(APIView):
    """DELETE /api/admin/users/<id>/ — admin deactivates a user"""
    permission_classes = [IsAdminUser]

    def delete(self, request, user_id):
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found.'}, status=404)
        name = user.get_full_name()
        user.is_active = False  # soft delete
        user.save()
        return Response({'message': f'User {name} deactivated.'})


class AdminAttendanceSummaryView(APIView):
    """GET /api/admin/attendance/summary/ — dept-wise attendance summary"""
    permission_classes = [IsAdminUser]

    def get(self, request):
        dept_code = request.query_params.get('dept')
        result = []

        depts = Department.objects.all()
        if dept_code:
            depts = depts.filter(code=dept_code)

        for dept in depts:
            students = Student.objects.filter(department=dept)
            total_att = 0
            count = 0
            below75 = 0
            for s in students:
                t = Attendance.objects.filter(student=s).count()
                p = Attendance.objects.filter(student=s, status='P').count()
                if t > 0:
                    pct = round(p / t * 100, 1)
                    total_att += pct
                    count += 1
                    if pct < 75:
                        below75 += 1
            result.append({
                'department':    dept.name,
                'code':          dept.code,
                'students':      students.count(),
                'avg_attendance': round(total_att / count, 1) if count else 0,
                'below_75':      below75,
            })
        return Response(result)


# ── AI Agent ──────────────────────────────────────────────────────────────────

class AIQueryView(APIView):
    """
    POST /api/ai/query/
    Body: { "message": "What is my attendance in CN?" }
    Returns context-aware answers using real student/faculty data.
    No external AI API needed — rule-based NLP with real DB data.
    """

    def post(self, request):
        message = request.data.get('message', '').strip().lower()
        user    = request.user

        if not message:
            return Response({'reply': 'Please ask me something!'})

        # ── Gather context based on role ──────────────────────────────────────
        context = {}
        role    = user.role
        notes_qs = None   # queryset of notes accessible to this user

        if hasattr(user, 'student'):
            student = user.student
            context['name']    = user.get_full_name()
            context['branch']  = student.department.code if student.department else ''
            context['sem']     = student.semester
            context['enroll']  = student.enrollment_no
            context['role']    = 'student'

            # Notes queryset for RAG
            notes_qs = Note.objects.filter(
                subject__department=student.department,
                subject__semester=student.semester
            )

            # Attendance data
            subjects = Subject.objects.filter(department=student.department, semester=student.semester)
            att_data = []
            for sub in subjects:
                total   = Attendance.objects.filter(student=student, subject=sub).count()
                present = Attendance.objects.filter(student=student, subject=sub, status='P').count()
                pct     = round((present / total * 100), 1) if total else 0
                att_data.append({'subject': sub.name, 'code': sub.code, 'pct': pct, 'total': total, 'present': present})
            context['attendance'] = att_data

            # Notes metadata
            notes = notes_qs.order_by('-uploaded_at')[:10]
            context['notes'] = [{'title': n.title, 'subject': n.subject.name, 'date': n.uploaded_at.strftime('%d %b')} for n in notes]

            # Assignments
            assignments = Assignment.objects.filter(subject__department=student.department, subject__semester=student.semester).order_by('deadline')
            submitted_ids = set(AssignmentSubmission.objects.filter(student=student).values_list('assignment_id', flat=True))
            context['assignments'] = [{'title': a.title, 'subject': a.subject.name, 'deadline': a.deadline.strftime('%d %b %Y'), 'submitted': a.id in submitted_ids} for a in assignments]

            # Announcements
            ann = Announcement.objects.filter(
                Q(audience='all') | Q(audience='students')
            ).filter(Q(department__isnull=True) | Q(department=student.department)).order_by('-created_at')[:5]
            context['announcements'] = [{'title': a.title, 'urgency': a.urgency, 'date': a.created_at.strftime('%d %b')} for a in ann]

        elif hasattr(user, 'faculty'):
            faculty = user.faculty
            context['name']   = user.get_full_name()
            context['branch'] = faculty.department.code if faculty.department else ''
            context['fid']    = faculty.faculty_id
            context['role']   = 'faculty'

            # Notes queryset for RAG
            notes_qs = Note.objects.filter(uploaded_by=faculty)

            # Subjects taught
            subjects = Subject.objects.filter(faculty=faculty)
            context['subjects'] = [{'name': s.name, 'code': s.code} for s in subjects]

            # Students in dept
            context['student_count'] = Student.objects.filter(department=faculty.department).count()

            # My assignments
            assignments = Assignment.objects.filter(uploaded_by=faculty).order_by('-created_at')[:5]
            context['assignments'] = [{'title': a.title, 'subject': a.subject.name, 'deadline': a.deadline.strftime('%d %b %Y'), 'submissions': a.submissions.count()} for a in assignments]

            # My notes
            notes = notes_qs.order_by('-uploaded_at')[:5]
            context['notes'] = [{'title': n.title, 'subject': n.subject.name, 'date': n.uploaded_at.strftime('%d %b')} for n in notes]

            # Announcements
            ann = Announcement.objects.filter(Q(audience='all') | Q(audience='faculty')).filter(
                Q(department__isnull=True) | Q(department=faculty.department)
            ).order_by('-created_at')[:5]
            context['announcements'] = [{'title': a.title, 'urgency': a.urgency, 'date': a.created_at.strftime('%d %b')} for a in ann]

        # ── Check if this is a RAG/content question ───────────────────────────
        rag_triggers = [
            'explain', 'what is', 'define', 'describe', 'how does', 'how do',
            'tell me about', 'summarize', 'summary', 'concept', 'theory',
            'algorithm', 'formula', 'law', 'theorem', 'process', 'difference',
            'compare', 'example', 'type', 'classify', 'derivation', 'proof',
            'meaning', 'definition', 'work', 'calculate', 'solve', 'write about'
        ]
        is_rag_query = notes_qs is not None and any(t in message for t in rag_triggers)

        # Also trigger RAG if message mentions a subject topic not covered by rules
        rule_keywords = ['attendance', 'present', 'absent', 'note', 'material', 'pdf',
                         'assignment', 'homework', 'due', 'deadline', 'announcement',
                         'notice', 'circular', 'timetable', 'schedule', 'cgpa', 'marks',
                         'result', 'hi', 'hello', 'hey', 'help', 'faculty', 'teacher',
                         'branch', 'department']
        hits_rule = any(k in message for k in rule_keywords)
        if not hits_rule and notes_qs is not None and notes_qs.exists():
            is_rag_query = True  # unknown query → try RAG

        if is_rag_query and notes_qs is not None:
            from .rag_utils import retrieve_chunks, ask_gemini
            chunks = retrieve_chunks(message, notes_qs, top_k=4)
            if chunks:
                answer = ask_gemini(
                    question=message,
                    context_chunks=chunks,
                    user_name=context.get('name', '').split()[0],
                    role=role
                )
                return Response({'reply': answer, 'role': role, 'rag': True})

        # ── Rule-based answer engine ──────────────────────────────────────────
        reply = self._answer(message, context, role)
        return Response({'reply': reply, 'role': role})

    def _answer(self, msg, ctx, role):
        name   = ctx.get('name', 'you').split()[0]
        branch = ctx.get('branch', '')

        # ── ATTENDANCE queries ────────────────────────────────────────────────
        if any(w in msg for w in ['attendance', 'present', 'absent', 'percentage', '%', 'shortag', 'below 75', 'shortage']):
            att = ctx.get('attendance', [])
            if not att:
                return f"Hi {name}! I don't have attendance data for you yet. Faculty will mark attendance and it'll appear here."

            if role == 'student':
                # Check for specific subject
                for sub in att:
                    if sub['code'].lower() in msg or sub['subject'].lower().split()[0] in msg:
                        pct   = sub['pct']
                        color = '🟢' if pct >= 80 else '🟡' if pct >= 75 else '🔴'
                        warn  = ' ⚠️ You are below 75% — attend more classes!' if pct < 75 else (' ✅ Good attendance!' if pct >= 80 else ' 🟡 Just above 75%, be careful.')
                        return f"{color} **{sub['subject']} ({sub['code']})** — {pct}% attendance ({sub['present']}/{sub['total']} classes){warn}"

                # Overall summary
                if not att:
                    return "No attendance data found yet."
                avg      = round(sum(s['pct'] for s in att) / len(att), 1)
                shortage = [s for s in att if s['pct'] < 75]
                lines    = [f"📊 **Your Attendance Summary, {name}:**\n"]
                for s in att:
                    icon = '🟢' if s['pct'] >= 80 else '🟡' if s['pct'] >= 75 else '🔴'
                    lines.append(f"{icon} {s['subject']} ({s['code']}): **{s['pct']}%**")
                lines.append(f"\n📈 Overall Average: **{avg}%**")
                if shortage:
                    lines.append(f"\n⚠️ Shortage in: {', '.join(s['code'] for s in shortage)} — below 75%!")
                return '\n'.join(lines)

        # ── NOTES queries ─────────────────────────────────────────────────────
        if any(w in msg for w in ['note', 'material', 'pdf', 'upload', 'download', 'study', 'resource', 'file']):
            notes = ctx.get('notes', [])
            if not notes:
                return f"Hi {name}! No study materials have been uploaded yet for your branch. Check back after your faculty uploads notes."
            lines = [f"📚 **Study Materials for {branch}:**\n"]
            for n in notes:
                lines.append(f"📄 **{n['title']}** — {n.get('subject','')} ({n.get('date','')})")
            if role == 'student':
                lines.append("\n➡️ Go to **Study Materials** section to download them.")
            else:
                lines.append("\n➡️ Go to **Upload Notes** section to add more.")
            return '\n'.join(lines)

        # ── ASSIGNMENT queries ────────────────────────────────────────────────
        if any(w in msg for w in ['assignment', 'homework', 'submit', 'due', 'deadline', 'pending', 'task']):
            assignments = ctx.get('assignments', [])
            if not assignments:
                return f"No assignments found for {branch} yet. Faculty will post assignments and they'll appear here."
            lines = [f"📝 **Assignments for {branch}:**\n"]
            for a in assignments:
                if role == 'student':
                    status = '✅ Submitted' if a['submitted'] else f"⏰ Due: {a['deadline']}"
                    lines.append(f"• **{a['title']}** ({a['subject']}) — {status}")
                else:
                    lines.append(f"• **{a['title']}** ({a['subject']}) — Due: {a['deadline']} | {a['submissions']} submitted")
            pending = [a for a in assignments if role == 'student' and not a['submitted']]
            if pending:
                lines.append(f"\n⚠️ You have **{len(pending)} pending** assignment(s)!")
            return '\n'.join(lines)

        # ── ANNOUNCEMENT / NOTICE / CIRCULAR queries ──────────────────────────
        if any(w in msg for w in ['announcement', 'notice', 'circular', 'news', 'update', 'notification', 'event', 'exam', 'holiday']):
            ann = ctx.get('announcements', [])
            if not ann:
                return "No announcements right now. I'll let you know when something is posted!"
            icons = {'urgent': '🔴', 'event': '📢', 'general': '📌'}
            lines = [f"🔔 **Latest Announcements for {branch}:**\n"]
            for a in ann:
                icon = icons.get(a['urgency'], '📌')
                lines.append(f"{icon} **{a['title']}** ({a['date']})")
            lines.append("\n➡️ Go to **Notices** section to read full details.")
            return '\n'.join(lines)

        # ── TIMETABLE queries ─────────────────────────────────────────────────
        if any(w in msg for w in ['timetable', 'schedule', 'class', 'today', 'tomorrow', 'time table', 'period']):
            return f"📅 Hi {name}! Go to the **Timetable** section in your dashboard to see your full {branch} week schedule."

        # ── CGPA / MARKS queries ──────────────────────────────────────────────
        if any(w in msg for w in ['cgpa', 'marks', 'result', 'grade', 'score', 'gpa']):
            return f"🎓 Hi {name}! Check the **Results** section for your CGPA and marks. Results are updated by the admin after each exam."

        # ── FACULTY queries (from student) ────────────────────────────────────
        if any(w in msg for w in ['faculty', 'teacher', 'professor', 'hod', 'lecturer', 'sir', 'mam', 'ma\'am']):
            return f"👩‍🏫 Your faculty details are listed in your **Student Profile** section under 'Faculty Assigned'. You can also see faculty names in the timetable."

        # ── BRANCH / DEPARTMENT queries ───────────────────────────────────────
        if any(w in msg for w in ['branch', 'department', 'aiml', 'cse', 'cs', 'it', 'me', 'mechanical']):
            return f"🏫 You are enrolled in the **{branch}** branch at IIST Indore, Semester {ctx.get('sem', '')}."

        # ── GREETING ─────────────────────────────────────────────────────────
        if any(w in msg for w in ['hi', 'hello', 'hey', 'namaste', 'good morning', 'good afternoon', 'good evening']):
            role_hint = "attendance, notes, assignments, announcements, and timetable" if role == 'student' else "attendance, uploaded notes, assignments, and announcements"
            return f"👋 Hello {name}! I'm your Campus Mitra AI assistant.\n\nI can help you with:\n• 📊 Attendance — ask 'What is my attendance?'\n• 📚 Notes — ask 'Show my study materials'\n• 📝 Assignments — ask 'What are my pending assignments?'\n• 🔔 Announcements — ask 'Any new notices?'\n• 📅 Timetable — ask 'Show my schedule'\n\nWhat would you like to know?"

        # ── HELP ──────────────────────────────────────────────────────────────
        if any(w in msg for w in ['help', 'what can you', 'what do you', 'how to', 'guide']):
            return f"🤖 **Campus Mitra AI — What I can help with:**\n\n📊 **Attendance** — 'What is my CN attendance?', 'Show attendance summary'\n📚 **Notes** — 'Show study materials', 'Any new notes?'\n📝 **Assignments** — 'What assignments are due?', 'Show pending tasks'\n🔔 **Notices** — 'Any new announcements?', 'Show circulars'\n📅 **Timetable** — 'Show my schedule'\n🎓 **Results** — 'What is my CGPA?'\n\nJust ask naturally and I'll answer using your real data!"

        # ── DEFAULT ───────────────────────────────────────────────────────────
        return f"🤔 I'm not sure about that, {name}. Try asking about:\n• Your **attendance** (e.g. 'What is my attendance?')\n• **Study materials** (e.g. 'Show notes')\n• **Assignments** (e.g. 'What are my pending assignments?')\n• **Announcements** (e.g. 'Any new notices?')\n• **Timetable** (e.g. 'Show my schedule')"
