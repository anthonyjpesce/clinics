from xmljson import badgerfish as bf
from xml.etree.ElementTree import fromstring, tostring
import xml.etree.ElementTree as ET
from json import dumps
import urllib2, socket, time
from bs4 import BeautifulSoup
from datetime import datetime
import time

# open xml file
tree = ET.parse('90029-50.xml')

# get root and convert it to a string
root = tree.getroot()
data = tostring(root)

# start a file to write to
f = open('90029-50.json','w')

# this is where all the beautiful data will go
clinics = []

locations = bf.data(fromstring(data))['feed']['entry']

# start your parsing
for clinic in locations:
    # name
    name = clinic['title']['$']

    # street
    street = clinic['summary']['div']['div']['div'][1]['div']['$']

    # city
    city = clinic['summary']['div']['div']['div'][1]['span'][0]['$']

    # state
    state = clinic['summary']['div']['div']['div'][1]['span'][1]['$']

    # zipcode
    zipcode = clinic['summary']['div']['div']['div'][1]['span'][2]['$']

    # telephone
    telephone = clinic['summary']['div']['div']['div'][2]['$']

    # categories
    categories = clinic['summary']['div']['div']['div'][3]['span']['$'].split(', ')

    # languages
    languages = clinic['summary']['div']['div']['div'][4]['span']['$'].split(',')

    # website = models.CharField(max_length=500)
    # email = models.CharField(max_length=500)
    # hours
    # org_type = models.CharField(max_length=500)
    # eligibility = models.CharField(max_length=500)

    # location
    location = clinic['{http://www.georss.org/georss}point']['$'].split(' ')

    # cdc link for more details in scraper.py
    cdclink = clinic['link']['@href']

    clinicinfo = {
        'name': name,
        'street': street,
        'city': city,
        'state': state,
        'zipcode': zipcode,
        'telephone': telephone,
        'categories': categories,
        'languages': languages,
        'location': location,
        'cdclink': cdclink
    }

    clinics.append(clinicinfo)

print dumps(clinics)

# write this to the file
f.write(dumps(clinics))
f.close()
