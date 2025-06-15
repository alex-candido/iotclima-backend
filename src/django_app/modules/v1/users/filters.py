# django_app/modules/v1/users/filters.py

import django_filters

from .models import User


class UsersFilter(django_filters.FilterSet):    
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
