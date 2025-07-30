# django_app/modules/v1/station_sensors/models.py

import uuid

from django.db import models

from django_app.modules.v1.sensors.models import Sensor
from django_app.modules.v1.stations.models import Station


class StationSensor(models.Model):
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)

    station = models.ForeignKey(
        Station, 
        on_delete=models.CASCADE,
        related_name='station_sensor_links'
    )
    sensor = models.ForeignKey(
        Sensor, 
        on_delete=models.CASCADE,
        related_name='station_sensor_links' 
    )

    installed_date = models.DateTimeField(null=True, blank=True)
    removed_date = models.DateTimeField(null=True, blank=True)
    position = models.CharField(max_length=100, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    calibrated_at = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = [['station', 'sensor']] 
        
    def __str__(self):
        return f"Station: {self.station.name} | Sensor: {self.sensor.get_type_display()} ({self.sensor.model})" # type: ignore