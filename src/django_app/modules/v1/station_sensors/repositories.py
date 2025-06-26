# django_app/modules/v1/station_sensors/repositories.py

from django.core.exceptions import ObjectDoesNotExist
from .models import StationSensor
from typing import Any, Dict, Union, Type
from uuid import UUID

class StationSensorRepository:

    def list(self):
        return StationSensor.objects.all()

    def create(self, validated_data):
        return StationSensor.objects.create(**validated_data)

    def get(self, pk: Union[int, str, UUID]):
        try:
            uuid_obj = UUID(str(pk))
            return StationSensor.objects.get(uuid=uuid_obj)
        except (ValueError, ObjectDoesNotExist):
            return StationSensor.objects.get(id=pk)  

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    def delete(self, instance):
        instance.is_active = False
        instance.save()
