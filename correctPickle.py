from pymongo import MongoClient
import pickle
client = MongoClient()
db = client.test_database
ncollection = db.node_collection
lightList = pickle.load(open("fakeit.p", "rb"))
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
pickle.dump(lightList, open("fakeit1.p", "wb"))