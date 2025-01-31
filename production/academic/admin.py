from django.contrib import admin
# from advanced_filters.admin import AdminAdvancedFiltersMixin

from . import models


admin.site.register(models.Department)
admin.site.register(models.Nationality)
admin.site.register(models.Session)
admin.site.register(models.Grade)
admin.site.register(models.Registration)
admin.site.register(models.Subject)