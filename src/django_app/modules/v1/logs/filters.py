# django_app/modules/v1/logs/filters.py

import django_filters
from django.db.models import Q

from .models import Log, LogSeverity


class LogFilter(django_filters.FilterSet):
    created_at = django_filters.DateTimeFromToRangeFilter()
    updated_at = django_filters.DateTimeFromToRangeFilter()

    level = django_filters.ChoiceFilter(choices=LogSeverity.choices)

    user_id = django_filters.NumberFilter(field_name='user__id', label="User ID")
    station_id = django_filters.NumberFilter(field_name='station__id', label="Station ID")

    search_term = django_filters.CharFilter(method='filter_by_search_term')

    def filter_by_search_term(self, queryset, name, value):
        if value:
            return queryset.filter(
                Q(message__icontains=value) |
                Q(level__icontains=value) | 
                Q(user__username__icontains=value) |
                Q(station__name__icontains=value)
            )
        return queryset

    is_active = django_filters.BooleanFilter(label="Is Active Log")

    class Meta:
        model = Log
        fields = {
            'message': ['exact', 'iexact', 'contains', 'icontains', 'startswith', 'istartswith', 'endswith', 'iendswith'],

            'created_at': ['exact', 'gt', 'gte', 'lt', 'lte'],
            'updated_at': ['exact', 'gt', 'gte', 'lt', 'lte'],

            'level': ['exact', 'in'],

            'user_id': ['exact'],
            'station_id': ['exact'],
        }