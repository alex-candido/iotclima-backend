# django_app/modules/v1/sensors/apps.py

from django.apps import AppConfig


class SensorsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'django_app.modules.v1.sensors'
    label = 'sensors'
    verbose_name = 'Sensors'
