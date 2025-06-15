# django_app/container.py

from .modules.v1.users.container import UsersContainer
from .modules.v1.places.container import PlacesContainer
from dependency_injector import containers, providers



class CoreContainer(containers.DeclarativeContainer):
    places_container = providers.Container(PlacesContainer)
    users_container = providers.Container(UsersContainer)
    
    config = providers.Configuration()

core_container = CoreContainer()


