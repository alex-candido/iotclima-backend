# django_app/modules/v1/sensors/container.py

from dependency_injector import containers, providers

from .repositories import SensorsRepository
from .services import SensorsService


class SensorsContainer(containers.DeclarativeContainer):
    repository = providers.Factory(SensorsRepository)
    service = providers.Factory(SensorsService, repository=repository)
