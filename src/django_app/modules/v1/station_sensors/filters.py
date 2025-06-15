import django_filters

from django_app.modules.v1.sensors.models import (SensorStatus, SensorType,
                                                  UnitType)
from django_app.modules.v1.stations.models import StationStatus

from .models import StationSensor


class StationSensorFilter(django_filters.FilterSet):
    installed_date = django_filters.DateTimeFromToRangeFilter()
    removed_date = django_filters.DateTimeFromToRangeFilter()
    calibrated_at = django_filters.DateTimeFromToRangeFilter()
    created_at = django_filters.DateTimeFromToRangeFilter()
    updated_at = django_filters.DateTimeFromToRangeFilter()

    is_active = django_filters.BooleanFilter()

    station_id = django_filters.NumberFilter(field_name='station__id', label="Station ID")
    station_name = django_filters.CharFilter(field_name='station__name', lookup_expr='icontains', label="Station Name")
    station_status = django_filters.ChoiceFilter(field_name='station__status', choices=StationStatus.choices, label="Station Status")

    sensor_id = django_filters.NumberFilter(field_name='sensor__id', label="Sensor ID")
    sensor_model = django_filters.CharFilter(field_name='sensor__model', lookup_expr='icontains', label="Sensor Model")
    sensor_type = django_filters.ChoiceFilter(field_name='sensor__type', choices=SensorType.choices, label="Sensor Type")
    sensor_status = django_filters.ChoiceFilter(field_name='sensor__status', choices=SensorStatus.choices, label="Sensor Status")
    sensor_unit = django_filters.ChoiceFilter(field_name='sensor__unit', choices=UnitType.choices, label="Sensor Unit")

    class Meta:
        model = StationSensor
        fields = {
            'position': ['exact', 'iexact', 'contains', 'icontains'],
            'is_active': ['exact'],

            'installed_date': ['exact', 'gt', 'gte', 'lt', 'lte'],
            'removed_date': ['exact', 'gt', 'gte', 'lt', 'lte'],
            'calibrated_at': ['exact', 'gt', 'gte', 'lt', 'lte'],
            'created_at': ['exact', 'gt', 'gte', 'lt', 'lte'],
            'updated_at': ['exact', 'gt', 'gte', 'lt', 'lte'],

            'station__id': ['exact'],
            'station__name': ['exact', 'iexact', 'contains', 'icontains'],
            'station__status': ['exact', 'in'], 
            'station__model': ['exact', 'iexact', 'contains', 'icontains'], 

            'sensor__id': ['exact'], 
            'sensor__model': ['exact', 'iexact', 'contains', 'icontains'],
            'sensor__type': ['exact', 'in'], 
            'sensor__status': ['exact', 'in'], 
            'sensor__unit': ['exact', 'in'], 
        }