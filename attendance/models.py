from django.db import models
from academic.models import Registration
from student.models import Student
from teacher.models import Classroom

class AttendanceManager(models.Manager):
    def create_attendance(self, std_class, std_roll):
        std_cls = Registration.objects.get(name=std_class)
        std = Student.objects.get(roll=std_roll, class_registration=std_cls)
        std_att = StudentAttendance.objects.create(
            class_name=std_cls,
            student=std,
            status=1
        )
        return std_att

class StudentAttendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    
    STATUS_CHOICES = [('Present', 'Present'), ('Absent', 'Absent'), ('Late', 'Late')]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Present')
    objects = AttendanceManager()
    attendance_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['student', 'attendance_date']

    def __str__(self):
        return f"{self.student.name} {self.student.surname}"
