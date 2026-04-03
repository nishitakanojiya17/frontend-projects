from django.urls import path
from . import views

urlpatterns = [
    path('login/',              views.login_view,        name='login'),
    path('logout/',             views.logout_view,       name='logout'),
    path('dashboard/',          views.dashboard_redirect, name='dashboard'),
    path('dashboard/student/',  views.student_dashboard, name='student_dashboard'),
    path('dashboard/faculty/',  views.faculty_dashboard, name='faculty_dashboard'),
    path('dashboard/parent/',   views.parent_dashboard,  name='parent_dashboard'),
    path('dashboard/admin/',    views.admin_dashboard,   name='admin_dashboard'),
]
