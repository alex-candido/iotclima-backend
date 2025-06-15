# django_app/modules/v1/stations/admin.py

from django.contrib import admin

from .models import Station, StationStatus


@admin.register(Station)
class StationAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'model', 'firmware', 'status', 'battery_level',
        'signal_strength', 'place', 'user', 'installed_at', 'created_at',
        'get_status_display_value', 
        'get_place_name',           
        'get_user_username'         
    )
    list_filter = (
        'status', 'model', 'firmware', 'place', 'user', 'installed_at',
        'last_maintenance_at', 'next_maintenance_at'
    )
    search_fields = ('name', 'description', 'model', 'firmware')
    ordering = ('-created_at',)

    raw_id_fields = ('place', 'user')
    list_per_page = 25

    @admin.display(description='Status')
    def get_status_display_value(self, obj):
        return obj.get_status_display()

    @admin.display(description='Place')
    def get_place_name(self, obj):
        return obj.place.name if obj.place else '-'

    @admin.display(description='Managed By')
    def get_user_username(self, obj):
        return obj.user.username if obj.user else '-'