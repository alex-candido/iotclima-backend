import django_filters
from django.db.models import Q

from django_app.modules.v1.stations.models import StationStatus
from .models import Record, Status


class RecordFilter(django_filters.FilterSet):
    recorded_at = django_filters.DateTimeFromToRangeFilter()
    created_at = django_filters.DateTimeFromToRangeFilter()
    updated_at = django_filters.DateTimeFromToRangeFilter()

    status = django_filters.ChoiceFilter(choices=Status.choices)

    temperature = django_filters.NumberFilter()
    humidity = django_filters.NumberFilter()
    wind_speed = django_filters.NumberFilter()
    wind_direction = django_filters.NumberFilter()
    pressure = django_filters.NumberFilter()
    rainfall = django_filters.NumberFilter()

    station_id = django_filters.NumberFilter(field_name='station__id', label="Station ID")
    station_name = django_filters.CharFilter(field_name='station__name', lookup_expr='icontains', label="Station Name")
    station_model = django_filters.CharFilter(field_name='station__model', lookup_expr='icontains', label="Station Model")
    station_firmware = django_filters.CharFilter(field_name='station__firmware', lookup_expr='icontains', label="Station Firmware")

    station_status = django_filters.ChoiceFilter(field_name='station__status', choices=StationStatus.choices, label="Station Status")

    search_term = django_filters.CharFilter(method='filter_by_search_term')

    def filter_by_search_term(self, queryset, name, value):
        if value:
            return queryset.filter(
                Q(station__name__icontains=value) |
                Q(station__description__icontains=value) |
                Q(station__model__icontains=value) |
                Q(station__firmware__icontains=value)
            )
        return queryset


    class Meta:
        model = Record
        fields = {
            'recorded_at': ['exact', 'gt', 'gte', 'lt', 'lte'],
            'created_at': ['exact', 'gt', 'gte', 'lt', 'lte'],
            'updated_at': ['exact', 'gt', 'gte', 'lt', 'lte'],

            'temperature': ['exact', 'gt', 'gte', 'lt', 'lte'],
            'humidity': ['exact', 'gt', 'gte', 'lt', 'lte'],
            'wind_speed': ['exact', 'gt', 'gte', 'lt', 'lte'],
            'wind_direction': ['exact'],
            'pressure': ['exact', 'gt', 'gte', 'lt', 'lte'],
            'rainfall': ['exact', 'gt', 'gte', 'lt', 'lte'],

            'status': ['exact', 'in'],
            'station_id': ['exact'],
        }