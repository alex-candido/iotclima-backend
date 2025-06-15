# django_app/modules/v1/station_sensors/admin.py

from django.contrib import admin

from .models import StationSensor


@admin.register(StationSensor)
class StationSensorAdmin(admin.ModelAdmin):
    list_display = (
        'uuid', 'station', 'sensor', 'position', 'installed_date',
        'get_station_name',
        'get_sensor_type_display',
        'get_sensor_model'
    )
    list_filter = (
        'station', 'sensor__type', 'is_active', 'installed_date', 'removed_date',
        'calibrated_at', 'created_at'
    )
    search_fields = (
        'station__name', 'sensor__model', 'position', 'uuid', 
    )
    ordering = ('-created_at',)

    raw_id_fields = ('station', 'sensor') 

    @admin.display(description='Station Name')
    def get_station_name(self, obj):
        return obj.station.name

    @admin.display(description='Sensor Type')
    def get_sensor_type_display(self, obj):
        return obj.sensor.get_type_display() # type: ignore

    @admin.display(description='Sensor Model')
    def get_sensor_model(self, obj):
        return obj.sensor.model