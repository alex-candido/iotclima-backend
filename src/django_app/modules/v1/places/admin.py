# django_app/modules/v1/places/admin.py

from django.contrib import admin
from django.contrib.gis.admin import GISModelAdmin

from .models import Place


@admin.register(Place)
class PlaceAdmin(GISModelAdmin):
    list_display = (
        'name', 'city', 'state', 'country', 'status', 'type', 'user',
        'get_latitude', 'get_longitude',
        'created_at'
    )
    list_filter = ('status', 'type', 'city', 'state', 'country', 'created_at')
    search_fields = ('name', 'description', 'address', 'city', 'state', 'country')
    ordering = ('name',)

    gis_map_filters = ['city', 'state', 'country']

    readonly_fields = (
        'uuid', 'created_at', 'updated_at',
        'get_latitude_display', 'get_longitude_display'
    )

    @admin.display(description='Latitude')
    def get_latitude(self, obj):
        return obj.location.y if obj.location else None

    @admin.display(description='Longitude')
    def get_longitude(self, obj):
        return obj.location.x if obj.location else None

    @admin.display(description='Latitude')
    def get_latitude_display(self, obj):
        return f"{obj.location.y:.6f}" if obj.location else "N/A"

    @admin.display(description='Longitude')
    def get_longitude_display(self, obj):
        return f"{obj.location.x:.6f}" if obj.location else "N/A"