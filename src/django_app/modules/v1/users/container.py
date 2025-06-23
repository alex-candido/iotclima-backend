# django_app/modules/v1/users/container.py

from dependency_injector import containers, providers
from django.contrib.auth import get_user_model

from .repositories import UsersRepository
from .services import UsersService

User = get_user_model()

class UsersContainer(containers.DeclarativeContainer):
    user_model = providers.Object(User)
    repository = providers.Factory(UsersRepository, model=user_model)
    service = providers.Factory(UsersService, repository=repository)
