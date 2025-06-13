# django_app/container.py

from dependency_injector import containers, providers



class CoreContainer(containers.DeclarativeContainer):
    
    config = providers.Configuration()

core_container = CoreContainer()


