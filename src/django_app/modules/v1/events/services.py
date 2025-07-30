# django_app/modules/v1/events/services.py

from rest_framework.exceptions import ValidationError
from rest_framework.request import QueryDict
from .filters import EventFilter
from .repositories import EventsRepository


class EventsService:
    def __init__(self, repository: EventsRepository):
        self.repository = repository

    def list(self, query_params: QueryDict):
        queryset = self.repository.list() 
        filterset = EventFilter(data=query_params, queryset=queryset)
        
        if not filterset.is_valid():
            raise ValidationError(filterset.errors) 
            
        filtered_queryset = filterset.qs.order_by('id') 
        total_count = queryset.count()
        return filtered_queryset, total_count

    def create(self, input_data):
        event = self.repository.create(input_data)
        return event

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