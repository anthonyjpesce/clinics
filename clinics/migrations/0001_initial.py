# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-24 20:00
from __future__ import unicode_literals

import django.contrib.gis.db.models.fields
import django.contrib.postgres.fields
import django.contrib.postgres.fields.ranges
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Clinic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, db_index=True, max_length=500)),
                ('slug', models.SlugField(blank=True, max_length=500)),
                ('street', models.CharField(blank=True, max_length=500)),
                ('city', models.CharField(blank=True, max_length=500)),
                ('state', models.CharField(blank=True, max_length=500)),
                ('zipcode', models.CharField(blank=True, max_length=500)),
                ('telephone', models.CharField(blank=True, max_length=500)),
                ('email', models.CharField(blank=True, max_length=500)),
                ('website', models.CharField(blank=True, max_length=500)),
                ('categories', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=500), blank=True, db_index=True, size=None)),
                ('languages', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=500), blank=True, db_index=True, size=None)),
                ('org_type', models.CharField(blank=True, max_length=500)),
                ('eligibility', models.CharField(blank=True, max_length=500)),
                ('monday_hours', django.contrib.postgres.fields.ranges.DateTimeRangeField(blank=True, db_index=True, null=True)),
                ('tuesday_hours', django.contrib.postgres.fields.ranges.DateTimeRangeField(blank=True, db_index=True, null=True)),
                ('wednesday_hours', django.contrib.postgres.fields.ranges.DateTimeRangeField(blank=True, db_index=True, null=True)),
                ('thursday_hours', django.contrib.postgres.fields.ranges.DateTimeRangeField(blank=True, db_index=True, null=True)),
                ('friday_hours', django.contrib.postgres.fields.ranges.DateTimeRangeField(blank=True, db_index=True, null=True)),
                ('saturday_hours', django.contrib.postgres.fields.ranges.DateTimeRangeField(blank=True, db_index=True, null=True)),
                ('sunday_hours', django.contrib.postgres.fields.ranges.DateTimeRangeField(blank=True, db_index=True, null=True)),
                ('location', django.contrib.gis.db.models.fields.PointField(blank=True, db_index=True, null=True, srid=4326)),
            ],
            options={
                'ordering': ('name',),
                'verbose_name': 'Clinic',
                'verbose_name_plural': 'Clinics',
            },
        ),
    ]
