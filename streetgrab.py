import matplotlib.pyplot as plt
from pymongo import MongoClient
def getStreetCoords(db, street):
    scollection = db.street_collection
    ncollection = db.node_collection
    s = scollection.find_one({'name':street})
    coordlist1 = []
    coordlist2 = []
    for i in s['refs']:
        node = ncollection.find_one({'name':i})
        if node is not None:
            print node
            r = node['coor']
            coordlist1.append(r[0])
            coordlist2.append(r[1])
    return [coordlist1,coordlist2]
client = MongoClient()
db = client.test_database
streetpar = raw_input("So, what street do you want? ")
coor = getStreetCoords(db, streetpar)
intersectionsx = coor[0]
intersectionsy=coor[1]
for i in xrange(0,len(coor[0])):
    print str(coor[1][i]) + "," + str(coor[0][i])
plt.plot(intersectionsx,intersectionsy, 'ro')
diffy = max(intersectionsx)-min(intersectionsx)
plt.axis([min(intersectionsx), max(intersectionsx), min(intersectionsy), max(intersectionsy)])

# done
plt.show()