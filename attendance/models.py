from django.db import models
from academic.models import Registration
from learner.models import Learner
from teacher.models import Classroom

class AttendanceManager(models.Manager):
    def create_attendance(self, std_class, std_roll):
        std_cls = Registration.objects.get(name=std_class)
        std = Learner.objects.get(roll=std_roll, class_registration=std_cls)
        std_att = LearnerAttendance.objects.create(
            class_name=std_cls,
            learner=std,
            status=1
        )
        return std_att

class LearnerAttendance(models.Model):
    learner = models.ForeignKey(Learner, on_delete=models.CASCADE)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    
    STATUS_CHOICES = [('Present', 'Present'), ('Absent', 'Absent'), ('Late', 'Late')]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Present')
    objects = AttendanceManager()
    attendance_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['learner', 'attendance_date']

    def __str__(self):
        return f"{self.learner.name} {self.learner.surname}"
