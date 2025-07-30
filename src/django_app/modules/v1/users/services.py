# django_app/modules/v1/users/services.py

from typing import Any, Union
from django.contrib.auth import get_user_model
from django.db.models import QuerySet
from rest_framework.request import QueryDict
from .filters import UsersFilter
from rest_framework.exceptions import ValidationError 
from .repositories import UsersRepository

User = get_user_model()

class UsersService:
    def __init__(self, repository: UsersRepository):
        self.repository = repository

    def list(self, query_params: QueryDict):
        queryset = self.repository.list() 
        total_count = queryset.count()
        
        filterset = UsersFilter(data=query_params, queryset=queryset)
        
        if not filterset.is_valid():
            raise ValidationError(filterset.errors)
        
        filtered_queryset = filterset.qs.order_by('id') 
        
        return filtered_queryset, total_count
    
    def create(self, input_data):
        return self.repository.create(input_data)

    def retrieve(self, pk):
        return self.repository.get(pk)

    def update(self, pk, input_data):
        instance = self.repository.get(pk)
        return self.repository.update(instance, input_data)

    def delete(self, pk):
        instance = self.repository.get(pk)
        self.repository.delete(instance)

    def get_instance(self, pk):
        return self.repository.get(pk)
