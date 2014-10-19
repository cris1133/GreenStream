from SimpleCV import *
from time import sleep
import grequests
import io
from PIL import Image as Image2
from socket import error as SocketError
import errno
import random
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
	sleep(0.001)
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
	sleep(5)
	i2s = getImages()
	print "-->"
	sleep(5)
	i3s = getImages()
	print "--->"
	for img in range(len(i1s)):
		intersection_name = intersections[img]
		in1 = intersection_name[:intersection_name.find('@')-1]
		in2 = intersection_name[intersection_name.find('@')+2:]
		results.append([in1, in2,testLines(i1s[img], i2s[img], i3s[img])])
	return results
		
def testLines(i1, i2, i3):
	if i1 is None or i2 is None or i3 is None:
		return "Insufficient Data"
	if np.matrix(i1).shape != np.matrix(i2).shape or np.matrix(i1).strides != np.matrix(i2).strides:
		return "Insufficient Data"
	i1c = i2-i1
	if np.matrix(i2).shape != np.matrix(i3).shape or np.matrix(i2).strides!= np.matrix(i3).strides:
		return "Insufficient Data"
	i2c = i3-i2
	i3 = i1c+i2c
	lines = i3.findLines(threshold=88, minlinelength=13)
	if lines == []:
		return "Insufficient Data"
	lines.draw()
	i3.show()
	angles = [l.angle() for l in lines]
	lengths = [int(l.length()) for l in lines]
	if sum(lengths) == 0:
		return "Insufficient Data"
	anomalies = np.ma.array(angles).anom()
	offset = 0
	for item in range(len(anomalies)):
		if abs(anomalies[item-offset]) > 34:
			if item-offset in anomalies:
				offset = offset+1
				del angles[item-offset]
				del lengths[item-offset]
	average = np.average(angles, weights=lengths)
	average2 = np.mean([average, max([abs(n) for n in angles]) * cmp(max(angles), 0) ])
	if abs(average2) > 20:
		return "Green"
	else:
		return "Red"
