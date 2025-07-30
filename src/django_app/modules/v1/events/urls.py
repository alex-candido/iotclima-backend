# django_app/modules/v1/events/urls.py

from rest_framework.routers import DefaultRouter
from .api import EventsViewSet

router = DefaultRouter()
router.register(r'', EventsViewSet, basename='events')

urlpatterns = router.urls
