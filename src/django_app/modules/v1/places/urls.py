# django_app/modules/v1/places/urls.py

from rest_framework.routers import DefaultRouter
from .api import PlacesViewSet

router = DefaultRouter()
router.register(r'', PlacesViewSet, basename='places')

urlpatterns = router.urls
