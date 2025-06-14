# django_app/modules/v1/users/repositories.py

from .models import User


class UsersRepository:

    def list(self):
        return User.objects.all()

    def create(self, validated_data):
        return User.objects.create(**validated_data)

    def get(self, pk):
        return User.objects.get(pk=pk)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    def delete(self, instance):
        instance.delete()
