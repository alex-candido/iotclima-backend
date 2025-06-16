# django_app/modules/v1/logs/models.py

import uuid

from django.conf import settings
from django.db import models

from django_app.modules.v1.stations.models import Station


class LogSeverity(models.IntegerChoices):
    DEBUG = 1, 'Debug'
    INFO = 2, 'Info'
    WARN = 3, 'Warn'
    ERROR = 4, 'Error'


class Log(models.Model):
    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)

    message = models.TextField()
    level = models.IntegerField(
        choices=LogSeverity.choices,
        default=LogSeverity.INFO
    )
    
    metadata = models.JSONField(default=dict, blank=True, null=True)

    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL, 
        null=True,
        blank=True, 
        related_name='logs'
    )

    station = models.ForeignKey(
        Station,
        on_delete=models.SET_NULL, 
        null=True,
        blank=True, 
        related_name='logs'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at'] 

    def __str__(self):
        return f"[{self.get_level_display()}] {self.message[:50]}..." # type: ignore