# django_app/modules/v1/users/container.py

from dependency_injector import containers, providers

from .repositories import UsersRepository
from .services import UsersService


class UsersContainer(containers.DeclarativeContainer):
    repository = providers.Factory(UsersRepository)
    service = providers.Factory(UsersService, repository=repository)
