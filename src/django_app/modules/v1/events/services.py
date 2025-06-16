# django_app/modules/v1/events/services.py

from rest_framework.exceptions import ValidationError

from .filters import EventFilter
from .repositories import EventsRepository


class EventsService:
    def __init__(self, repository: EventsRepository):
        self.repository = repository

    def list(self, query_params=None):
        queryset = self.repository.list()
        
        if query_params:
            filterset = EventFilter(query_params, queryset=queryset)
            if not filterset.is_valid():
                raise ValidationError(filterset.errors) 
            
            queryset = filterset.qs
        return queryset

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