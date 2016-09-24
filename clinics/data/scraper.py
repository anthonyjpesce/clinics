import urllib2, socket, time
from bs4 import BeautifulSoup

url = 'https://gettested.cdc.gov/gettested_redirect/111227'

page = urllib2.urlopen(url)
soup = BeautifulSoup(page,"html.parser")

# find the hours
hoursParent = soup.find('span',{'class':'views-field-field-gsl-hours'})
days = hoursParent.find('div',{'class':'item-list'}).text.split('\n')

# print hours

hours = {}

for day in days:
	# find the semicolon
	dayname = day[:day.index(':')].encode('utf-8')
	daystart = day[day.index(':')+2:day.index(' - ')].replace('\r','').encode('utf-8')
	dayend = day[day.index(' - ')+3:].replace('\r','').encode('utf-8')

	times = {
		'daystart': daystart,
		'dayend': dayend
	}


	hours[dayname] = times

print hours