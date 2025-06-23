# django_app/modules/v1/users/repositories.py
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model
from django.db.models import QuerySet
from typing import Any, Dict, Union, Type
from uuid import UUID

User = get_user_model()

class UsersRepository:
    def __init__(self, model: Type[Any] = User):
        self.model = model
        
    def _get_base_queryset(self):
        return self.model.objects.all().prefetch_related(
            'groups',
            'user_permissions',
            'user_permissions__content_type'
        )

    def list(self):
        return self._get_base_queryset()

    def create(self, validated_data):
        return self.model.objects.create(**validated_data)

    def get(self, pk: Union[int, str, UUID]):
        try:
            uuid_obj = UUID(str(pk))
            return self._get_base_queryset().get(uuid=uuid_obj)
        except (ValueError, ObjectDoesNotExist):
            return self._get_base_queryset().get(id=pk)  

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    def delete(self, instance):
        instance.is_active = False
        instance.save()
