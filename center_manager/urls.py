from django.urls import path
from . import views


urlpatterns = [
    path('login/', views.admin_login, name='admin_login'),
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
    
]
    
    
    # New teacher management URLs
    # path('teacher/register/', views.teacher_registration, name='admin_teacher_registration'),
    # path('add-designation/', views.add_designation, name='add_designation'),
    # path('designation/', views.designation_view, name='designation'),

