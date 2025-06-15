# django_app/modules/v1/places/repositories.py

from .models import Place


class PlacesRepository:

    def list(self):
        return Place.objects.all()

    def create(self, validated_data):
        return Place.objects.create(**validated_data)

    def get(self, pk):
        return Place.objects.get(pk=pk)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    def delete(self, instance):
        instance.delete()
