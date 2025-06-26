import django_filters
from django.db.models import Q

from django_app.modules.v1.sensors.models import (SensorStatus, SensorType, UnitType)

from .models import Event, EventCategory, EventSeverity, EventStatus, EventType


class EventFilter(django_filters.FilterSet):
    occurred_at = django_filters.DateTimeFromToRangeFilter()
    resolved_at = django_filters.DateTimeFromToRangeFilter()
    created_at = django_filters.DateTimeFromToRangeFilter()
    updated_at = django_filters.DateTimeFromToRangeFilter()

    type = django_filters.ChoiceFilter(choices=EventType.choices)
    category = django_filters.ChoiceFilter(choices=EventCategory.choices)
    severity = django_filters.ChoiceFilter(choices=EventSeverity.choices)
    status = django_filters.ChoiceFilter(choices=EventStatus.choices)

    user_id = django_filters.NumberFilter(field_name='user__id', label="User ID")
    station_sensor_id = django_filters.NumberFilter(field_name='station_sensor__id', label="StationSensor ID")

    search_term = django_filters.CharFilter(method='filter_by_search_term')

    def filter_by_search_term(self, queryset, name, value):
        if value:
            return queryset.filter(
                Q(title__icontains=value) |
                Q(description__icontains=value) |
                Q(station_sensor__position__icontains=value) |
                Q(station_sensor__station__name__icontains=value) |
                Q(station_sensor__station__description__icontains=value) |
                Q(station_sensor__station__model__icontains=value) |
                Q(station_sensor__sensor__model__icontains=value) |
                Q(station_sensor__sensor__name__icontains=value) |
                Q(station_sensor__sensor__description__icontains=value)
            )
        return queryset

    is_active = django_filters.BooleanFilter(label="Is Active Event")

    class Meta:
        model = Event
        fields = {
            'title': ['exact', 'iexact', 'contains', 'icontains', 'startswith', 'istartswith', 'endswith', 'iendswith'],
            'description': ['exact', 'iexact', 'contains', 'icontains', 'startswith', 'istartswith', 'endswith', 'iendswith'],

            'occurred_at': ['exact', 'gt', 'gte', 'lt', 'lte'],
            'resolved_at': ['exact', 'gt', 'gte', 'lt', 'lte'],
            'created_at': ['exact', 'gt', 'gte', 'lt', 'lte'],
            'updated_at': ['exact', 'gt', 'gte', 'lt', 'lte'],

            'type': ['exact', 'in'],
            'category': ['exact', 'in'],
            'severity': ['exact', 'in'],
            'status': ['exact', 'in'],

            'user_id': ['exact'],
            'station_sensor_id': ['exact'],
        }