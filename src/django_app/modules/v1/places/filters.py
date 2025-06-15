# django_app/modules/v1/places/filters.py

import django_filters
from django.contrib.gis.geos import GEOSGeometry, LineString, Point, Polygon

from .models import Place, PlaceType, Status


class PlaceFilter(django_filters.FilterSet):
    
    created_at = django_filters.DateTimeFromToRangeFilter()
    updated_at = django_filters.DateTimeFromToRangeFilter()

    status = django_filters.ChoiceFilter(choices=Status.choices)
    type = django_filters.ChoiceFilter(choices=PlaceType.choices)

    # 1. g_near: Filter places near a point within a given radius.
    #    Usage: ?g_near=lat,lon,radius_km
    g_near = django_filters.CharFilter(method='filter_g_near', label="Near a point (lat,lon,radius_km)")
    def filter_g_near(self, queryset, name, value):
        try:
            lat_str, lon_str, radius_km_str = value.split(',')
            ref_point = Point(float(lon_str), float(lat_str), srid=4326) # Point(longitude, latitude)
            radius_meters = float(radius_km_str) * 1000 # Convert KM to meters
            queryset = queryset.filter(location__distance_lte=(ref_point, radius_meters))

        except (ValueError, IndexError, TypeError): pass # Ignore invalid input
        return queryset

    # 2. g_within_box: Filter places within a bounding box.
    #    Usage: ?g_within_box=min_lon,min_lat,max_lon,max_lat
    g_within_box = django_filters.CharFilter(method='filter_g_within_box', label="Within a bounding box (min_lon,min_lat,max_lon,max_lat)")
    def filter_g_within_box(self, queryset, name, value):
        try:
            min_lon, min_lat, max_lon, max_lat = map(float, value.split(','))
            bbox_polygon = Polygon.from_bbox((min_lon, min_lat, max_lon, max_lat))
            queryset = queryset.filter(location__within=bbox_polygon)
        except (ValueError, IndexError, TypeError): pass
        return queryset

    # 3. g_within_polygon: Filter places within a given WKT polygon.
    #    Usage: ?g_within_polygon=POLYGON((lon1 lat1, lon2 lat2, ...))
    g_within_polygon = django_filters.CharFilter(method='filter_g_within_polygon', label="Within a polygon (WKT)")
    def filter_g_within_polygon(self, queryset, name, value):
        try:
            polygon_geom = GEOSGeometry(value, srid=4326)
            queryset = queryset.filter(location__within=polygon_geom)
        except Exception: pass 
        return queryset
    
    # 4. g_intersects: Filter places intersecting a given WKT geometry.
    #    Usage: ?g_intersects=POINT(lon lat) or LINESTRING(...) or POLYGON(...)
    g_intersects = django_filters.CharFilter(method='filter_g_intersects', label="Intersects WKT Geometry")
    def filter_g_intersects(self, queryset, name, value):
        try:
            geom = GEOSGeometry(value, srid=4326)
            queryset = queryset.filter(location__intersects=geom)
        except Exception: pass
        return queryset

    # 5. g_wkt: Generic filter for WKT (can be redundant with intersects/within, but provided if needed for specific use)
    #    Usage: ?g_wkt=GEOMETRYCOLLECTION(POINT(...), LINESTRING(...)) - filters if location intersects ANY part of WKT
    g_wkt = django_filters.CharFilter(method='filter_g_wkt', label="Intersects any WKT geometry")
    def filter_g_wkt(self, queryset, name, value):
        try:
            geom = GEOSGeometry(value, srid=4326)
            queryset = queryset.filter(location__intersects=geom)
        except Exception: pass
        return queryset

    # 6. g_distance: Filter by explicit distance range (e.g., between X and Y km from a point)
    #    Usage: ?g_distance=lat,lon,min_km,max_km
    g_distance = django_filters.CharFilter(method='filter_g_distance', label="Distance range from point (lat,lon,min_km,max_km)")
    def filter_g_distance(self, queryset, name, value):
        try:
            lat, lon, min_km, max_km = map(float, value.split(','))
            ref_point = Point(lon, lat, srid=4326)
            min_meters = min_km * 1000
            max_meters = max_km * 1000
            # Use __distance_lte and __distance_gte for range
            queryset = queryset.filter(
                location__distance_lte=(ref_point, max_meters),
                location__distance_gte=(ref_point, min_meters)
            )
        except (ValueError, IndexError, TypeError): pass
        return queryset

    # 7. g_buffer: Filter places intersecting a buffer created around a given WKT geometry.
    #    Usage: ?g_buffer=WKT_GEOMETRY,radius_meters
    g_buffer = django_filters.CharFilter(method='filter_g_buffer', label="Intersects buffer around WKT (WKT,radius_meters)")
    def filter_g_buffer(self, queryset, name, value):
        try:
            geom_str, radius_str = value.split(',', 1) # Split only on first comma
            geom = GEOSGeometry(geom_str, srid=4326)
            radius_meters = float(radius_str)
            buffered_geom = geom.buffer(radius_meters) # Create buffer

            queryset = queryset.filter(location__intersects=buffered_geom)
        except Exception: pass
        return queryset
    
    # 8. g_contains: Filter geometries that contain the Place's location.
    #    Usage: ?g_contains=POLYGON(...)
    g_contains = django_filters.CharFilter(method='filter_g_contains', label="Contained by WKT Geometry")
    def filter_g_contains(self, queryset, name, value):
        try:
            container_geom = GEOSGeometry(value, srid=4326)
            queryset = queryset.filter(location__contained=container_geom) # Note: __contained is the inverse of __contains
        except Exception: pass
        return queryset

    # 9. g_along_line: Filter places that are within a certain distance from a given LineString.
    #    Usage: ?g_along_line=LINESTRING(lon1 lat1,...),tolerance_meters
    g_along_line = django_filters.CharFilter(method='filter_g_along_line', label="Along a line (LINESTRING,tolerance_meters)")
    def filter_g_along_line(self, queryset, name, value):
        try:
            line_str, tolerance_str = value.split(',', 1)
            line_geom = GEOSGeometry(line_str, srid=4326)
            tolerance_meters = float(tolerance_str)
            
            # Use __dwithin for geographic distance along a line
            queryset = queryset.filter(location__dwithin=(line_geom, tolerance_meters))
        except Exception: pass
        return queryset


    class Meta:
        model = Place
        fields = {
            'name': ['exact', 'iexact', 'contains', 'icontains', 'startswith', 'istartswith', 'endswith', 'iendswith'],
            'description': ['exact', 'iexact', 'contains', 'icontains', 'startswith', 'istartswith', 'endswith', 'iendswith'],
            'address': ['exact', 'iexact', 'contains', 'icontains', 'startswith', 'istartswith', 'endswith', 'iendswith'],
            'city': ['exact', 'iexact', 'contains', 'icontains', 'startswith', 'istartswith', 'endswith', 'iendswith'],
            'state': ['exact', 'iexact', 'contains', 'icontains', 'startswith', 'istartswith', 'endswith', 'iendswith'],
            'country': ['exact', 'iexact', 'contains', 'icontains', 'startswith', 'istartswith', 'endswith', 'iendswith'],
            
            'status': ['exact', 'in'], 
            'type': ['exact', 'in'],
            
            'created_at': ['exact', 'gt', 'gte', 'lt', 'lte'],
            'updated_at': ['exact', 'gt', 'gte', 'lt', 'lte'],
        }