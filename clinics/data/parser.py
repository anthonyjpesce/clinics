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

# dump it into a dict which turns it into json
# print dumps(bf.data(fromstring(data)))


locations = bf.data(fromstring(data))['feed']['entry']


def parseTimes(day):
    daystartstr = day[day.index(':')+2:day.index(' - ')].replace('\r','').encode('utf-8')
    dayendstr = day[day.index(' - ')+3:].replace('\r','').encode('utf-8')

    try:
        daystart = datetime.strptime(daystartstr, '%I:%M%p').time()
        dayend = datetime.strptime(dayendstr, '%I:%M%p').time()

        # build small dict with the times
        times = {
            'daystart': daystart,
            'dayend': dayend
        }
        return times
    except:
        pass

# print len(locations)

# print locations[0]['link']['@href']

# locations[0]['test'] = 'HELLO'

# print dumps(locations[0])

# loop through clinic, scrape and augment
for clinic in locations[:2]:
    categories = clinic['summary']['div']['div']['div'][3]['span']['$']
    # print dumps()

    url = clinic['link']['@href']

    print url
    page = urllib2.urlopen(url)

    # check if detail page exists
    if page.geturl() != 'https://gettested.cdc.gov/':

        # soup it up
        soup = BeautifulSoup(page,"html.parser")

        # find the hours
        hoursParent = soup.find('span',{'class':'views-field-field-gsl-hours'})

        # check on formatting of list
        if len(hoursParent.find('div',{'class':'item-list'}).ul.findAll('li')) > 1:
            print 'hello'

            hours = {}

            for day in hoursParent.find('div',{'class':'item-list'}).ul.findAll('li'):
                # gimme the text
                day = day.text

                # find the semicolon
                dayname = day[:day.index(':')].encode('utf-8')

                # set to day key
                hours[dayname] = parseTimes(day)

            print hours

        else:
            days = hoursParent.find('div',{'class':'item-list'}).text.split('\n')

            hours = {}

            for day in days:
                # find the semicolon
                dayname = day[:day.index(':')].encode('utf-8')

                # set to day key
                hours[dayname] = parseTimes(day)

            print hours

        # get website
        websiteparent = soup.find('span',{'class':'views-field-gsl-props-web'})
        website = websiteparent.find('span',{'class':'field-content'}).a['href']

        # get eligibility reqs
        eligibilityparent = soup.find('span',{'class':'views-field-field-gsl-eligibility'})
        eligibility = eligibilityparent.find('span',{'class':'field-content'}).text

        print eligibility

        # get org type
        orgtypeparent = soup.find('span',{'class':'views-field-field-gsl-org-type'})
        orgtype = orgtypeparent.find('span',{'class':'field-content'}).text

        print orgtype

        # get email if available
        emailparent = soup.find('span',{'class':'views-field-field-gsl-email'})
        if emailparent.find('span',{'class':'field-content'}).a != None:
            email = emailparent.find('span',{'class':'field-content'}).a.text
            print email
        else:
            print 'no email'
        # loop through services to find anything else to add to categories
        servicesparent = soup.find('span',{'class':'views-field-field-gsl-services'})

        if len(servicesparent.find('div',{'class':'item-list'}).ul.findAll('li')) > 1:
            services = []
            for service in servicesparent.find('div',{'class':'item-list'}).ul.findAll('li'):
                services.append(service.text.strip().encode('utf-8'))
            print services

        else:
            serviceslist = servicesparent.find('div',{'class':'item-list'}).text.replace('\r','').encode('utf-8').split('\n')

            services = []
            for service in serviceslist:
                services.append(service.strip())

            print services
        # print dumps(clinic)

    time.sleep(1)


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





