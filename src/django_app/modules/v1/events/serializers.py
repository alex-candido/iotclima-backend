# django_app/modules/v1/events/serializers.py

from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import serializers

from django_app.modules.v1.station_sensors.models import StationSensor

from .models import Event, EventCategory, EventSeverity, EventStatus, EventType

User = get_user_model()


class EventsInputSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    description = serializers.CharField()
    occurred_at = serializers.DateTimeField()
    resolved_at = serializers.DateTimeField(allow_null=True, required=False)

    type = serializers.ChoiceField(choices=EventType.choices)
    category = serializers.ChoiceField(choices=EventCategory.choices)
    severity = serializers.ChoiceField(choices=EventSeverity.choices)
    status = serializers.ChoiceField(choices=EventStatus.choices, default=EventStatus.OPEN)
    
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        required=False,
        allow_null=True
    )
    station_sensor = serializers.PrimaryKeyRelatedField(
        queryset=StationSensor.objects.all(), 
        required=False, 
        allow_null=True
    )

class EventsOutputSerializer(serializers.ModelSerializer):
    type_display = serializers.CharField(source='get_type_display', read_only=True)
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    severity_display = serializers.CharField(source='get_severity_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    user_username = serializers.CharField(source='user.username', read_only=True, required=False, allow_null=True)
    
    station_name = serializers.CharField(source='station_sensor.station.name', read_only=True, required=False, allow_null=True)
    station_model = serializers.CharField(source='station_sensor.station.model', read_only=True, required=False, allow_null=True)
    
    sensor_model = serializers.CharField(source='station_sensor.sensor.model', read_only=True, required=False, allow_null=True)
    sensor_type_display = serializers.CharField(source='station_sensor.sensor.get_type_display', read_only=True, required=False, allow_null=True)


    class Meta:
        model = Event
        fields = (
            'id', 'uuid', 'title', 'description', 'occurred_at', 'resolved_at',
            'type', 'type_display',
            'category', 'category_display',
            'severity', 'severity_display',
            'status', 'status_display',
            'user', 'user_username',
            'station_sensor', 
            'station_name', 
            'station_model', 
            'sensor_model', 
            'sensor_type_display', 
            'created_at', 'updated_at'
        )