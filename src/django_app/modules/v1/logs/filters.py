# django_app/modules/v1/logs/filters.py

import django_filters
from django.db import \
    models  # Necessário para filter_overrides (se houver outros)

from .models import Log, LogSeverity


class LogFilter(django_filters.FilterSet):
    created_at = django_filters.DateTimeFromToRangeFilter()
    updated_at = django_filters.DateTimeFromToRangeFilter()

    level = django_filters.ChoiceFilter(choices=LogSeverity.choices)
    
    user_id = django_filters.NumberFilter(field_name='user__id', label="User ID")
    station_id = django_filters.NumberFilter(field_name='station__id', label="Station ID")


    class Meta:
        model = Log
        fields = {
            'message': ['exact', 'iexact', 'contains', 'icontains', 'startswith', 'istartswith', 'endswith', 'iendswith'],
            
            'created_at': ['exact', 'gt', 'gte', 'lt', 'lte'],
            'updated_at': ['exact', 'gt', 'gte', 'lt', 'lte'],

            'level': ['exact', 'in'],

            'user__id': ['exact'],
            'station__id': ['exact'],
        }