from SimpleCV import *
from time import sleep
import time
import grequests
import io
from PIL import Image as Image2
from socket import error as SocketError
import random
from pymongo import MongoClient
#client = MongoClient()
#db = client.test_database
#scollection = db.street_collection
#ncollection = db.node_collection

## Unpickle needed data
## Image(Image2.open(io.BytesIO(images[0].content))).show()
## from PIL import Image as Image2
## import io

def f5(seq, idfun=None): 
	# order preserving
	if idfun is None:
		def idfun(x): return x
	seen = {}
	result = []
	for item in seq:
		marker = idfun(item)
		# in old Python versions:
		# if seen.has_key(marker)
		# but in new ones:
		if marker in seen: continue
		seen[marker] = 1
		result.append(item)
	return result

intersections = f5(pickle.load(open("intersections.p","rb")))
img_urls = f5(pickle.load(open("images.p","rb")))
intersections2 = []

for intersection in intersections:
	in1 = intersection[:intersection.find('@')-1]
	in2 = intersection[intersection.find('@')+2:]
	intersections2.append([in1, in2])

## "correct" pickles
lightList = intersections2
print lightList
def findNumb(str):
	m = [str.rfind('0'),str.rfind('1'),str.rfind('2'),str.rfind('3'),str.rfind('4'),str.rfind('5'),str.rfind('6'),str.rfind('7'),str.rfind('8'),str.rfind('9')]
	print m
	return m.index(max(m))
def findAll(str):
	return str.find("st") + str.find("th") + str.find("nd")
def clean(stra):
	lastNumb =findNumb(stra)
	print lastNumb
	lastIndex =stra.rfind(str(lastNumb))
	print lastIndex
	if lastIndex!=-1 and stra.find(" ")!=-1:
		ls = stra.split(" ")
		ret = ''
		ret =ls[0]
		if lastNumb==1:
			ret+="st"
		elif lastNumb==2:
			ret+="nd"
		elif lastNumb==3:
			ret+="rd"
		else:
			ret+="th"
		ret+=" " 
		ret +=ls[1]
	else:
		return stra
	return ret
    
for i in xrange(len(lightList)):
	for j in xrange(len(lightList[0])):
		lightList[i][j] = lightList[i][j].replace("Ave.", "Avenue")
		lightList[i][j] = lightList[i][j].replace("Ave", "Avenue")
		lightList[i][j] = lightList[i][j].replace("St.", "Street")
		lightList[i][j] = lightList[i][j].replace("ST.", "Street")
		lightList[i][j] = lightList[i][j].replace("St", "Street")
		lightList[i][j] = lightList[i][j].replace("ST", "Street")
		lightList[i][j] = lightList[i][j].replace("Pl.", "Place")
		lightList[i][j] = lightList[i][j].replace("Pl", "Place")
		lightList[i][j] = lightList[i][j].replace("N.", "North")
		lightList[i][j] = lightList[i][j].replace("S.", "South")
		lightList[i][j] = lightList[i][j].replace("E.", "East")
		lightList[i][j] = lightList[i][j].replace("W.", "West")
		lightList[i][j]=clean(lightList[i][j])

# for i in xrange(len(lightList)):
    # for j in xrange(len(lightList[0])):
        # lightList[i][j] = clean(lightList[i][j])
for i in xrange(len(lightList)):
	print lightList[i]

for url in range(len(img_urls)-1):
	if img_urls[url] == u'http://207.251.86.238/cctv258.jpg':
		del img_urls[url]

def genHeaders():
	ua = ""
	ua = ua + str(random.randint(1, 100))
	ua = ua + str(random.randint(1, 100))
	ua = ua + str(random.randint(1, 100))
	ua = ua + str(random.randint(1, 100))
	ua = ua + str(random.randint(1, 100))
	ua = ua + str(random.randint(1, 100))
	sleep(0.01)
	return {'User-Agent':ua}
def getImages():
	images = []
	unsent = (grequests.get(u, headers=genHeaders()) for u in img_urls)
	images = grequests.map(unsent)

	for image in range(len(images)):
		try:
			images[image] = Image(Image2.open(io.BytesIO(images[image].content)))
		except:
			images[image] = None
	return images

def testImages():
	results = []
	i1s = getImages()
	print "->"
	sleep(1)
	i2s = getImages()
	print "-->"
	sleep(1)
	i3s = getImages()
	print "--->"
	for img in range(len(i1s)):
		intersection_name = lightList[img]
		results.append([intersection_name[0], intersection_name[1],testLines(i1s[img], i2s[img], i3s[img])])
	return results
		
def testLines(i1, i2, i3):
	if i1 is None or i2 is None or i3 is None:
		return "Insufficient Data"
	if np.matrix(i1).shape != np.matrix(i2).shape or np.matrix(i1).strides != np.matrix(i2).strides:
		return "Insufficient Data"
	try:
		i1c = i2-i1
	except:
		return "Insufficient Data"
	if np.matrix(i2).shape != np.matrix(i3).shape or np.matrix(i2).strides!= np.matrix(i3).strides:
		return "Insufficient Data"
	try:
		i2c = i3-i2
		i3 = i1c+i2c
	except:
		return "Insufficient Data"
	lines = i3.findLines(threshold=88, minlinelength=13)
	if lines == []:
		return "Insufficient Data"
	lines.draw()
	angles = [abs(l.angle()) for l in lines]
	lengths = [int(l.length()) for l in lines]
	# Filter out smallest lines
	average_length = np.mean(lengths)
	new_lengths = []
	new_angles = []
	# Give me only the top 70% of lines
	# 50 * 1.4 = 70
	for item in range(len(lengths)):
		if lengths[item] < average_length*1.4:
			continue
		else:
			new_lengths.append(lengths[item])
			new_angles.append(angles[item])
	if sum(new_lengths) == 0:
		return "Insufficient Data"
	if sum(lengths) == 0:
		return "Insufficient Data"
	anomalies = [(n/np.mean(new_angles))*100 for n in np.ma.array(new_angles).anom()]
	offset = 0
	for item in range(len(anomalies)):
		if abs(anomalies[item-offset]) > 50:
			if item-offset in anomalies:
				offset = offset+1
				del new_angles[item-offset]
				del new_anlengths[item-offset]
				print "Filtered Anomaly"
	average = np.average(new_angles, weights=new_lengths)
	if abs(average) > 20:
		return "Green"
	else:
		return "Red"

def calculateTimeGap(t, t2):
	s1 = t-t2
	s2 = (s1[0]*60) + s1[1]
	return s2

def startRealTime():
	on = 1
	timesR = [0 for n in range(164)]
	timesG = [0 for n in range(164)]
	gapsRg = [0 for n in range(164)]
	gapsGr = [0 for n in range(164)]
	r1 = None
	r2 = None
	curTime = 0
	while on==1:
		sleep(5)
		if r1 == None:
			r1 = testImages()
		else:
			r2 = testImages()
			for item in range(len(r1)):
				#a = ncollection.find_one({'on':[r1[0],r1[1]]})
				#if a is None:
				#	a= ncollection.find_one({'on':[r1[1],r1[0]]})
				#if a is None:
				#	continue
				if r1[item] != r2[item] and r1[item] != "Insufficient Data" and r2[item] != "Insufficient Data":
					if r1[item] == "Red":
						#ncollection.update({'name':a['name']},{'$set':{'light':'green'}})
						timesG[item] = np.ma.array([int(time.asctime().split(" ")[3].split(":")[1]), int(time.asctime().split(" ")[3].split(":")[2])])
						#ncollection.update({'name':a['name']},{'$set':{'dr':calculateTimeGap(timesG[item], timesR[item])}})
					else:
						#ncollection.update({'name':a['name']},{'$set':{'light':'red'}})
						timesR[item] = np.ma.array([int(time.asctime().split(" ")[3].split(":")[1]), int(time.asctime().split(" ")[3].split(":")[2])])
						#ncollection.update({'name':a['name']},{'$set':{'dr':calculateTimeGap(timesG[item], timesR[item])}})
					counts[item] = 0
			r1 = r2
			r2 = None
		print timesR
		print timesG
	if on == 1:
		startRealTime()
