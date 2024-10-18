from django.urls import path
from . import views
from .views import TeacherLoginView, teacher_dashboard



urlpatterns = [
    path('teacher/teacher_login/', views.TeacherLoginView.as_view(), name='teacher_login'),
    path('teacher/teacher_dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('teacher/profile/', views.teacher_profile, name='teacher_profile'),
    # path('submit-attendance-timesheet/<int:session_id>/', views.submit_attendance_and_timesheet, name='submit_attendance_and_timesheet'),
    path('teacher/learner-list/', views.learner_list, name='learner-list'),
    path('teacher/learner-search/', views.learner_search, name='learner-search'),
]
