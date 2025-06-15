# django_app/modules/v1/station_sensors/services.py

from rest_framework.exceptions import ValidationError

from .filters import StationSensorFilter
from .repositories import StationSensorRepository


class StationSensorService:
    def __init__(self, repository: StationSensorRepository):
        self.repository = repository

    def list(self, query_params=None):
        queryset = self.repository.list()
        
        if query_params:
            filterset = StationSensorFilter(query_params, queryset=queryset)
            if not filterset.is_valid():
                raise ValidationError(filterset.errors) 
            
            queryset = filterset.qs
        return queryset

    def create(self, input_data):
        station_sensor = self.repository.create(input_data)
        return station_sensor

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