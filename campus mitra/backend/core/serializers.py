from rest_framework import serializers
from .models import (User, Student, Faculty, Parent, Department,
                     Subject, Timetable, Attendance, Note, Announcement,
                     Assignment, AssignmentSubmission)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'first_name', 'last_name']


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'


class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    department = DepartmentSerializer(read_only=True)

    class Meta:
        model = Student
        fields = '__all__'


class FacultySerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    department = DepartmentSerializer(read_only=True)

    class Meta:
        model = Faculty
        fields = '__all__'


class SubjectSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer(read_only=True)
    faculty_name = serializers.SerializerMethodField()

    def get_faculty_name(self, obj):
        if obj.faculty:
            return obj.faculty.user.get_full_name()
        return ''

    class Meta:
        model = Subject
        fields = '__all__'


class TimetableSerializer(serializers.ModelSerializer):
    subject_name = serializers.CharField(source='subject.name', read_only=True)
    subject_code = serializers.CharField(source='subject.code', read_only=True)
    department_name = serializers.CharField(source='department.name', read_only=True)

    class Meta:
        model = Timetable
        fields = '__all__'


class AttendanceSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.user.get_full_name', read_only=True)
    enrollment_no = serializers.CharField(source='student.enrollment_no', read_only=True)
    subject_name = serializers.CharField(source='subject.name', read_only=True)

    class Meta:
        model = Attendance
        fields = '__all__'


class NoteSerializer(serializers.ModelSerializer):
    subject_name = serializers.CharField(source='subject.name', read_only=True)
    subject_code = serializers.CharField(source='subject.code', read_only=True)
    uploaded_by_name = serializers.SerializerMethodField()
    file_url = serializers.SerializerMethodField()

    def get_uploaded_by_name(self, obj):
        return obj.uploaded_by.user.get_full_name()

    def get_file_url(self, obj):
        request = self.context.get('request')
        if obj.file and request:
            return request.build_absolute_uri(obj.file.url)
        return obj.file.url if obj.file else ''

    class Meta:
        model = Note
        fields = ['id', 'title', 'subject', 'subject_name', 'subject_code',
                  'uploaded_by', 'uploaded_by_name', 'file', 'file_url', 'uploaded_at']
        read_only_fields = ['uploaded_by', 'uploaded_at', 'subject_name',
                            'subject_code', 'uploaded_by_name', 'file_url']


class AnnouncementSerializer(serializers.ModelSerializer):
    posted_by_name = serializers.CharField(source='posted_by.get_full_name', read_only=True)
    department_name = serializers.SerializerMethodField()

    def get_department_name(self, obj):
        return obj.department.name if obj.department else ''

    class Meta:
        model = Announcement
        fields = '__all__'


class AssignmentSerializer(serializers.ModelSerializer):
    subject_name = serializers.CharField(source='subject.name', read_only=True)
    subject_code = serializers.CharField(source='subject.code', read_only=True)
    department_name = serializers.CharField(source='subject.department.name', read_only=True)
    faculty_name = serializers.SerializerMethodField()
    file_url = serializers.SerializerMethodField()
    submission_count = serializers.SerializerMethodField()

    def get_faculty_name(self, obj):
        if obj.uploaded_by:
            return obj.uploaded_by.user.get_full_name()
        return ''

    def get_file_url(self, obj):
        request = self.context.get('request')
        if obj.file and request:
            return request.build_absolute_uri(obj.file.url)
        return obj.file.url if obj.file else ''

    def get_submission_count(self, obj):
        return obj.submissions.count()

    class Meta:
        model = Assignment
        fields = ['id', 'title', 'description', 'subject', 'subject_name', 'subject_code',
                  'department_name', 'uploaded_by', 'faculty_name', 'file', 'file_url',
                  'deadline', 'created_at', 'submission_count']
        read_only_fields = ['uploaded_by', 'created_at', 'subject_name', 'subject_code',
                            'department_name', 'faculty_name', 'file_url', 'submission_count']


class AssignmentSubmissionSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.user.get_full_name', read_only=True)
    enrollment_no = serializers.CharField(source='student.enrollment_no', read_only=True)
    assignment_title = serializers.CharField(source='assignment.title', read_only=True)
    file_url = serializers.SerializerMethodField()

    def get_file_url(self, obj):
        request = self.context.get('request')
        if obj.file and request:
            return request.build_absolute_uri(obj.file.url)
        return obj.file.url if obj.file else ''

    class Meta:
        model = AssignmentSubmission
        fields = '__all__'
