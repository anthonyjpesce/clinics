from clinics import views
from django.conf import settings
from django.conf.urls import include, url


urlpatterns = [
    url(r'^$', views.IndexView.as_view()),
]
