from django.urls import path
from . import views

urlpatterns = [
    path('attendance/',                         views.faculty_attendance_list,  name='faculty_attendance_list'),
    path('attendance/mark/<int:slot_id>/',      views.mark_attendance,          name='mark_attendance'),
    path('attendance/my/',                      views.student_attendance_view,  name='student_attendance'),
    path('attendance/report/',                  views.admin_attendance_report,  name='admin_attendance_report'),
]
