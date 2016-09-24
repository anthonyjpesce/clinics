from __future__ import unicode_literals
from django.contrib.gis.db import models
from django.contrib.postgres.fields import ArrayField


class Clinic(models.Model):
    name = models.CharField(max_length=500)
    street = models.CharField(max_length=500)
    city = models.CharField(max_length=500)
    state = models.CharField(max_length=500)
    zipcode = models.CharField(max_length=500)
    telephone = models.CharField(max_length=500)
    categories = ArrayField(models.CharField(max_length=500), blank=True)
    languages = ArrayField(models.CharField(max_length=500), blank=True)
    website = models.CharField(max_length=500)
    email = models.CharField(max_length=500)
    hours
    org_type = models.CharField(max_length=500)
    eligibility = models.CharField(max_length=500)
    location = models.PointField()
    objects = models.GeoManager()