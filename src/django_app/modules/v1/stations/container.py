# django_app/modules/v1/stations/container.py

from dependency_injector import containers, providers

from .repositories import StationsRepository
from .services import StationsService


class StationsContainer(containers.DeclarativeContainer):
    repository = providers.Factory(StationsRepository)
    service = providers.Factory(StationsService, repository=repository)
