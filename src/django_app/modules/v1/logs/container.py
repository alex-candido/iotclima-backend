# django_app/modules/v1/logs/container.py

from dependency_injector import containers, providers

from .repositories import LogsRepository
from .services import LogsService


class LogsContainer(containers.DeclarativeContainer):
    repository = providers.Factory(LogsRepository)
    service = providers.Factory(LogsService, repository=repository)
