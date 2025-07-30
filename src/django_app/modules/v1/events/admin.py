# django_app/modules/v1/events/admin.py

from django.contrib import admin

from django_app.modules.v1.sensors.models import Sensor
from django_app.modules.v1.station_sensors.models import StationSensor
from django_app.modules.v1.stations.models import Station

from .models import Event, EventCategory, EventSeverity, EventStatus, EventType


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = (
        'uuid',
        'title',
        'get_type_display',
        'get_category_display',
        'get_severity_display',
        'get_status_display',
        'station_sensor',
        'user',
        'occurred_at',
        'resolved_at',
        'created_at',
    )
    list_filter = (
        'type', 'category', 'severity', 'status', 
        'station_sensor__sensor__type',
        'station_sensor__sensor__model',
        'station_sensor__sensor__status',
        'user',
        'occurred_at', 'resolved_at', 'created_at'
    )
    search_fields = (
        'title', 'description', 
        'station_sensor__sensor__model',
        'user__username',
    )
    ordering = ('-occurred_at',)

    raw_id_fields = ('user', 'station_sensor',)


    @admin.display(description='Type')
    def get_type_display(self, obj):
        return obj.get_type_display()

    @admin.display(description='Category')
    def get_category_display(self, obj):
        return obj.get_category_display()
    
    @admin.display(description='Severity')
    def get_severity_display(self, obj):
        return obj.get_severity_display()
    
    @admin.display(description='Status')
    def get_status_display(self, obj):
        return obj.get_status_display()