from django.urls import path
from . import views

urlpatterns = [
<<<<<<< Updated upstream
    path('add-department/', views.add_department, name='add-department'),
    path('create-class/', views.add_class, name='create-class'),
    path('create-section/', views.create_section, name='create-section'),
    path('create-session/', views.create_session, name='create-session'),
    path('create-shift/', views.create_shift, name='create-shift'),
    path('class-registration/', views.class_registration, name='class-registration'),
    path('class-list/', views.class_list, name='class-list'),
    path('guide-teacher/', views.create_guide_teacher, name='guide-teacher'),

    # Ajax URLs for loading dynamic dropdowns
    path('ajax/load-upazilla/', views.load_upazilla, name='load-upazilla'),  # Corrected line
    path('ajax/load-union/', views.load_union, name='load-union'),
=======
    path('add-department', views.add_department, name='add-department'),
    path('create-class', views.add_class, name='create-class'),
    path('create-section', views.create_section, name='create-section'),
    path('create-session', views.create_session, name='create-session'),
    path('create-shift', views.create_shift, name='create-shift'),
    path('class-registration', views.class_registration, name='class-registration'),
    path('class-list', views.class_list, name='class-list'),
    #path('guide-teacher', views.create_guide_teacher, name='guide-teacher'),
>>>>>>> Stashed changes
]




