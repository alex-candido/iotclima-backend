# django_app/modules/v1/users/filters.py

import django_filters
from django_app.modules.v1.users.models import User 
from django.db.models import Q

class UsersFilter(django_filters.FilterSet):
    group_name = django_filters.BaseInFilter(field_name='groups__name', lookup_expr='in')
    search_term = django_filters.CharFilter(method='filter_by_search_term')
    
    def filter_by_search_term(self, queryset, name, value):
        if value:
            return queryset.filter(
                Q(username__icontains=value) |
                Q(email__icontains=value) |
                Q(first_name__icontains=value) |
                Q(last_name__icontains=value)
            )
        return queryset

    class Meta:
        model = User
        fields = {
            'username': ['exact', 'iexact', 'contains', 'icontains', 'startswith', 'istartswith', 'endswith', 'iendswith'],
            'email': ['exact', 'iexact', 'contains', 'icontains'],
            'first_name': ['exact', 'icontains'],
            'last_name': ['exact', 'icontains'],
            'date_joined': ['exact', 'gt', 'gte', 'lt', 'lte', 'range'],
            'last_login': ['exact', 'gt', 'gte', 'lt', 'lte', 'range', 'isnull'],
        }
