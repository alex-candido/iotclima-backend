# django_app/container.py

from .modules.v1.users.container import UsersContainer
from dependency_injector import containers, providers



class CoreContainer(containers.DeclarativeContainer):
    users_container = providers.Container(UsersContainer)
    
    config = providers.Configuration()

core_container = CoreContainer()


