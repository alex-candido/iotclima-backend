# django_app/modules/v1/records/serializers.py

from rest_framework import serializers

from django_app.modules.v1.station_sensors.serializers import \
    StationSensorOutputSerializer
from django_app.modules.v1.stations.models import Station

from .models import Record, Status


class RecordsInputSerializer(serializers.Serializer):
    recorded_at = serializers.DateTimeField()
    temperature = serializers.FloatField(allow_null=True, required=False)
    humidity = serializers.FloatField(allow_null=True, required=False)
    wind_speed = serializers.FloatField(allow_null=True, required=False)
    wind_direction = serializers.FloatField(allow_null=True, required=False)
    pressure = serializers.FloatField(allow_null=True, required=False)
    rainfall = serializers.FloatField(allow_null=True, required=False)
    
    status = serializers.ChoiceField(choices=Status.choices, default=Status.ACTIVE)
    
    station = serializers.PrimaryKeyRelatedField(
        queryset=Station.objects.all(), 
        required=True
    )


class RecordsOutputSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    station_name = serializers.CharField(source='station.name', read_only=True)
    station_model = serializers.CharField(source='station.model', read_only=True)
    station_firmware = serializers.CharField(source='station.firmware', read_only=True)
    station_status_display = serializers.CharField(source='station.get_status_display', read_only=True)

    class Meta:
        model = Record
        fields = (
            'id', 'uuid', 'recorded_at', 'temperature', 'humidity', 'wind_speed',
            'wind_direction', 'pressure', 'rainfall',
            'status', 'status_display',
            'station', 'station_name', 'station_model', 'station_firmware', 'station_status_display',
            'created_at', 'updated_at'
        )
        