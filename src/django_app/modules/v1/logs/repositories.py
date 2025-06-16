from .models import Log


class LogsRepository:
    def list(self):
        return Log.objects.all()

    def create(self, validated_data):
        return Log.objects.create(**validated_data)

    def get(self, pk):
        return Log.objects.get(pk=pk)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    def delete(self, instance):
        instance.delete()