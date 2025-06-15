# django_app/routes.py

from django.urls import include, path

urlpatterns = [
    path('station_sensors/', include('django_app.modules.v1.station_sensors.urls')),
    path('sensors/', include('django_app.modules.v1.sensors.urls')),
    path('stations/', include('django_app.modules.v1.stations.urls')),
    path('places/', include('django_app.modules.v1.places.urls')),
    path('users/', include('django_app.modules.v1.users.urls')),
    path('auth/', include('django_app.modules.v1.auth.urls')),
]