# django_app/modules/v1/Stations/repositories.py

from django.core.exceptions import ObjectDoesNotExist
from .models import Station, StationStatus
from typing import Any, Dict, Union, Type
from uuid import UUID

class StationsRepository:

    def list(self):
        return Station.objects.all()

    def create(self, validated_data):
        return Station.objects.create(**validated_data)
    
    def get(self, pk: Union[int, str, UUID]):
        try:
            uuid_obj = UUID(str(pk))
            return Station.objects.get(uuid=uuid_obj)
        except (ValueError, ObjectDoesNotExist):
            return Station.objects.get(id=pk)  

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    def delete(self, instance):
        instance.status = StationStatus.INACTIVE 
        instance.save()
