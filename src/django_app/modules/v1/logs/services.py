from rest_framework.exceptions import ValidationError

from rest_framework.request import QueryDict
from .filters import LogFilter
from .repositories import LogsRepository


class LogsService:
    def __init__(self, repository: LogsRepository):
        self.repository = repository

    def list(self, query_params: QueryDict):
        queryset = self.repository.list() 
        filterset = LogFilter(data=query_params, queryset=queryset)
        
        if not filterset.is_valid():
            raise ValidationError(filterset.errors) 
            
        filtered_queryset = filterset.qs.order_by('id') 
        total_count = queryset.count()
        return filtered_queryset, total_count

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