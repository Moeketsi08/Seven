from django.urls import path
from . import views


urlpatterns = [
    path('login/', views.admin_login, name='admin_login'),
    path('center_manager/center_login/', views.CenterLoginView.as_view(), name='center_login'),
    path('center_manager/center_dashboard/', views.center_dashboard, name='center_dashboard'),
    path('center_manager/allocate_teacher/', views.allocate_teacher, name='allocate_teacher'),
    path('center_manager/edit_teacher_allocate/', views.edit_teacher_allocation, name='edit_teacher_allocation'),
    path('logout/', views.admin_logout, name='admin_logout'),
    path('center_manager/teacher-list/', views.teacher_list, name='teacher_list'),
    path('center_manager/teacher-profile/<int:teacher_id>/', views.teacher_profile, name='teacher_profile'),
    path('center_manager/teacher-delete/<int:teacher_id>/', views.teacher_delete, name='teacher_delete'),
    path('center_manager/profile/', views.profile, name='profile'),
    path('center_manager/update-profile/', views.update_profile, name='update-profile'),
    path('center_manager/learner-list/', views.learner_list, name='learner-list'),
    path('center_manager/learner-search/', views.learner_search, name='learner-search'),
]
    
    
    # New teacher management URLs
    # path('teacher/register/', views.teacher_registration, name='admin_teacher_registration'),
    # path('add-designation/', views.add_designation, name='add_designation'),
    # path('designation/', views.designation_view, name='designation'),

