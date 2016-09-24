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

# print len(locations)

# print locations[0]['link']['@href']

# locations[0]['test'] = 'HELLO'

# print dumps(locations[0])

# loop through clinic, scrape and augment
# for clinic in locations[:2]:
#     categories = clinic['summary']['div']['div']['div'][3]['span']['$']
#     # print dumps()

#     url = clinic['link']['@href']

    # print url
    # page = urllib2.urlopen(url)

    # # check if detail page exists
    # if page.geturl() != 'https://gettested.cdc.gov/':

    #     # soup it up
    #     soup = BeautifulSoup(page,"html.parser")

    #     # find the hours
    #     hoursParent = soup.find('span',{'class':'views-field-field-gsl-hours'})

    #     # check on formatting of list
    #     if len(hoursParent.find('div',{'class':'item-list'}).ul.findAll('li')) > 1:
    #         print 'hello'

    #         hours = {}

    #         for day in hoursParent.find('div',{'class':'item-list'}).ul.findAll('li'):
    #             # gimme the text
    #             day = day.text

    #             # find the semicolon
    #             dayname = day[:day.index(':')].encode('utf-8')

    #             # set to day key
    #             hours[dayname] = parseTimes(day)

    #         print hours

    #     else:
    #         days = hoursParent.find('div',{'class':'item-list'}).text.split('\n')

    #         hours = {}

    #         for day in days:
    #             # find the semicolon
    #             dayname = day[:day.index(':')].encode('utf-8')

    #             # set to day key
    #             hours[dayname] = parseTimes(day)

    #         print hours

    #     # get website
    #     websiteparent = soup.find('span',{'class':'views-field-gsl-props-web'})
    #     website = websiteparent.find('span',{'class':'field-content'}).a['href']

    #     # get eligibility reqs
    #     eligibilityparent = soup.find('span',{'class':'views-field-field-gsl-eligibility'})
    #     eligibility = eligibilityparent.find('span',{'class':'field-content'}).text

    #     print eligibility

    #     # get org type
    #     orgtypeparent = soup.find('span',{'class':'views-field-field-gsl-org-type'})
    #     orgtype = orgtypeparent.find('span',{'class':'field-content'}).text

    #     print orgtype

    #     # get email if available
    #     emailparent = soup.find('span',{'class':'views-field-field-gsl-email'})
    #     if emailparent.find('span',{'class':'field-content'}).a != None:
    #         email = emailparent.find('span',{'class':'field-content'}).a.text
    #         print email
    #     else:
    #         print 'no email'
    #     # loop through services to find anything else to add to categories
    #     servicesparent = soup.find('span',{'class':'views-field-field-gsl-services'})

    #     if len(servicesparent.find('div',{'class':'item-list'}).ul.findAll('li')) > 1:
    #         services = []
    #         for service in servicesparent.find('div',{'class':'item-list'}).ul.findAll('li'):
    #             services.append(service.text.strip().encode('utf-8'))
    #         print services

    #     else:
    #         serviceslist = servicesparent.find('div',{'class':'item-list'}).text.replace('\r','').encode('utf-8').split('\n')

    #         services = []
    #         for service in serviceslist:
    #             services.append(service.strip())

    #         print services
    #     # print dumps(clinic)

    # time.sleep(1)


    # page = urllib2.urlopen(url)
    # soup = BeautifulSoup(page,"html.parser")

    # check that URL is not cdc homepage

# # find the hours
# hoursParent = soup.find('span',{'class':'views-field-field-gsl-hours'})
# days = hoursParent.find('div',{'class':'item-list'}).text.split('\n')

# hours = {}

# for day in days:
#     # find the semicolon
#     dayname = day[:day.index(':')].encode('utf-8')
#     daystartstr = day[day.index(':')+2:day.index(' - ')].replace('\r','').encode('utf-8')
#     dayendstr = day[day.index(' - ')+3:].replace('\r','').encode('utf-8')

#     daystart = datetime.strptime(daystartstr, '%I:%M%p').time()
#     dayend = datetime.strptime(dayendstr, '%I:%M%p').time()

#     # build small dict with the times
#     times = {
#         'daystart': daystart,
#         'dayend': dayend
#     }

#     # set to day key
#     hours[dayname] = times

# # get website
# websiteparent = soup.find('span',{'class':'views-field-gsl-props-web'})
# website = websiteparent.find('span',{'class':'field-content'}).a['href']

# # get eligibility reqs
# eligibilityparent = soup.find('span',{'class':'views-field-field-gsl-eligibility'})
# eligibility = eligibilityparent.find('span',{'class':'field-content'}).text

# print eligibility





