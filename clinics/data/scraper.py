import urllib2, socket, time
from bs4 import BeautifulSoup
from datetime import datetime

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


url = 'https://gettested.cdc.gov/gettested_redirect/114434'
url = 'https://gettested.cdc.gov/gettested_redirect/113767'

page = urllib2.urlopen(url)

# check if detail page exists
if page.geturl() != 'https://gettested.cdc.gov/':

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
    


    # loop through services to find anything else to add to categories



