# django_app/modules/v1/sensors/models.py

import uuid

from django.conf import settings
from django.db import models


class SensorType(models.IntegerChoices):
    TEMPERATURE = 1, 'Temperature'
    HUMIDITY = 2, 'Humidity'
    WIND = 3, 'Wind'
    PRESSURE = 4, 'Pressure'
    RAINFALL = 5, 'Rainfall'
    OTHER = 6, 'Other'

class SensorStatus(models.IntegerChoices):
    ACTIVE = 1, 'Active'
    INACTIVE = 0, 'Inactive'
    ERROR = 2, 'Error'
    
class UnitType(models.IntegerChoices):
    CELSIUS = 1, 'Celsius'
    FAHRENHEIT = 2, 'Fahrenheit'
    PERCENT = 3, 'Percent' 
    METERS_PER_SECOND = 4, 'Meters/Second' 
    KILOMETERS_PER_HOUR = 5, 'Kilometers/Hour' 
    HECTOPASCAL = 6, 'Hectopascal'
    MILLIMETERS = 7, 'Millimeters'
    OTHER = 8, 'Other Unit'

class Sensor(models.Model):
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)

    model = models.CharField(max_length=255)
    
    unit = models.IntegerField(
        choices=UnitType.choices
    )
    
    min_value = models.FloatField()
    max_value = models.FloatField()
    
    type = models.IntegerField(
        choices=SensorType.choices
    )

    status = models.IntegerField(
        choices=SensorStatus.choices,
        default=SensorStatus.ACTIVE
    )
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='sensors_managed'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.get_type_display()} Sensor ({self.model})" # type: ignore
