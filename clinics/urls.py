from clinics import views
from django.conf import settings
from django.conf.urls import include, url
from rest_framework import routers, serializers, viewsets
from clinics.views import ClinicViewSet

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'clinics', ClinicViewSet)

urlpatterns = [
    url(r'^$', views.IndexView.as_view()),
    url(r'^api/', include(router.urls)),
    url(r'^(?P<slug>[\w-]+)/$', views.ClinicDetailView.as_view()),
    # url(r'^api-auth/',
    #     include('rest_framework.urls', namespace='rest_framework')),
]
