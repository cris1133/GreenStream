from imposm.parser import OSMParser
import matplotlib.pyplot as plt
from pymongo import MongoClient


# simple class that handles the parsed OSM data.
class Streetlight(object):  
    def nodes(self, nodes):
        client = MongoClient()
        db = client.test_database
        scollection = db.street_collection
        ncollection = db.node_collection
        # callback method for ways
        for osmid, tags, refs in nodes:
            if 'highway' in tags:
                tag = tags['highway']
                if tag=='stop':
                    ncollection.update({"name":osmid}, {'$set':{'light':'na'}})
                if tag== 'traffic_signals':
                    ncollection.update({"name":osmid}, {'$set':{'light':'none'}})
                    # instantiate counter and parser and start parsing
def main():
    counter = Streetlight()
    c = OSMParser(concurrency=4, nodes_callback=counter.nodes)
    c.parse_xml_file('map')
    print 'operation complete!'
    
if __name__=="__main__":
    main()
