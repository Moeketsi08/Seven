from django.db import models
from academic.models import ClassRegistration, Student

class AttendanceManager(models.Manager):
    def create_attendance(self, std_class, std_roll):
        std_cls = ClassRegistration.objects.get(name=std_class)
        std = Student.objects.get(roll=std_roll, class_registration=std_cls)
        std_att = StudentAttendance.objects.create(
            class_name=std_cls,
            student=std,
            status=1
        )
        return std_att

class StudentAttendance(models.Model):
    class_name = models.ForeignKey(ClassRegistration, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, default=1)
    status = models.IntegerField(default=0)
    date = models.DateField(auto_now_add=True)

    objects = AttendanceManager()

    class Meta:
        unique_together = ['student', 'date']

    def __str__(self):
        return f"{self.student.first_name} {self.student.last_name}"
