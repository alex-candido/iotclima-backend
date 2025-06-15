# django_app/container.py

from .modules.v1.users.container import UsersContainer
from .modules.v1.places.container import PlacesContainer
from .modules.v1.stations.container import StationsContainer
from .modules.v1.sensors.container import SensorsContainer
from dependency_injector import containers, providers



class CoreContainer(containers.DeclarativeContainer):
    sensors_container = providers.Container(SensorsContainer)
    stations_container = providers.Container(StationsContainer)
    places_container = providers.Container(PlacesContainer)
    users_container = providers.Container(UsersContainer)
    
    config = providers.Configuration()

core_container = CoreContainer()


