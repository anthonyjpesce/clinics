import os
import json
import logging
from datetime import datetime
from django.conf import settings
from clinics.models import Clinic
from django.utils.text import slugify
from django.contrib.gis.geos import Point
from psycopg2.extras import DateTimeTZRange
from django.core.management.base import BaseCommand

logger = logging.getLogger('clinics')
PATH_TO_DATA = os.path.join(
    settings.BASE_DIR,
    'clinics',
    'data',
    '90029-50-all-data.json'
)
with open(PATH_TO_DATA) as data:
    data = json.load(data)


class Command(BaseCommand):
    help = "Load candidates and associate with committees"

    def clean_time(self, timestring):
        toks = timestring.split(':')
        return [int(i) for i in toks]

    def clean_categories(self, categories):
        if not categories:
            return None
        
        pretty = {
            'chlamydia': 'Chlamydia',
            'hiv': 'HIV',
            'gonorrhea': 'Gonorrhea',
            'herpes': 'Herpes',
            'syphilis': 'Syphilis',
            'hepatitis a': 'Hepatitis A',
            'hepatitis b': 'Hepatitis B',
            'hepatitis c': 'Hepatitis C',
        }
        out = []
        tests = pretty.keys()
        
        for i in categories:
            toks = i.lower().split(' ')
            for t in tests:
                if t in toks and ('test' in toks or 'testing' in toks):
                    out.append(pretty[t])
        
        return list(set(out))

    def handle(self, *args, **options):
        """
        Loop through our clinics JSON and load them into the database.
        """
        # delete the old ones first
        logger.debug('Deleting %s old records' % Clinic.objects.count())
        Clinic.objects.all().delete()
        # Loop through the json and load each
        logger.debug('Loading %s new records' % len(data))
        for index, i in enumerate(data):
            c = Clinic(
                name=i.get('name', ''),
                street=i.get('street', ''),
                city=i.get('city', ''),
                state=i.get('state', ''),
                zipcode=i.get('zipcode', ''),
                telephone=i.get('telephone', ''),
                email=i.get('email', ''),
                website=i.get('website', ''),
                categories=i.get('categories', None),
                clean_categories=self.clean_categories(i.get('categories', None)),
                languages=i.get('languages', None),
                org_type=i.get('orgtype', ''),
                eligibility=i.get('eligibility', ''),
            )
            c.slug = slugify("%s %s" % (c.name, index))
            if i.get('location'):
                c.location = Point(
                    y=float(i['location'][0]),
                    x=float(i['location'][1]),
                )
                
            if i.get('hours'):
                if i['hours'].get('Monday'):
                    op = self.clean_time(i['hours']['Monday']['daystart'])
                    cl = self.clean_time(i['hours']['Monday']['dayend'])
                    c.monday_hours = DateTimeTZRange(
                        datetime(2015, 1, 1, op[0], op[1], 0, 0),
                        datetime(2015, 1, 1, cl[0], cl[1], 0, 0),
                    )
                                
                if i['hours'].get('Tuesday'):
                    op = self.clean_time(i['hours']['Tuesday']['daystart'])
                    cl = self.clean_time(i['hours']['Tuesday']['dayend'])
                    c.tuesday_hours = DateTimeTZRange(
                        datetime(2015, 1, 1, op[0], op[1], 0),
                        datetime(2015, 1, 1, cl[0], cl[1], 0),
                    )
                
                if i['hours'].get('Wednesday'):
                    op = self.clean_time(i['hours']['Wednesday']['daystart'])
                    cl = self.clean_time(i['hours']['Wednesday']['dayend'])
                    c.wednesday_hours = DateTimeTZRange(
                        datetime(2015, 1, 1, op[0], op[1], 0),
                        datetime(2015, 1, 1, cl[0], cl[1], 0),
                    )
    
                if i['hours'].get('Thursday'):
                    op = self.clean_time(i['hours']['Thursday']['daystart'])
                    cl = self.clean_time(i['hours']['Thursday']['dayend'])
                    c.thursday_hours = DateTimeTZRange(
                        datetime(2015, 1, 1, op[0], op[1], 0),
                        datetime(2015, 1, 1, cl[0], cl[1], 0),
                    )
    
                if i['hours'].get('Friday'):
                    op = self.clean_time(i['hours']['Friday']['daystart'])
                    cl = self.clean_time(i['hours']['Friday']['dayend'])
                    c.friday_hours = DateTimeTZRange(
                        datetime(2015, 1, 1, op[0], op[1], 0),
                        datetime(2015, 1, 1, cl[0], cl[1], 0),
                    )
    
                if i['hours'].get('Saturday'):
                    op = self.clean_time(i['hours']['Saturday']['daystart'])
                    cl = self.clean_time(i['hours']['Saturday']['dayend'])
                    c.saturday_hours = DateTimeTZRange(
                        datetime(2015, 1, 1, op[0], op[1], 0),
                        datetime(2015, 1, 1, cl[0], cl[1], 0),
                    )
    
                if i['hours'].get('Sunday'):
                    op = self.clean_time(i['hours']['Sunday']['daystart'])
                    cl = self.clean_time(i['hours']['Sunday']['dayend'])
                    c.sunday_hours = DateTimeTZRange(
                        datetime(2015, 1, 1, op[0], op[1], 0),
                        datetime(2015, 1, 1, cl[0], cl[1], 0),
                    )
            c.save()
            logger.debug('    Loaded %s' % c)
        logger.debug('Done')