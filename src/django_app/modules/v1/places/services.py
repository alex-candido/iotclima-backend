# django_app/modules/v1/places/services.py

from django.contrib.gis.db.models import GeometryField
from django.contrib.gis.db.models.functions import Centroid, Distance
from django.contrib.gis.geos import Point
from django.db.models import Aggregate
from rest_framework.exceptions import ValidationError

from django_app.modules.v1.users.repositories import UsersRepository

from .filters import PlaceFilter
from .repositories import PlacesRepository


class CustomConvexhull(Aggregate):
    function = 'ST_ConvexHull'
    template = '%(function)s(%(expressions)s)'
    output_field_class = GeometryField 

class PlacesService:
    def __init__(self, repository: PlacesRepository, users_repository: UsersRepository):
        self.repository = repository
        self.users_repository = users_repository

    # --- CRUD Methods ---
    def list(self, query_params=None):
        queryset = self.repository.list()
        
        if query_params:
            filterset = PlaceFilter(query_params, queryset=queryset)
            if filterset.is_valid():
                queryset = filterset.qs
            else:
                raise ValidationError(filterset.errors)

        return queryset

    def create(self, input_data):
        latitude = input_data.pop('latitude', None)
        longitude = input_data.pop('longitude', None)
        
        place = self.repository.create(input_data)

        if latitude is not None and longitude is not None:
            place.set_location(latitude, longitude)
            place.save()

        return place

    def retrieve(self, pk):
        return self.repository.get(pk)

    def update(self, pk, input_data):
        instance = self.repository.get(pk)

        latitude = input_data.pop('latitude', None)
        longitude = input_data.pop('longitude', None)
        
        updated_instance = self.repository.update(instance, input_data)
        
        if latitude is not None and longitude is not None:
            updated_instance.set_location(latitude, longitude)
            updated_instance.save()

        return updated_instance

    def delete(self, pk):
        instance = self.repository.get(pk)
        self.repository.delete(instance)

    def get_instance(self, pk):
        return self.repository.get(pk)

    # --- Geospatial Analytics and Aggregation Methods (Following g_ Pattern) ---

    def g_centroid(self):
        queryset = self.repository.list().annotate(
            centroid_location=Centroid('location')
        )
        return queryset
    
    def g_convex_hull(self):
        convex_hull_geom = self.repository.list().aggregate(
            overall_hull=CustomConvexhull('location') 
        ).get('overall_hull')
        
        return convex_hull_geom

    def g_k_nearest(self, ref_latitude: float, ref_longitude: float, k: int):
        ref_point = Point(ref_longitude, ref_latitude, srid=4326)
        
        queryset = self.repository.list().annotate(
            distance_km=Distance('location', ref_point, spheroid=True)
        ).order_by('distance_km')[:k]
        
        return queryset