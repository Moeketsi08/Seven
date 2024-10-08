from django.urls import path
from . import views
from .views import TeacherLoginView, teacher_dashboard



urlpatterns = [
    path('teacher_login/', views.TeacherLoginView.as_view(), name='teacher_login'),
    path('teacher_dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('profile/', views.teacher_profile, name='teacher_profile'),
    path('submit-attendance-timesheet/<int:session_id>/', views.submit_attendance_and_timesheet, name='submit_attendance_and_timesheet'),
    path('student-list/', views.student_list, name='student-list'),
    path('student-search/', views.student_search, name='student-search'),
]
