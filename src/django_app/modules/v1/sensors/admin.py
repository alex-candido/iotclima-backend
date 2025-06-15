# django_app/modules/v1/sensors/admin.py

from django.contrib import admin
from .models import Sensors

@admin.register(Sensors)
class SensorsAdmin(admin.ModelAdmin):
    list_display = ('id', 'uuid', 'name', 'created_at', 'updated_at')
    search_fields = ('id', 'uuid', 'name')
    ordering = ('-created_at',)
