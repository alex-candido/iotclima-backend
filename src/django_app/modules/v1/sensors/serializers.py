# django_app/modules/v1/sensors/serializers.py

from rest_framework import serializers
from .models import Sensors


class SensorsInputSerializer(serializers.Serializer):
    uuid = serializers.CharField()  # Tipo UUIDField não reconhecido
    type = serializers.CharField()  # Tipo IntegerField;model=CharField não reconhecido
    min_value = serializers.CharField()  # Tipo FloatField;max_value=FloatField;calibrated_at=DateTimeField não reconhecido
    status = serializers.CharField()  # Tipo IntegerField;station=ForeignKey não reconhecido
    user = serializers.CharField()  # Tipo ForeignKey não reconhecido
    created_at = serializers.CharField()  # Tipo DateTimeField não reconhecido
    updated_at = serializers.CharField()  # Tipo DateTimeField não reconhecido


class SensorsOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensors
        fields = '__all__'
