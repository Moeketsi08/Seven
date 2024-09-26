from django.urls import path
from . import views



urlpatterns = [
<<<<<<< Updated upstream
    path('registration/', views.teacher_registration, name='teacher-registration'),
    path('list/', views.teacher_list, name='teacher-list'),
    path('profile/<int:teacher_id>/', views.teacher_profile, name='teacher-profile'),
    path('delete/<int:teacher_id>/', views.teacher_delete, name='teacher-delete'),
    path('edit/<int:teacher_id>/', views.teacher_edit, name='teacher-edit'),
    path('load-upazilla/', views.load_upazilla, name='load-upazilla'),
    path('login/', views.TeacherLoginView.as_view(), name='teacher_login'),
    path('dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    
=======
    path('login/', views.teacher_login, name='teacher_login'),
    path('dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('submit-attendance-and-timesheet/<int:session_id>/', views.submit_attendance_and_timesheet, name='submit_attendance_and_timesheet'),
>>>>>>> Stashed changes
]
