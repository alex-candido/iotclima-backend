# django_app/modules/v1/events/serializers.py

from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import serializers

from django_app.modules.v1.sensors.models import Sensor
from django_app.modules.v1.stations.models import Station

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
    station = serializers.PrimaryKeyRelatedField(
        queryset=Station.objects.all(),
        required=True
    )
    sensor = serializers.PrimaryKeyRelatedField(
        queryset=Sensor.objects.all(),
        required=False,
        allow_null=True
    )


class EventsOutputSerializer(serializers.ModelSerializer):
    type_display = serializers.CharField(source='get_type_display', read_only=True)
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    severity_display = serializers.CharField(source='get_severity_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    user_username = serializers.CharField(source='user.username', read_only=True, required=False, allow_null=True)
    station_name = serializers.CharField(source='station.name', read_only=True)
    sensor_model = serializers.CharField(source='sensor.model', read_only=True, required=False, allow_null=True)


    class Meta:
        model = Event
        fields = (
            'id', 'uuid', 'title', 'description', 'occurred_at', 'resolved_at',
            'type', 'type_display',
            'category', 'category_display',
            'severity', 'severity_display',
            'status', 'status_display',
            'user', 'user_username',
            'station', 'station_name',
            'sensor', 'sensor_model',
            'created_at', 'updated_at'
        )