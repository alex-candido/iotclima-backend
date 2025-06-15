# django_app/modules/v1/sensors/urls.py

from rest_framework.routers import DefaultRouter
from .api import SensorsViewSet

router = DefaultRouter()
router.register(r'', SensorsViewSet, basename='sensors')

urlpatterns = router.urls
