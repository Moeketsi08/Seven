from django.contrib import admin
from . import models

admin.site.register(models.Teacher)
admin.site.register(models.TeacherCenterAssignment)
admin.site.register(models.Classroom)
