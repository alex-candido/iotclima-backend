# django_app/modules/v1/places/container.py

from dependency_injector import containers, providers

from django_app.modules.v1.users.repositories import UsersRepository

from .repositories import PlacesRepository
from .services import PlacesService


class PlacesContainer(containers.DeclarativeContainer):
    repository = providers.Factory(PlacesRepository)
    users_repository = providers.Factory(UsersRepository) 

    service = providers.Factory(PlacesService, repository=repository, users_repository=users_repository)
