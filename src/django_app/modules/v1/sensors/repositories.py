# django_app/modules/v1/sensors/repositories.py

from django.core.exceptions import ObjectDoesNotExist
from .models import Sensor, SensorStatus
from typing import Any, Dict, Union, Type
from uuid import UUID

class SensorsRepository:

    def list(self):
        return Sensor.objects.all()

    def create(self, validated_data):
        return Sensor.objects.create(**validated_data)

    def get(self, pk: Union[int, str, UUID]):
        try:
            uuid_obj = UUID(str(pk))
            return Sensor.objects.get(uuid=uuid_obj)
        except (ValueError, ObjectDoesNotExist):
            return Sensor.objects.get(id=pk)  

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    def delete(self, instance):
        instance.status = SensorStatus.INACTIVE
        instance.save()
