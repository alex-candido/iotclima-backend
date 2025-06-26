# django_app/modules/v1/sensors/services.py

from rest_framework.exceptions import ValidationError

from .filters import SensorFilter
from .repositories import SensorsRepository


class SensorsService:
    def __init__(self, repository: SensorsRepository):
        self.repository = repository

    def list(self, query_params=None):
        queryset = self.repository.list()
        
        filterset = SensorFilter(data=query_params, queryset=queryset)
        if not filterset.is_valid():
            raise ValidationError(filterset.errors)
        
        filtered_queryset = filterset.qs.order_by('id')
        total_count = filtered_queryset.count() 
        return filtered_queryset, total_count

    def create(self, input_data):
        sensor = self.repository.create(input_data)
        return sensor

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

