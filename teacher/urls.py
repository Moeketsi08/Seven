from django.urls import path
from . import views



urlpatterns = [
    path('login/', views.teacher_login, name='teacher_login'),
    path('dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('submit-attendance-and-timesheet/<int:session_id>/', views.submit_attendance_and_timesheet, name='submit_attendance_and_timesheet'),
]
