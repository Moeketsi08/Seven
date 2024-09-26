from django.contrib import admin
from .models import StudentAttendance

class StudentAttendanceAdmin(admin.ModelAdmin):
    list_display = ['class_name', 'date', 'status']  # Removed 'student'
    list_filter = ['date', 'status']
    search_fields = ['class_name__name']  # Assuming ClassRegistration has a 'name' field

admin.site.register(StudentAttendance, StudentAttendanceAdmin)
