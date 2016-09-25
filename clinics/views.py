import json
from clinics.models import Clinic
from django.core import serializers
from django.shortcuts import render
from django.contrib.gis.geos import Point
from django.contrib.gis.geoip2 import GeoIP2
from rest_framework.response import Response
from clinics.serializers import ClinicSerializer
from django.views.generic import TemplateView, DetailView
from django.contrib.gis.db.models.functions import Distance
from rest_framework import status, filters, viewsets, generics

# init geoip
G = GeoIP2()
JSONSerializer = serializers.get_serializer("json")

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


class IndexView(TemplateView):
    template_name = "index.html"
    
    def get_context_data(self, **kwargs):
        try:
            ip = get_client_ip(self.request)
            lon, lat = G.lon_lat(ip)
        except:
            ip = None
            lon, lat = (-118.2437, 34.0522)
        
        pt = Point(lon, lat)
        distance_ordered = Clinic.objects.distance(pt).order_by('distance')[:10]
        distance_ordered.annotate(distance=Distance('location', pt))
        
        data = []
        for i in distance_ordered:
            tmp = i.as_dict()
            tmp['distance'] = i.distance.mi
            data.append(tmp)
        
        return {
            'clinics': json.dumps(data),
            'coords': [lon, lat]
        }


class ClinicDetailView(DetailView):
    model = Clinic
    template_name = "detail.html"


# API Views
class ClinicViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Clinic.objects.all().order_by('name')
    serializer_class = ClinicSerializer

    def get_queryset(self):
        queryset = Clinic.objects.all()
        
        # basic filter options
        lat = self.request.query_params.get('lat', None)
        lon = self.request.query_params.get('lon', None)
        categories = self.request.query_params.getlist('categories', None)
        
        if lat and lon:
            try:
                pt = Point(float(lon), float(lat))
            except:
                return Response("Bad point data", status.HTTP_400_BAD_REQUEST)
            
            queryset = Clinic.objects.distance(pt).order_by('distance')
            queryset.annotate(distance=Distance('location', pt))
        
        if categories:
            queryset = queryset.filter(clean_categories__contains=categories)
            
        return queryset