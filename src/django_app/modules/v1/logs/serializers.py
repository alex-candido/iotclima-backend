# django_app/modules/v1/logs/serializers.py

from django.contrib.auth import get_user_model
from rest_framework import serializers

from django_app.modules.v1.stations.models import Station

from .models import Log, LogSeverity

User = get_user_model()

class LogsInputSerializer(serializers.Serializer):
    message = serializers.CharField()
    level = serializers.ChoiceField(choices=LogSeverity.choices, default=LogSeverity.INFO)
    metadata = serializers.JSONField(binary=False, required=False, allow_null=True)
    
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        required=False,
        allow_null=True
    )
    station = serializers.PrimaryKeyRelatedField(
        queryset=Station.objects.all(),
        required=False,
        allow_null=True
    )

class LogsOutputSerializer(serializers.ModelSerializer):
    level_display = serializers.CharField(source='get_level_display', read_only=True)

    user_username = serializers.CharField(source='user.username', read_only=True, required=False, allow_null=True)
    station_name = serializers.CharField(source='station.name', read_only=True, required=False, allow_null=True)


    class Meta:
        model = Log
        fields = (
            'id', 'uuid', 'message', 'level', 'level_display', 'metadata',
            'user', 'user_username', 'station', 'station_name',
            'created_at', 'updated_at'
        )