from django.urls import path
from . import views
from .views import TeacherLoginView, teacher_dashboard



urlpatterns = [
    path('teacher-login/', views.TeacherLoginView.as_view(), name='teacher-login'),
    path('learner-attendance/', views.learner_attendance, name='learner-attendance'),
    path('learner-report/', views.learner_report, name='learner-report'),
    path('teacher-dashboard/', views.teacher_dashboard, name='teacher-dashboard'),
    path('profile/', views.teacher_profile, name='teacher-profile'),
    # path('submit-attendance-timesheet/<int:session_id>/', views.submit_attendance_and_timesheet, name='submit_attendance_and_timesheet'),
    path('learner-list/', views.learner_list, name='learner-list'),
    path('learner-search/', views.learner_search, name='learner-search'),
]
