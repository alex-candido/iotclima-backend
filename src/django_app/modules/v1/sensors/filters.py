import django_filters
from django.db.models import Q

from .models import Sensor, SensorStatus, SensorType, UnitType


class SensorFilter(django_filters.FilterSet):
    created_at = django_filters.DateTimeFromToRangeFilter()
    updated_at = django_filters.DateTimeFromToRangeFilter()

    status = django_filters.ChoiceFilter(choices=SensorStatus.choices)
    type = django_filters.ChoiceFilter(choices=SensorType.choices)
    unit = django_filters.ChoiceFilter(choices=UnitType.choices)

    user_id = django_filters.NumberFilter(field_name='user__id', label="User ID")

    search_term = django_filters.CharFilter(method='filter_by_search_term')

    def filter_by_search_term(self, queryset, name, value):
        if value:
            return queryset.filter(
                Q(name__icontains=value) |
                Q(description__icontains=value) |
                Q(model__icontains=value)
            )
        return queryset

    class Meta:
        model = Sensor
        fields = {
            'model': ['exact', 'iexact', 'contains', 'icontains', 'startswith', 'istartswith', 'endswith', 'iendswith'],

            'min_value': ['exact', 'lt', 'lte', 'gt', 'gte'],
            'max_value': ['exact', 'lt', 'lte', 'gt', 'gte'],

            'type': ['exact', 'in'],
            'status': ['exact', 'in'],
            'unit': ['exact', 'in'],

            'created_at': ['exact', 'gt', 'gte', 'lt', 'lte'],
            'updated_at': ['exact', 'gt', 'gte', 'lt', 'lte'],

            'user_id': ['exact'],
        }