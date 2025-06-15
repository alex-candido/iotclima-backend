# django_app/modules/v1/station_sensors/container.py

from dependency_injector import containers, providers

from .repositories import StationSensorRepository
from .services import StationSensorService


class StationSensorsContainer(containers.DeclarativeContainer):
    repository = providers.Factory(StationSensorRepository)
    service = providers.Factory(StationSensorService, repository=repository)
