from django.contrib import admin
from .models import Center, CenterManager, Designation, Report

class CenterAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs  # Superusers see all centers
        return qs.filter(center_manager=request.user.centermanager)  # Managers see only their centers

admin.site.register(Center)
admin.site.register(CenterManager)
admin.site.register(Designation)
admin.site.register(Report) 

