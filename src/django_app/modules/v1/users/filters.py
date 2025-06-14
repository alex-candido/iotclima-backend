# django_app/modules/v1/users/filters.py

import django_filters


class UsersFilter(django_filters.FilterSet):
    username = django_filters.CharFilter(lookup_expr='icontains')
    email = django_filters.CharFilter(lookup_expr='icontains') 
    first_name = django_filters.CharFilter(lookup_expr='icontains')
    last_name = django_filters.CharFilter(lookup_expr='icontains')
    date_joined = django_filters.DateFromToRangeFilter()
    last_login = django_filters.DateTimeFromToRangeFilter()
