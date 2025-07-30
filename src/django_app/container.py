# django_app/container.py

from .modules.v1.records.container import RecordsContainer
from .modules.v1.events.container import EventsContainer
from .modules.v1.logs.container import LogsContainer
from dependency_injector import containers, providers

from .modules.v1.places.container import PlacesContainer
from .modules.v1.sensors.container import SensorsContainer
from .modules.v1.station_sensors.container import StationSensorsContainer
from .modules.v1.stations.container import StationsContainer
from .modules.v1.users.container import UsersContainer


class CoreContainer(containers.DeclarativeContainer):
    logs_container = providers.Container(LogsContainer)
    events_container = providers.Container(EventsContainer)
    records_container = providers.Container(RecordsContainer)
    station_sensors_container = providers.Container(StationSensorsContainer)
    sensors_container = providers.Container(SensorsContainer)
    stations_container = providers.Container(StationsContainer)
    places_container = providers.Container(PlacesContainer)
    users_container = providers.Container(UsersContainer)
    
    config = providers.Configuration()

core_container = CoreContainer()


