# django_app/modules/v1/sensors/admin.py

from django.contrib import admin

from .models import (Sensor, SensorStatus, SensorType,  # Importar UnitType
                     UnitType)


@admin.register(Sensor)
class SensorAdmin(admin.ModelAdmin):
    list_display = (
        'uuid',
        'get_type_display_value',
        'model',
        'get_unit_display_value',
        'min_value',
        'max_value',
        'get_status_display_value',
        'user',
        'created_at',
    )
    list_filter = (
        'type',
        'status',
        'model',
        'unit',
        'user',
        'created_at',
    )
    search_fields = (
        'model',
        'unit',
        'uuid',
    )
    ordering = ('type', 'model',)

    raw_id_fields = ('user',)
    list_per_page = 25

    @admin.display(description='Sensor Type')
    def get_type_display_value(self, obj):
        return obj.get_type_display()

    @admin.display(description='Status')
    def get_status_display_value(self, obj):
        return obj.get_status_display()
    
    @admin.display(description='Unit')
    def get_unit_display_value(self, obj):
        return obj.get_unit_display()