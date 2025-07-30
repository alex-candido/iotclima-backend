# django_app/modules/v1/station_sensors/urls.py

from rest_framework.routers import DefaultRouter

from .api import StationSensorViewSet

router = DefaultRouter()
router.register(r'', StationSensorViewSet, basename='station_sensors')

urlpatterns = router.urls
