# django_app/modules/v1/logs/repositories.py

from django.core.exceptions import ObjectDoesNotExist
from .models import Log
from typing import Any, Dict, Union, Type
from uuid import UUID

class LogsRepository:
    def list(self):
        return Log.objects.all()

    def create(self, validated_data):
        return Log.objects.create(**validated_data)

    def get(self, pk: Union[int, str, UUID]):
        try:
            uuid_obj = UUID(str(pk))
            return Log.objects.get(uuid=uuid_obj)
        except (ValueError, ObjectDoesNotExist):
            return Log.objects.get(id=pk)  

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    def delete(self, instance):
        instance.delete()