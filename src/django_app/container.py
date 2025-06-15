# django_app/container.py

from dependency_injector import containers, providers

from .modules.v1.places.container import PlacesContainer
from .modules.v1.sensors.container import SensorsContainer
from .modules.v1.station_sensors.container import StationSensorsContainer
from .modules.v1.stations.container import StationsContainer
from .modules.v1.users.container import UsersContainer


class CoreContainer(containers.DeclarativeContainer):
    station_sensors_container = providers.Container(StationSensorsContainer)
    sensors_container = providers.Container(SensorsContainer)
    stations_container = providers.Container(StationsContainer)
    places_container = providers.Container(PlacesContainer)
    users_container = providers.Container(UsersContainer)
    
    config = providers.Configuration()

core_container = CoreContainer()


