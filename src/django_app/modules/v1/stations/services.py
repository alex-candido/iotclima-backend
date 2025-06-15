# django_app/modules/v1/stations/services.py

from rest_framework.exceptions import ValidationError

from .filters import StationFilter
from .repositories import StationsRepository


class StationsService:
    def __init__(self, repository: StationsRepository):
        self.repository = repository

    def list(self, query_params=None):
        queryset = self.repository.list()
        
        if query_params:
            filterset = StationFilter(query_params, queryset=queryset)
            if not filterset.is_valid():
                raise ValidationError(filterset.errors) 
            
            queryset = filterset.qs
        return queryset

    def create(self, input_data):
        station = self.repository.create(input_data)
        return station

    def retrieve(self, pk):
        return self.repository.get(pk)

    def update(self, pk, input_data):
        instance = self.repository.get(pk)
        updated_instance = self.repository.update(instance, input_data)
        return updated_instance

    def delete(self, pk):
        instance = self.repository.get(pk)
        self.repository.delete(instance)

    def get_instance(self, pk):
        return self.repository.get(pk)