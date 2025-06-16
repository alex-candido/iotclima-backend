# django_app/modules/v1/records/container.py

from dependency_injector import containers, providers

from .repositories import RecordsRepository
from .services import RecordsService


class RecordsContainer(containers.DeclarativeContainer):
    repository = providers.Factory(RecordsRepository)
    service = providers.Factory(RecordsService, repository=repository)
