import urllib2, socket, time, json
from bs4 import BeautifulSoup
from datetime import datetime
from json import dumps

def parseTimes(day):
    daystartstr = day[day.index(':')+2:day.index(' - ')].replace('\r','').encode('utf-8')
    dayendstr = day[day.index(' - ')+3:].replace('\r','').encode('utf-8')

    try:
        daystart = datetime.strptime(daystartstr, '%I:%M%p').strftime("%H:%M")
        dayend = datetime.strptime(dayendstr, '%I:%M%p').strftime("%H:%M")

        # build small dict with the times
        times = {
            'daystart': daystart,
            'dayend': dayend
        }
        return times
    except:
        pass

# file to read from
clinics = json.load(open('90029-50.json','r'))

f = open('90029-50-more-data.json','w')

for clinic in clinics:
    url = clinic['cdclink']
    print url

    # which clinic?
    cindex = clinics.index(clinic)

    page = urllib2.urlopen(url)

    # check if detail page exists
    if page.geturl() != 'https://gettested.cdc.gov/':

        soup = BeautifulSoup(page,"html.parser")

        # find the hours
        hoursParent = soup.find('span',{'class':'views-field-field-gsl-hours'})

        # check on formatting of list
        if len(hoursParent.find('div',{'class':'item-list'}).ul.findAll('li')) > 1:

            hours = {}

            for day in hoursParent.find('div',{'class':'item-list'}).ul.findAll('li'):
                # gimme the text
                day = day.text

                # find the semicolon
                dayname = day[:day.index(':')].encode('utf-8')

                # set to day key
                hours[dayname] = parseTimes(day)

        else:
            days = hoursParent.find('div',{'class':'item-list'}).text.split('\n')

            hours = {}

            if len(days) > 1:
                for day in days:
                    # find the semicolon
                    dayname = day[:day.index(':')].encode('utf-8')

                    # set to day key
                    hours[dayname] = parseTimes(day)

            clinics[cindex]['hours'] = hours

        # get website
        websiteparent = soup.find('span',{'class':'views-field-gsl-props-web'})
        website = websiteparent.find('span',{'class':'field-content'}).a['href']

        clinics[cindex]['website'] = website

        # get eligibility reqs
        eligibilityparent = soup.find('span',{'class':'views-field-field-gsl-eligibility'})
        eligibility = eligibilityparent.find('span',{'class':'field-content'}).text

        clinics[cindex]['eligibility'] = eligibility

        # get org type
        orgtypeparent = soup.find('span',{'class':'views-field-field-gsl-org-type'})
        orgtype = orgtypeparent.find('span',{'class':'field-content'}).text

        clinics[cindex]['orgtype'] = orgtype

        # get email if available
        emailparent = soup.find('span',{'class':'views-field-field-gsl-email'})
        if emailparent.find('span',{'class':'field-content'}).a != None:
            email = emailparent.find('span',{'class':'field-content'}).a.text

            clinics[cindex]['email'] = email

        # loop through services to find anything else to add to categories
        servicesparent = soup.find('span',{'class':'views-field-field-gsl-services'})

        categories = clinics[cindex]['categories']

        if len(servicesparent.find('div',{'class':'item-list'}).ul.findAll('li')) > 1:
            # services = []
            for service in servicesparent.find('div',{'class':'item-list'}).ul.findAll('li'):
                service = service.text.strip().encode('utf-8')
                if service not in categories:
                    categories.append(service)

        else:
            serviceslist = servicesparent.find('div',{'class':'item-list'}).text.replace('\r','').encode('utf-8').split('\n')

            # services = []
            for service in serviceslist:
                service = service.strip()

                if service not in categories:
                    categories.append(service)

    time.sleep(1)

# write this to the file
f.write(dumps(clinics))
f.close()