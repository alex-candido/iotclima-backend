from rest_framework.exceptions import ValidationError

from .filters import LogFilter
from .repositories import LogsRepository


class LogsService:
    def __init__(self, repository: LogsRepository):
        self.repository = repository

    def list(self, query_params=None):
        queryset = self.repository.list()
        
        if query_params:
            filterset = LogFilter(query_params, queryset=queryset)
            if not filterset.is_valid():
                raise ValidationError(filterset.errors) 
            
            queryset = filterset.qs
        return queryset

    def create(self, input_data):
        log = self.repository.create(input_data)
        return log

    def retrieve(self, pk):
        return self.repository.get(pk)

    def update(self, pk, input_data):
        instance = self.repository.get(pk)
        updated_instance = self.repository.update(instance, input_data)
        return updated_instance

    def delete(self, pk):
        instance = self.repository.get(pk)
        instance.delete()

    def get_instance(self, pk):
        return self.repository.get(pk)