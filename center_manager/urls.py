from django.urls import path
from . import views
from .views import  upload_document

urlpatterns = [
    #path('', views.root_redirect_view, name='root_redirect'),
    path('login/', views.admin_login, name='admin_login'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('center-manager/center-login/', views.CenterLoginView.as_view(), name='center-login'),
    path('center-manager/center-dashboard/', views.center_dashboard, name='center-dashboard'),
    path('center-manager/allocate_teacher/', views.allocate_teacher, name='allocate_teacher'),
    path('center-manager/edit_teacher_allocate/', views.edit_teacher_allocation, name='edit_teacher_allocation'),
    path('logout/', views.admin_logout, name='admin_logout'),
    path('center-manager/teacher-list/', views.teacher_list, name='teacher_list'),
    path('center-manager/teacher-profile/<int:teacher_id>/', views.teacher_profile, name='teacher-profile'),
    path('center-manager/teacher-delete/<int:teacher_id>/', views.teacher_delete, name='teacher_delete'),
    path('center-manager/profile/', views.profile, name='profile'),
    path('center-manager/update-profile/', views.update_profile, name='update-profile'),
    path('center-manager/learner-list/', views.learner_list, name='center-learner-list'),
    path('center-manager/learner-search/', views.learner_search, name='center-learner-search'),
    path('center-manager/learner-login/', views.LearnerLoginView.as_view(), name='learner-login'),
    path('center-manager/learner-dashboard/', views.learner_dashboard, name='learner-dashboard'),
    path('center-manager/learner-registration/', views.learner_registration, name='learner-registration'),
    path('center-manager/teacher-timesheets/', views.teacher_timesheets, name='teacher-timesheets'),
    path('center-manager/learner-attendance/',  views.learner_attendance, name='center-learner-attendance'),
    path('center-manager/learner-report/', views.learner_report, name='center-learner-report'),
    path('center-manager/admin-learner-registration/', views.admin_learner_registration, name='admin-learner-registration'),
    path('center-manager/admin_teacher_timesheets/', views.admin_teacher_timesheets, name='admin_teacher_timesheets'),
    path('center-manager/admin-learner-attendance/',  views.admin_learner_attendance, name='admin-learner-attendance'),
    path('center-manager/admin-learner-report/', views.admin_learner_report, name='admin-learner-report'),
    path('center-manager/admin-learner-list/', views.admin_learner_list, name='admin-learner-list'),
    path('center-manager/admin-learner-search/', views.admin_learner_search, name='admin-learner-search'),
    path('center-manager/admin_edit_teacher_allocate/', views.admin_edit_teacher_allocation, name='admin_edit_teacher_allocation'),
    path('center-manager/admin_teacher-list/', views.admin_teacher_list, name='admin_teacher_list'),
    path('center-manager/admin_teacher-profile/<int:teacher_id>/', views.admin_teacher_profile, name='admin_teacher-profile'),
    path('center-manager/export-timesheet-csv/', views.export_timesheet_csv, name='export_timesheet_csv'),
    path('center-manager/export-timesheet-pdf/', views.export_timesheet_pdf, name='export_timesheet_pdf'),
    path('center-manager/upload-document/', upload_document, name='upload_document'),
]
    
    
    # New teacher management URLs
    # path('teacher/register/', views.teacher_registration, name='admin_teacher_registration'),
    # path('add-designation/', views.add_designation, name='add_designation'),
    # path('designation/', views.designation_view, name='designation'),

