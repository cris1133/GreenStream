from pymongo import MongoClient
import pickle
client = MongoClient()
db = client.test_database
ncollection = db.node_collection
scollection = db.street_collection
lightList = pickle.load(open("fakeit1.p", "rb"))
def listOverlap(list1, list2):
    for i in list1:
        for j in list2:
            if j==i:
                return i
for i in xrange(len(lightList)):
    s1 =lightList[i][0]
    s2 =lightList[i][1]
    state = lightList[i][2]
    scol1=scollection.find_one({'name':s1})
    scol2=scollection.find_one({'name':s2})
    if scol1 is not None and scol2 is not None:
        s1Nodes = scol1['refs']
        s2Nodes = scol2['refs']
        overlap = listOverlap(s1Nodes, s2Nodes)
        ncollection.update({'name':overlap}, {'$set':{'light':state.lower()}})
        
    