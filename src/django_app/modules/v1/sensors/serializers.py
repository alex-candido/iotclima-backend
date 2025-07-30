# django_app/modules/v1/sensors/serializers.py

from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Sensor, SensorStatus, SensorType, UnitType

User = get_user_model()


class SensorsInputSerializer(serializers.Serializer):
    type = serializers.ChoiceField(choices=SensorType.choices)
    model = serializers.CharField(max_length=255)
    
    unit = serializers.ChoiceField(choices=UnitType.choices)
    min_value = serializers.FloatField()
    max_value = serializers.FloatField()
    
    status = serializers.ChoiceField(choices=SensorStatus.choices, default=SensorStatus.ACTIVE)
    
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        required=False,
        allow_null=True
    )

class SensorsOutputSerializer(serializers.ModelSerializer):
    type_display = serializers.CharField(source='get_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    unit_display = serializers.CharField(source='get_unit_display', read_only=True)

    user_username = serializers.CharField(source='user.username', read_only=True, required=False, allow_null=True)
    user_email = serializers.CharField(source='user.email', read_only=True, required=False, allow_null=True)

    class Meta:
        model = Sensor
        fields = (
            'id', 'uuid', 'type', 'type_display', 'model', 
            'unit', 'unit_display', 'min_value', 'max_value', 
            'status', 'status_display',
            'user', 'user_username', 'user_email',
            'created_at', 'updated_at'
        )