from django.contrib import admin
from .models import LearnerAttendance

class LearnerAttendanceAdmin(admin.ModelAdmin):
    list_display = ['classroom', 'attendance_date', 'status']  # Removed 'learner'
    list_filter = ['attendance_date', 'status']
    search_fields = ['classroom_grade']  # Assuming ClassRegistration has a 'name' field

admin.site.register(LearnerAttendance, LearnerAttendanceAdmin)
