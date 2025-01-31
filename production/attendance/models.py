from django.db import models
from learner.models import Learner
from teacher.models import Classroom, Teacher

class LearnerAttendance(models.Model):
    STATUS_CHOICES = (
        ('P', 'Present'),
        ('A', 'Absent'),
        ('L', 'Late'),
    )

    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    learner = models.ForeignKey(Learner, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    status = models.CharField(choices=STATUS_CHOICES, max_length=1)
    remarks = models.TextField(blank=True, null=True)
    
    class Meta:
        unique_together = ('teacher', 'classroom', 'learner', 'date')

    def __str__(self):
        return f'{self.learner.name} - {self.date} - {self.status}'
