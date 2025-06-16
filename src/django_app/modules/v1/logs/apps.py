# django_app/modules/v1/logs/apps.py

from django.apps import AppConfig


class LogsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'django_app.modules.v1.logs'
    label = 'logs'
    verbose_name = 'Logs'
