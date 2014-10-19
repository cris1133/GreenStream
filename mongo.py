from pymongo import MongoClient
client = MongoClient()
db = client.test_database
scollection = db.street_collection
ncollection = db.node_collection
print ncollection.find({'light':'none'}).count()
print ncollection.find_one({'on':['67th Street','Columbus Avenue']})['name']
# for i in scollection.find():
    # print len(i['refs'])
