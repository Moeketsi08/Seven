from django.urls import path
from . import views


urlpatterns = [
    path('login/', views.admin_login, name='admin_login'),
    path('logout/', views.admin_logout, name='admin_logout'),
    path('add-designation/', views.add_designation, name='add_designation'),
    
    # New teacher management URLs
    path('teacher/register/', views.teacher_registration, name='admin_teacher_registration'),
    path('teacher/list/', views.admin_teacher_list, name='admin_teacher_list'),
    path('teacher/profile/<int:teacher_id>/', views.admin_teacher_profile, name='admin_teacher_profile'),
    path('teacher/delete/<int:teacher_id>/', views.admin_teacher_delete, name='admin_teacher_delete'),
    path('teacher/edit/<int:teacher_id>/', views.admin_teacher_edit, name='admin_teacher_edit'),
    
    path('designation/', views.designation_view, name='designation'),
]
