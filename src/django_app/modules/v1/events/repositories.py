# django_app/modules/v1/events/repositories.py

from django.core.exceptions import ObjectDoesNotExist
from .models import Event, EventStatus
from typing import Any, Dict, Union, Type
from uuid import UUID

class EventsRepository:
    def list(self):
        return Event.objects.all()

    def create(self, validated_data):
        return Event.objects.create(**validated_data)

    def get(self, pk: Union[int, str, UUID]):
        try:
            uuid_obj = UUID(str(pk))
            return Event.objects.get(uuid=uuid_obj)
        except (ValueError, ObjectDoesNotExist):
            return Event.objects.get(id=pk) 

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    def delete(self, instance):
        instance.status = EventStatus.RESOLVED 
        instance.save()