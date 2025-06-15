# django_app/modules/v1/stations/filters.py

import django_filters

from .models import Station, StationStatus


class StationFilter(django_filters.FilterSet):
    installed_at = django_filters.DateTimeFromToRangeFilter()
    last_maintenance_at = django_filters.DateTimeFromToRangeFilter()
    next_maintenance_at = django_filters.DateTimeFromToRangeFilter()
    created_at = django_filters.DateTimeFromToRangeFilter()
    updated_at = django_filters.DateTimeFromToRangeFilter()

    status = django_filters.ChoiceFilter(choices=StationStatus.choices)

    place_id = django_filters.NumberFilter(field_name='place__id', lookup_expr='exact', label="Place ID")
    user_id = django_filters.NumberFilter(field_name='user__id', lookup_expr='exact', label="User ID")


    class Meta:
        model = Station
        fields = {
            'name': ['exact', 'iexact', 'contains', 'icontains', 'startswith', 'istartswith', 'endswith', 'iendswith'],
            'description': ['exact', 'iexact', 'contains', 'icontains', 'startswith', 'istartswith', 'endswith', 'iendswith'],
            'model': ['exact', 'iexact', 'contains', 'icontains', 'startswith', 'istartswith', 'endswith', 'iendswith'],
            'firmware': ['exact', 'iexact', 'contains', 'icontains', 'startswith', 'istartswith', 'endswith', 'iendswith'],
            
            'battery_level': ['exact', 'lt', 'lte', 'gt', 'gte'],
            'signal_strength': ['exact', 'lt', 'lte', 'gt', 'gte'],

            'installed_at': ['exact', 'gt', 'gte', 'lt', 'lte'],
            'last_maintenance_at': ['exact', 'gt', 'gte', 'lt', 'lte'],
            'next_maintenance_at': ['exact', 'gt', 'gte', 'lt', 'lte'],
            'created_at': ['exact', 'gt', 'gte', 'lt', 'lte'],
            'updated_at': ['exact', 'gt', 'gte', 'lt', 'lte'],
        }