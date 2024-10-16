from django.urls import path
from .views import SetAttendance #learner_attendance was also imported. Currently disabled learner app

urlpatterns = [
    #path('learner/', learner_attendance, name='learner-attendance'),
    path('set-attendance/<std_class>/<std_roll>', SetAttendance.as_view(), name='set-attendance')
]