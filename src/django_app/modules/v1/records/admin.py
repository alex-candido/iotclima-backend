# django_app/modules/v1/records/admin.py

from django.contrib import admin

from .models import Record, Status


@admin.register(Record)
class RecordAdmin(admin.ModelAdmin):
    list_display = (
        'station', 'recorded_at', 'temperature', 'humidity', 'wind_speed',
        'wind_direction', 'pressure', 'rainfall', 'status', 'created_at',
        'get_status_display_value', 'get_station_name',
    )
    list_filter = (
        'status', 'recorded_at', 'created_at',
    )
    search_fields = (
        'station__name', 'recorded_at',
    )
    ordering = ('-recorded_at',)

    raw_id_fields = ('station',)
    list_per_page = 25
    
    @admin.display(description='Record Status')
    def get_status_display_value(self, obj):
        return obj.get_status_display()

    @admin.display(description='Station Name')
    def get_station_name(self, obj):
        return obj.station.name