import django_filters
from django.db.models import Q

from django_app.modules.v1.sensors.models import (SensorStatus, SensorType, UnitType)
from django_app.modules.v1.stations.models import StationStatus

from .models import StationSensor


class StationSensorFilter(django_filters.FilterSet):
    installed_date = django_filters.DateTimeFromToRangeFilter()
    removed_date = django_filters.DateTimeFromToRangeFilter()
    calibrated_at = django_filters.DateTimeFromToRangeFilter()
    created_at = django_filters.DateTimeFromToRangeFilter()
    updated_at = django_filters.DateTimeFromToRangeFilter()

    is_active = django_filters.BooleanFilter(label="Is Active")

    station_id = django_filters.NumberFilter(field_name='station__id', label="Station ID")
    station_name = django_filters.CharFilter(field_name='station__name', lookup_expr='icontains', label="Station Name")
    station_status = django_filters.ChoiceFilter(field_name='station__status', choices=StationStatus.choices, label="Station Status")

    sensor_id = django_filters.NumberFilter(field_name='sensor__id', label="Sensor ID")
    sensor_model = django_filters.CharFilter(field_name='sensor__model', lookup_expr='icontains', label="Sensor Model")
    sensor_type = django_filters.ChoiceFilter(field_name='sensor__type', choices=SensorType.choices, label="Sensor Type")
    sensor_status = django_filters.ChoiceFilter(field_name='sensor__status', choices=SensorStatus.choices, label="Sensor Status")
    sensor_unit = django_filters.ChoiceFilter(field_name='sensor__unit', choices=UnitType.choices, label="Sensor Unit")

    search_term = django_filters.CharFilter(method='filter_by_search_term')

    def filter_by_search_term(self, queryset, name, value):
        if value:
            return queryset.filter(
                Q(position__icontains=value) |
                Q(station__name__icontains=value) |
                Q(station__description__icontains=value) |
                Q(station__model__icontains=value) |
                Q(station__firmware__icontains=value) |
                Q(sensor__model__icontains=value) |
                Q(sensor__name__icontains=value) |
                Q(sensor__description__icontains=value)
            )
        return queryset


    class Meta:
        model = StationSensor
        fields = {
            'position': ['exact', 'iexact', 'contains', 'icontains'],

            'installed_date': ['exact', 'gt', 'gte', 'lt', 'lte'],
            'removed_date': ['exact', 'gt', 'gte', 'lt', 'lte'],
            'calibrated_at': ['exact', 'gt', 'gte', 'lt', 'lte'],
            'created_at': ['exact', 'gt', 'gte', 'lt', 'lte'],
            'updated_at': ['exact', 'gt', 'gte', 'lt', 'lte'],
            
            'station_id': ['exact'],
            'is_active': [],
        }