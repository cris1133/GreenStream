import requests
from bs4 import BeautifulSoup
import hashlib
## Scrape CIDS
## Scrape Intersection Names
## Scrape Image Locations
cids = []
intersections = []
image_urls = []
url_head = "http://"

cid_url = "http://nyctmc.org/multiview2.php"
data = requests.get(cid_url)
data = data.text
data = BeautifulSoup(data)

def f5(seq, idfun=None): 
	# order preserving
	if idfun is None:
		def idfun(x): return hash(x)
	seen = {}
	result = []
	removed = []
	for item in seq:
		marker = idfun(item)
		# in old Python versions:
		# if seen.has_key(marker)
		# but in new ones:
		if marker in seen: 
			removed.append(item)
			continue
		seen[marker] = 1
		result.append(item)
	return result, removed
	
def getInitialData(data):
	for table in data.find_all('table'):
		if table.get('id') == "tableCam":
			return table.descendants

def getImageUrl(cid):
	url = "http://nyctmc.org/google_popup.php?cid="+cid
	data = requests.get(url)
	data = data.text
	data = BeautifulSoup(data)
	data = data.find_all('script')[0].contents
	data = data[0][data[0].find('h'):data[0].find('+')]
	data = data[:data.find("'")]
	return data

# Scrape CIDS
d1 = getInitialData(data)
prohibited = []
for item in d1:
	if hasattr(item, "find_all"):
		stop = 0
		for item in item.find_all('td'):
			if "Inactive" in str(item.contents):
				stop=1
		if stop==0:
			for item in item.find_all('input'):
				value = item.get('value')
				if not value in prohibited:
					cids.append(item.get('value'))
		else:
			for item in item.find_all('input'):
				prohibited.append(item.get('value'))

## Get Intersection Names
d1 = getInitialData(data)
prohibited = []
for item in d1:
	if hasattr(item, "find_all"):
		stop = 0
		for item in item.find_all('td'):
			if "Inactive" in str(item.contents):
				stop=1
		if stop==0:
			for item in item.find_all('span'):
				if item.get('class') == ['OTopTitle']:
					name = item.contents[0]
					if not name in prohibited:
						intersections.append(item.contents[0])
		else:
			for item in item.find_all('span'):
				if item.get('class') == ['OTopTitle']:
					prohibited.append(item.contents[0])

## Get Image URLs
##for cid in cids:
##	image_urls.append(getImageUrl(cid))


