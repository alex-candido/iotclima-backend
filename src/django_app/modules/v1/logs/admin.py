# django_app/modules/v1/logs/admin.py

from django.contrib import admin

from .models import Log, LogSeverity


@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    list_display = (
        'uuid', 'get_level_display', 'message', 'user', 'station', 'created_at',
        'get_user_username', 'get_station_name',
    )
    list_filter = (
        'station', 'created_at'
    )
    search_fields = (
        'message', 'user__username', 'station__name', 'uuid'
    )
    ordering = ('-created_at',)

    raw_id_fields = ('user', 'station',)
    
    readonly_fields = ('uuid', 'created_at', 'updated_at', 'metadata',)
    
    list_per_page = 25

    @admin.display(description='Level')
    def get_level_display(self, obj):
        return obj.get_level_display()

    @admin.display(description='User')
    def get_user_username(self, obj):
        return obj.user.username if obj.user else '-'

    @admin.display(description='Station')
    def get_station_name(self, obj):
        return obj.station.name if obj.station else '-'