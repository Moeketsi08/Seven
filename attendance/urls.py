from django.urls import path
from .views import SetAttendance #student_attendance was also imported. Currently disabled student app

urlpatterns = [
    #path('student/', student_attendance, name='student-attendance'),
    path('set-attendance/<std_class>/<std_roll>', SetAttendance.as_view(), name='set-attendance')
]