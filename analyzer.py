# Dijkstra's algorithm for shortest paths
# David Eppstein, UC Irvine, 4 April 2002
from pymongo import MongoClient
import time
# http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/117228
from priodict import priorityDictionary
from math import radians, cos, sin, asin, sqrt
def nodeDist (node1, node2, time):
    lon1,lat1=node1['coor']
    lon2,lat2=node2['coor']
    dist, slope = haversine(lon1, lat1, lon2, lat2) #distance in minutes
    invertedLight = False
    if node2['light']=='na':
        return dist
    state = node2['light']=='green'
    if slope<=0:
        invertedLight = True
    if invertedLight == False:
        if state:
            timeleft = node2['lastLight'] + node2['dg']-time
            if timeleft>dist:
                return dist
            else:
                return dist + node2['dr']
        else:
            timeleft = node2['lastLight']+node2['dr']-time
            if timeleft<dist:
                return dist
            else:
                return timeleft
    else:
        if state:
            timeleft = node2['lastLight'] + node2['dg']-time
            if timeleft>dist:
                return timeleft
            else:
                return dist
        else:
            timeleft = node2['lastLight']+node2['dr']-time
            if timeleft<dist:
                return dist + node2['dr']
            else:
                return dist
    
def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 

    # 6367 km is the radius of the Earth
    mi = 3959 * c
    return mi/25*60, dlat/dlon
def Dijkstra(start,end=None):
	client = MongoClient()
    db = client.test_database
    ncollection = db.node_collection"""
	Find shortest paths from the start vertex to all
	vertices nearer than or equal to the end.

	The input graph G is assumed to have the following
	representation: A vertex can be any object that can
	be used as an index into a dictionary.  G is a
	dictionary, indexed by vertices.  For any vertex v,
	G[v] is itself a dictionary, indexed by the neighbors
	of v.  For any edge v->w, G[v][w] is the length of
	the edge.  This is related to the representation in
	<http://www.python.org/doc/essays/graphs.html>
	where Guido van Rossum suggests representing graphs
	as dictionaries mapping vertices to lists of neighbors,
	however dictionaries of edges have many advantages
	over lists: they can store extra information (here,
	the lengths), they support fast existence tests,
	and they allow easy modification of the graph by edge
	insertion and removal.  Such modifications are not
	needed here but are important in other graph algorithms.
	Since dictionaries obey iterator protocol, a graph
	represented as described here could be handed without
	modification to an algorithm using Guido's representation.

	Of course, G and G[v] need not be Python dict objects;
	they can be any other object that obeys dict protocol,
	for instance a wrapper in which vertices are URLs
	and a call to G[v] loads the web page and finds its links.
	
	The output is a pair (D,P) where D[v] is the distance
	from start to v and P[v] is the predecessor of v along
	the shortest path from s to v.
	
	Dijkstra's algorithm is only guaranteed to work correctly
	when all edge lengths are positive. This code does not
	verify this property for all edges (only the edges seen
 	before the end vertex is reached), but will correctly
	compute shortest paths even for some graphs with negative
	edges, and will raise an exception if it discovers that
	a negative edge has caused it to make a mistake.
	"""

	D = {}	# dictionary of final distances
	P = {}	# dictionary of predecessors
	Q = priorityDictionary()   # est.dist. of non-final vert.
	Q[start] = 0
	
	for v in Q:
		D[v] = Q[v]
		if v == end: break
        curnode = ncollection.find_one({'name':v})
		availablenodes = curnode['availableNodes']
		for node in availablenodes:
            nnode = ncollection.find_one({'name':node})
            
			vwLength = D[v] + nodeDist(curnode, nnode, time.time()+D[node]
			if node in D:
				if vwLength < D[node]:
					raise ValueError, \
  "Dijkstra: found better path to already-final vertex"
			elif node not in Q or vwLength < Q[w]:
				Q[node] = vwLength
				P[node] = v
	
	return (D,P)		
def shortestPath(start,end):
	"""
	Find a single shortest path from the given start vertex
	to the given end vertex.
	The input has the same conventions as Dijkstra().
	The output is a list of the vertices in order along
	the shortest path.
	"""

	D,P = Dijkstra(start,end)
	Path = []
	while 1:
		Path.append(end)
		if end == start: break
		end = P[end]
	Path.reverse()
	return Path
