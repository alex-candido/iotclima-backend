# django_app/modules/v1/stations/urls.py

from rest_framework.routers import DefaultRouter
from .api import StationsViewSet

router = DefaultRouter()
router.register(r'', StationsViewSet, basename='stations')

urlpatterns = router.urls
