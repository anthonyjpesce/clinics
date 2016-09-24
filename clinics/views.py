import json
from clinics.models import Clinic
from django.shortcuts import render
# from django.contrib.gis.geoip2 import GeoIP2
from django.views.generic import TemplateView

# init geoip
# G = GeoIP2()

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


class IndexView(TemplateView):
    template_name = "index.html"
    
    # def get_context_data(self, **kwargs):
    #     ip = get_client_ip(self.request)
    #     lon, lat = G.lon_lat(ip)
    #     return {
    #         'ip': ip,
    #         'lon': lon,
    #         'lat': lat,
    #     }
