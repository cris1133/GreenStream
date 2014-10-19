from pymongo import MongoClient
import time
def closestRed(nodes, index):
    closestless = 0
    closestgreat = len(nodes)-1
    for i in xrange(len(nodes)):
        f = nodes[i]
        if f is not None and f['light']=='red':
            if i<index:
                closestless = i
            elif i>index:
                closestgreat = i
                break
    return [closestless,closestgreat]
def closestGreen(nodes, index):
    closestless = 0
    closestgreat = len(nodes)-1
    for i in xrange(len(nodes)):
        f = nodes[i]
        if f is not None and f['light']=='green':
            if i<index:
                closestless = i
            else:
                closestgreat = i
                break
    return [closestless,closestgreat]
client = MongoClient()
db = client.test_database
scollection = db.street_collection
ncollection = db.node_collection
counter = 0
while ncollection.find_one({"light":"none"}) is not None and counter<2:
    print 'start of of round ' + str(counter)
    knownRed = ncollection.find({"light":"red"})
    knownGreen = ncollection.find({"light":"green"})
    counter = 0
    for i in knownRed:
        print 'start red' + str(counter)
        for j in i['on']:
            if j!=0:
                start1 = time.time()
                street1 = j
                print street1
                s1 = scollection.find_one({'name':j})
                s1Nodes = s1['refs']
                print "time1: " + str(time.time()-start1)
                start1 = time.time()
                print "S1NODES: " + str(len(s1Nodes))
                nodes = [ncollection.find_one({'name': g}) for g in s1Nodes]
                
                # for g in s1Nodes:
                    # f = ncollection.find_one({'name': g})
                    # nodes.append(f)
                
                print "time2: " + str(time.time()-start1)
                start1 = time.time()
                s1index = -1
                if i['name'] in s1Nodes:
                    s1index = s1Nodes.index(i['name'])
                else:
                    continue
                print "time3: " + str(time.time()-start1)
                rRange = closestRed(nodes, s1index)
                start1 = time.time()
                greenRange = closestGreen(nodes, s1index)
                print "time4: " + str(time.time()-start1)
                start1 = time.time()
                redRange = [max([rRange[0], greenRange[0]]), min([rRange[1], greenRange[1]])] 
                if redRange[1]-redRange[0]<4:
                    continue
                print "time5: " + str(time.time()-start1)
                start1 = time.time()
                for k in xrange(redRange[0], redRange[1]):
                    f = nodes[k]
                    if f is not None and f['light'] == 'none':
                        ncollection.update({'name':s1Nodes[k]},{'$set':{'light':'red'}})
                
                print "time2: " + str(time.time()-start1)
                start1 = time.time()
        counter+=1
    for i in knownGreen:
        print 'start green'
        for j in i['on']:
            if j!=0:
                start1 = time.time()
                street1 = j
                print street1
                s1 = scollection.find_one({'name':j})
                s1Nodes = s1['refs']
                print "time1: " + str(time.time()-start1)
                start1 = time.time()
                print "S1NODES: " + str(len(s1Nodes))
                nodes = [ncollection.find_one({'name': g}) for g in s1Nodes]
                
                # for g in s1Nodes:
                    # f = ncollection.find_one({'name': g})
                    # nodes.append(f)
                
                print "time2: " + str(time.time()-start1)
                start1 = time.time()
                s1index = -1
                if i['name'] in s1Nodes:
                    s1index = s1Nodes.index(i['name'])
                else:
                    continue
                print "time3: " + str(time.time()-start1)
                rRange = closestRed(nodes, s1index)
                start1 = time.time()
                greenRange = closestGreen(nodes, s1index)
                print "time4: " + str(time.time()-start1)
                start1 = time.time()
                greenRange = [max([rRange[0], greenRange[0]]), min([rRange[1], greenRange[1]])] 
                if greenRange[1]-greenRange[0]<4:
                    continue
                print "time5: " + str(time.time()-start1)
                start1 = time.time()
                for k in xrange(greenRange[0], greenRange[1]):
                    f = nodes[k]
                    if f is not None and f['light'] == 'none':
                        ncollection.update({'name':s1Nodes[k]},{'$set':{'light':'green'}})
                
                print "time2: " + str(time.time()-start1)
                start1 = time.time()
        counter+=1
    print 'end of round ' + str(counter)
    counter +=1
print 'Extrapolated!'
