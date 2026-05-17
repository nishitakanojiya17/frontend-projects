from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

urlpatterns = [
    # ── Auth ──────────────────────────────────────────────────────────────────
    path('auth/login/',             views.LoginView.as_view(),              name='login'),
    path('auth/refresh/',           TokenRefreshView.as_view(),             name='token_refresh'),
    path('auth/me/',                views.MeView.as_view(),                 name='me'),

    # ── Attendance ─────────────────────────────────────────────────────────────
    path('attendance/mark/',        views.MarkAttendanceView.as_view(),     name='mark_attendance'),
    path('attendance/my/',          views.StudentAttendanceView.as_view(),  name='my_attendance'),
    path('attendance/subject/<int:subject_id>/',
                                    views.AttendanceBySubjectView.as_view(),name='attendance_by_subject'),

    # ── Notes ──────────────────────────────────────────────────────────────────
    path('notes/',                  views.NoteListView.as_view(),           name='notes'),
    path('notes/upload/',           views.NoteUploadView.as_view(),         name='note_upload'),

    # ── Assignments ────────────────────────────────────────────────────────────
    path('assignments/',            views.AssignmentListView.as_view(),     name='assignments'),

    # ── Announcements ──────────────────────────────────────────────────────────
    path('announcements/',          views.AnnouncementListView.as_view(),   name='announcements'),
    path('announcements/new/',      views.AnnouncementCreateView.as_view(), name='announcement_create'),

    # ── Timetable ──────────────────────────────────────────────────────────────
    path('timetable/',              views.TimetableView.as_view(),          name='timetable'),

    # ── Subjects ───────────────────────────────────────────────────────────────
    path('subjects/',               views.SubjectListView.as_view(),        name='subjects'),

    # ── Faculty ────────────────────────────────────────────────────────────────
    path('faculty/my/',             views.StudentFacultyListView.as_view(), name='student_faculty'),

    # ── Departments ────────────────────────────────────────────────────────────
    path('departments/',            views.DepartmentListView.as_view(),     name='departments'),

    # ── Parent ─────────────────────────────────────────────────────────────────
    path('parent/children/',        views.ParentChildView.as_view(),        name='parent_children'),

    # ── Admin ──────────────────────────────────────────────────────────────────
    path('admin/users/',            views.UserListView.as_view(),           name='admin_users'),
    path('admin/alerts/',           views.AttendanceAlertView.as_view(),    name='admin_alerts'),
    path('admin/students/',         views.AdminStudentListView.as_view(),   name='admin_students'),
    path('admin/faculty/',          views.AdminFacultyListView.as_view(),   name='admin_faculty'),
]
