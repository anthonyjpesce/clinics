import json
from clinics.models import Clinic
from django.core import serializers
from django.shortcuts import render
from django.contrib.gis.geos import Point
from django.contrib.gis.geoip2 import GeoIP2
from django.views.generic import TemplateView
from django.contrib.gis.db.models.functions import Distance

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
