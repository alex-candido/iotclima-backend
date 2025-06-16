# django_app/modules/v1/records/services.py

from rest_framework.exceptions import ValidationError

from .filters import RecordFilter
from .repositories import RecordsRepository


class RecordsService:
    def __init__(self, repository: RecordsRepository):
        self.repository = repository

    def list(self, query_params=None):
        queryset = self.repository.list()
        
        if query_params:
            filterset = RecordFilter(query_params, queryset=queryset)
            if not filterset.is_valid():
                raise ValidationError(filterset.errors) 
            
            queryset = filterset.qs
        return queryset

    def create(self, input_data):
        record = self.repository.create(input_data)
        return record

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