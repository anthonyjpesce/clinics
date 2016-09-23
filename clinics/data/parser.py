# import xml.etree.ElementTree
# e = xml.etree.ElementTree.parse('90029-50.xml').getroot()


# print e
# print e.findall('feed')

# for atype in e.findall('type'):
#     print(atype.get('foobar'))

import xml.etree.ElementTree as ET
tree = ET.parse('90029-50.xml')
root = tree.getroot()

# root = ET.fromstring(country_data_as_string)

# print root
# print root.tag

print root[6][0].tag
print root[6][0].attrib
print root[6][0].text

# for child in root:
# 	for item in child:
# 		print item.tag, item.attrib
	# print child.tag, child.attrib


