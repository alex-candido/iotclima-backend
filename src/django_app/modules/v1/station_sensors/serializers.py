# django_app/modules/v1/station_sensors/serializers.py

from rest_framework import serializers

from django_app.modules.v1.sensors.models import Sensor
from django_app.modules.v1.stations.models import Station

from .models import StationSensor


class StationSensorInputSerializer(serializers.Serializer):
    station = serializers.PrimaryKeyRelatedField(queryset=Station.objects.all(), required=True)
    sensor = serializers.PrimaryKeyRelatedField(queryset=Sensor.objects.all(), required=True)

    position = serializers.CharField(max_length=100, allow_blank=True, required=False)
    installed_date = serializers.DateTimeField(allow_null=True, required=False)
    removed_date = serializers.DateTimeField(allow_null=True, required=False)
    is_active = serializers.BooleanField(required=False, default=True)
    calibrated_at = serializers.DateTimeField(allow_null=True, required=False)


class StationSensorOutputSerializer(serializers.ModelSerializer):
    station_id = serializers.IntegerField(source='station.id', read_only=True)
    station_uuid = serializers.UUIDField(source='station.uuid', read_only=True)
    station_name = serializers.CharField(source='station.name', read_only=True)
    station_model = serializers.CharField(source='station.model', read_only=True)

    sensor_id = serializers.IntegerField(source='sensor.id', read_only=True)
    sensor_uuid = serializers.UUIDField(source='sensor.uuid', read_only=True)
    sensor_model = serializers.CharField(source='sensor.model', read_only=True)
    sensor_type_display = serializers.CharField(source='sensor.get_type_display', read_only=True)
    sensor_unit_display = serializers.CharField(source='sensor.get_unit_display', read_only=True)
    sensor_status_display = serializers.CharField(source='sensor.get_status_display', read_only=True)


    class Meta:
        model = StationSensor
        fields = (
            'id', 'uuid',
            'station_id', 'station_uuid', 'station_name', 'station_model',
            'sensor_id', 'sensor_uuid', 'sensor_model', 'sensor_type_display', 'sensor_unit_display', 'sensor_status_display',
            'position', 'installed_date', 'removed_date', 'is_active', 'calibrated_at',
            'created_at', 'updated_at'
        )