# django_app/modules/v1/records/models.py

import uuid

from django.db import models

from django_app.modules.v1.stations.models import Station


class Status(models.IntegerChoices):
    ACTIVE = 1, 'Active'
    INACTIVE = 0, 'Inactive'


class Record(models.Model):
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)

    recorded_at = models.DateTimeField()
    
    temperature = models.FloatField(null=True, blank=True)
    humidity = models.FloatField(null=True, blank=True)
    wind_speed = models.FloatField(null=True, blank=True)
    wind_direction = models.FloatField(null=True, blank=True)
    pressure = models.FloatField(null=True, blank=True)
    rainfall = models.FloatField(null=True, blank=True)
    
    status = models.IntegerField(
        choices=Status.choices,
        default=Status.ACTIVE
    )
    
    station = models.ForeignKey(
        Station,
        on_delete=models.CASCADE, 
        related_name='records' 
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-recorded_at'] 

    def __str__(self):
        return f"Record for {self.station.name} at {self.recorded_at.strftime('%Y-%m-%d %H:%M')}"