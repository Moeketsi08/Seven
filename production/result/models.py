from django.db import models

from academic.models import Registration

# Create your models here.

# TODO linked to teacher

class SubjectRegistration(models.Model):
    select_class = models.ForeignKey(Registration, on_delete=models.CASCADE, null=True)
    subject_name = models.CharField(max_length=45)
    subject_code = models.IntegerField(unique=True)
    marks = models.IntegerField()
    pass_mark = models.IntegerField()
    add_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.subject_name
