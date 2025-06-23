# django_app/modules/v1/places/repositories.py

from django.core.exceptions import ObjectDoesNotExist
from .models import Place, Status
from typing import Any, Dict, Union, Type
from uuid import UUID

class PlacesRepository:

    def list(self):
        return Place.objects.all()

    def create(self, validated_data):
        return Place.objects.create(**validated_data)

    def get(self, pk: Union[int, str, UUID]):
        try:
            uuid_obj = UUID(str(pk))
            return Place.objects.get(uuid=uuid_obj)
        except (ValueError, ObjectDoesNotExist):
            return Place.objects.get(id=pk)  

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    def delete(self, instance):
        instance.status = Status.INACTIVE
        instance.save()
