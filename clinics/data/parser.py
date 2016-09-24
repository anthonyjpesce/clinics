from xmljson import badgerfish as bf
from xml.etree.ElementTree import fromstring, tostring
import xml.etree.ElementTree as ET
from json import dumps

# open xml file
tree = ET.parse('90029-50.xml')

# get root and convert it to a string
root = tree.getroot()
data = tostring(root)

# dump it into a dict which turns it into json
# print dumps(bf.data(fromstring(data)))


locations = bf.data(fromstring(data))['feed']['entry']

print len(locations)

print locations[0]['link']['@href']

locations[0]['test'] = 'HELLO'

print dumps(locations[0])

for clinic in locations:
	if clinic['link']['@href'] =='https://gettested.cdc.gov/gettested_redirect/111227':
		print dumps(clinic)
	# print clinic['link']['@href']

# print locations['feed']
# for key in locations:
    # print key, 'corresponds to', locations[key]