# django_app/modules/v1/events/container.py

from dependency_injector import containers, providers

from .repositories import EventsRepository
from .services import EventsService


class EventsContainer(containers.DeclarativeContainer):
    repository = providers.Factory(EventsRepository)
    service = providers.Factory(EventsService, repository=repository)
