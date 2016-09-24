from __future__ import unicode_literals
from django.contrib.gis.db import models
from django.contrib.postgres.fields import ArrayField, DateTimeRangeField


class Clinic(models.Model):
    # Clinic name
    name = models.CharField(max_length=500, blank=True, db_index=True)
    slug = models.SlugField(max_length=500, blank=True, db_index=True)
    # Address/contact fields
    street = models.CharField(max_length=500, blank=True)
    city = models.CharField(max_length=500, blank=True)
    state = models.CharField(max_length=500, blank=True)
    zipcode = models.CharField(max_length=500, blank=True)
    telephone = models.CharField(max_length=500, blank=True)
    email = models.CharField(max_length=500, blank=True)
    website = models.CharField(max_length=500, blank=True)
    # Misc
    categories = ArrayField(
        models.CharField(max_length=500),
        blank=True,
        db_index=True
    )
    languages = ArrayField(
        models.CharField(max_length=500),
        blank=True,
        db_index=True
    )
    org_type = models.CharField(max_length=500, blank=True)
    eligibility = models.CharField(max_length=500, blank=True)
    # Hours for each day
    monday_hours = DateTimeRangeField(blank=True, null=True, db_index=True)
    tuesday_hours = DateTimeRangeField(blank=True, null=True, db_index=True)
    wednesday_hours = DateTimeRangeField(blank=True, null=True, db_index=True)
    thursday_hours = DateTimeRangeField(blank=True, null=True, db_index=True)
    friday_hours = DateTimeRangeField(blank=True, null=True, db_index=True)
    saturday_hours = DateTimeRangeField(blank=True, null=True, db_index=True)
    sunday_hours = DateTimeRangeField(blank=True, null=True, db_index=True)
    # Point field
    location = models.PointField(blank=True, null=True, db_index=True)
    objects = models.GeoManager()
    
    class Meta:
        verbose_name = 'Clinic'
        verbose_name_plural = 'Clinics'
        ordering = ("name",)

    def __unicode__(self):
        return self.name

