
# coding: utf-8

# In[1]:

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from mpl_toolkits.basemap import Basemap
from shapely.geometry import Point, Polygon, MultiPoint, MultiPolygon
from shapely.prepared import prep
import fiona
from matplotlib.collections import PatchCollection
from descartes import PolygonPatch
import json
import datetime
import cPickle as pickle
import os
import csv
import itertools
from math import radians, cos, sin, asin, sqrt

from matplotlib import rc
rc('font', **{'family':'sans-serif',
    'sans-serif':['Helvetica'],
    'monospace': ['Inconsolata'],
    'serif': ['Adobe Garamamond Pro']})


data_list = os.listdir('place/')


dict_list = []
for dat in data_list:
    print dat
    with open('place/'+dat, 'r') as f:
        dict_list.append(pickle.load(f))



df = pd.DataFrame(dict_list)
newdf = df[['name','geometry', 'place_id', 'types']]
newdf['lat'] = newdf['geometry'].apply(lambda x: x['location']['lat'])
newdf['long'] = newdf['geometry'].apply(lambda x: x['location']['lng'])
newdf.drop('geometry',axis=1,inplace=True)


newdf.to_csv('places/newdf.csv', sep='\t', encoding='utf-8')
data = pd.read_csv('places/newdf.csv', delimiter='\t')
data.drop('Unnamed: 0', axis=1, inplace=True)



def haversine(origin,
              destination):
    """
    Find distance between a pair of lat/lng coordinates
    """
    # convert decimal degrees to radians
    lat1, lon1, lat2, lon2 = map(radians, [float(origin[0]), float(origin[1]),float(destination[0]), float(destination[1])])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2.)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2.)**2
    c = 2 * asin(sqrt(a))
    r = 3959  # Radius of earth in miles
    return '%.2f' % (c * r)


#data cleaning
data['name'] = data.name.str.upper()
data['name'] = data.name.str.strip()
print(data['name'].value_counts()[:10])

# new dataframe for selected "types"
print(data['types'].value_counts()[:10])
data_cafe = data[data['types'].str.contains("cafe")]
data_restaurants = data[data['types'].str.contains("restaurant")]
data_parks = data[data['types'].str.contains("park")]
data_lodging = data[data['types'].str.contains("lodging")]
data_store = data[data['types'].str.contains("store")]

#grab desired places from user_submitted ranking
########################################################
data['places'] = ''
pd.options.mode.chained_assignment = None  # default='war


# pick 1
match = data.name.str.contains('(^REDWOOD)(.*)( )(REGIONAL)(.*)( )(PARK)')
print(data['name'][match].value_counts()) # Check what hits we are getting
print("Total: ",sum(match))
data['places'][match] = "RRP"

# pick 2
match = data.name.str.contains('(^TOMALES)(.*)( )(BAY)(.*)( )(RESORT)(.*)( )(&)(.*)( )(MARINA)')
print(data['name'][match].value_counts()) # Check what hits we are getting
print("Total: ",sum(match))
data['places'][match] = "TBRM"

#pick 3
match = data.name.str.contains('(^STABLE)(.*)( )(CAFE)')
print(data['name'][match].value_counts()) # Check what hits we are getting
print("Total: ",sum(match))
data['places'][match] = "SC"


#pick 4
match = data.name.str.contains('(^BROWN)(.*)( )(SUGAR)(.*)( )(KITCHEN)')
print(data['name'][match].value_counts()) # Check what hits we are getting
print("Total: ",sum(match))
data['places'][match] = "BSK"


#pick 5
match = data.name.str.contains('(^BLUE)(.*)( )(BOTTLE)(.*)( )(COFFEE)')
print(data['name'][match].value_counts()) # Check what hits we are getting
print("Total: ",sum(match))
data['places'][match] = "BBC"

#pick 6
match = data.name.str.contains('(^CHEESE)(.*)( )(BOARD)(.*)( )(PIZZA)')
print(data['name'][match].value_counts()) # Check what hits we are getting
print("Total: ",sum(match))
data['places'][match] = "CBP"


#pick 7
match = data.name.str.contains('(^THE)(.*)( )(SLANTED)(.*)( )(DOOR)')
print(data['name'][match].value_counts()) # Check what hits we are getting
print("Total: ",sum(match))
data['places'][match] = "TSD"


# remove non-filtered entries and add an index
data_filtered = data[data['places'] != ""]
data_filtered['place_id'] = data_filtered.index

print(data_filtered['places'].value_counts())

# extract selected places in optimization inputs to a list

all_places_lst = data_filtered[['name','lat', 'long', 'place_id']].values.tolist()
print(len(all_places_lst))
print all_places_lst

#initialize cut based on location parameters

mission = [37.7599, -122.4148]

cut_off = 20
# Alo concatenate the ID with the name
place_list = [[str(x[3])+"_"+x[0],x[1],x[2]] for x in all_places_lst if
                  float(haversine(mission , [x[1],x[2]] )) <= cut_off]

print("Cut list contains %d places" % len(place_list))
print place_list


#identify cross_places
cross_places = [[place_list[i],place_list[j]]
                for i in range(len(place_list))
                for j in range(len(place_list))
                if i!=j]
print(len(cross_places))
print cross_places


# export distances to calculate to a CSV
#########################################
f = open('walk_to_calculate.csv', 'w')
w = csv.writer(f)
w.writerow(["place_A", "Lat_A", "Lon_A", "place_B", "Lat_B","Lon_B"])
for x in cross_places:
    w.writerow([x[0][0],x[0][1],x[0][2],x[1][0],x[1][1],x[1][2]])
f.close()


"""
define function to plot map
"""
def geo_network(all_places, places_in_group, connections, name='network_map.html', minutes=120):
    """
    Helper function:
    Plot the network on an easy-to-read google-map
    """
    map = []
    for x in all_places:
        if x[0] in places_in_group:
            # places in cliques
            map.append("<marker name = \"%s\" lat = \"%.5f\" lng = \"%.5f\" col = \"red\"/>"
                       % (x[0],x[1],x[2]))
        else:
            # places not in cliques
            map.append("<marker name = \"%s\" lat = \"%.5f\" lng = \"%.5f\" col = \"green\"/>"
                       % (x[0],x[1],x[2]))
    for x in connections:
        if float(x[-1]) <= minutes:
            # Connections
            map.append("<line latfrom = \"%.5f\" longfrom = \"%.5f\" latto = \"%.5f\" longto = \"%.5f\"/>"
                       % (float(x[1]),float(x[2]),float(x[4]),float(x[5])))
    # Map part 1
    htmltext = """<!DOCTYPE html >

<style type="text/css">
                        html, body {
                            height: 100%;
                            width: 100%;
                            padding: 0;
                            margin: 0;
                        }
                        .labels {
                            color: black;
                            background-color: white;
                            font-family: "Lucida Grande", "Arial", sans-serif;
                    font-size: 10px;
                            text-align: center;
                    width: 45px;
                            border: 0 solid black;
                            white-space: nowrap;
                        }
                    </style>

                    <html>
                    <head>
                    <meta name="viewport" content="initial-scale=1.0, user-scalable=yes" />
                    <meta http-equiv="content-type" content="text/html; charset=UTF-8"/>
                    <title>Network</title>
                    <xml id="myxml">"""
    # Map part 2
    for x in map:
        htmltext += x + "\n"

    # Map part 3
    htmltext += """
            </xml>
            <script type="text/javascript" src="https://maps.googleapis.com/maps/api/js?&libraries=geometry"></script>
            <script type="text/javascript" src="http://google-maps-utility-library-v3.googlecode.com/svn/trunk/markerwithlabel/src/markerwithlabel.js"></script>
            <script>
            var XML = document.getElementById("myxml");
            if(XML.documentElement == null)
            XML.documentElement = XML.firstChild;
            var MARKERS = XML.getElementsByTagName("marker");
            var LINES = XML.getElementsByTagName("line");
            function initialize() {
                 var mapOptions = {
                                center: new google.maps.LatLng(37.76324,-122.41548),
                                zoom: 12,
                                styles:
                                [
                                {"featureType":"administrative","stylers":[{ "saturation":-80},{"visibility":"off"}]},
                                {"featureType":"landscape.natural","elementType":"geometry","stylers":[{"color":"#d0e3b4"}]},
                                {"featureType":"landscape.natural.terrain","elementType":"geometry","stylers":[{"visibility":"off"}]},
                                {"featureType":"poi","elementType":"labels","stylers":[{"visibility":"on"}]},
                                {"featureType":"poi.business","elementType":"all","stylers":[{"visibility":"off"}]},
                                {"featureType":"poi.medical","elementType":"geometry","stylers":[{"color":"#fbd3da"}]},
                                {"featureType":"poi.park","elementType":"geometry","stylers":[{"color":"#bde6ab"}]},
                                {"featureType":"road","elementType":"geometry.stroke","stylers":[{"visibility":"off"}]},
                                {"featureType":"road","elementType":"labels","stylers":[{"visibility":"off"}]},
                                {"featureType":"road.highway","elementType":"geometry.fill","stylers":[{"color":"#ffe15f"}]},
                                {"featureType":"road.highway","elementType":"geometry.stroke","stylers":[{"color":"#efd151"}]},
                                {"featureType":"road.arterial","elementType":"geometry.fill","stylers":[{"color":"#ffffff"}]},
                                {"featureType":"road.local","elementType":"geometry.fill","stylers":[{"color":"black"}]},
                                {"featureType":"transit","stylers":[{"visibility":"off"}]},
                                {"featureType":"water","elementType":"geometry","stylers":[{"color":"#a2daf2"}]}
                                ]
                        };
                var map = new google.maps.Map(document.getElementById('map'),
                    mapOptions);
                var bounds = new google.maps.LatLngBounds();
                for (var i = 0; i < MARKERS.length; i++) {
                    var name = MARKERS[i].getAttribute("name");
                    var point_i = new google.maps.LatLng(
                        parseFloat(MARKERS[i].getAttribute("lat")),
                        parseFloat(MARKERS[i].getAttribute("lng")));
                    var col =  MARKERS[i].getAttribute("col")
                    if (col == "green") {
                        var ic = "https://storage.googleapis.com/support-kms-prod/SNP_2752129_en_v0"
                    } else {
                        var ic = "https://storage.googleapis.com/support-kms-prod/SNP_2752125_en_v0"
                    }
                    var marker = new MarkerWithLabel({
                        position: point_i,
                        map: map,
                        icon: ic,
                        //labelContent: name,
                        labelAnchor: new google.maps.Point(22, 0),
                        labelClass: "labels", // the CSS class for the label
                        labelStyle: {opacity: 0.75},
                    })
                    bounds.extend(point_i);
                };
            for (var i = 0; i < LINES.length; i++) {
                var point_a = new google.maps.LatLng(
                        parseFloat(LINES[i].getAttribute("latfrom")),
                        parseFloat(LINES[i].getAttribute("longfrom")));
                var point_b = new google.maps.LatLng(
                        parseFloat(LINES[i].getAttribute("latto")),
                        parseFloat(LINES[i].getAttribute("longto")));
                var flightPlanCoordinates = [
                    point_a,
                    point_b
                ];
                var flightPath = new google.maps.Polyline({
                    path: flightPlanCoordinates,
                    geodesic: true,
                    strokeColor: 'black',
                    strokeOpacity: 1,
                    strokeWeight: 1
                });
                flightPath.setMap(map);
            };
            }
            google.maps.event.addDomListener(window, 'load', initialize);
            </script>
            </head>
            <body>
            <center>

<div id="map" style="width:95%; height:1200px;"></div>

            <center>
            </body>
            </html>
    """
    with open(name, 'w') as f:
        f.write(htmltext)
    f.close()


# In[66]:


import csv
import networkx as nx
from pylab import *

def is_problematic(grp):
    if len(grp) > 2:
        return True
    return False

def extract_clusters(clusters):
    """
    From a list of clusters/groups, extract unique places
    and the cluster if it is problematic
    """
    lst_clqs = []  # Contains all the groups
    unq_places_clq = [] # Contains places in a clique
    for c in clusters:
        if is_problematic(c):
            lst_clqs.append(c)
            for x in c:
                if x not in unq_places_clq:
                    unq_places_clq.append(x)
    return [lst_clqs,unq_places_clq]

minutes = 10000

# Read in calculated distances
#[store_a],[lat_a],[lon_a],[store_b],[lat_b],[lon_b],[time_min]
in_data = []
with open('walk_to_calculate.csv') as f:
    reader = csv.reader(f)
    headers = next(f)
    for x in reader:
        in_data.append(x)
f.close()

# data_edges = [[x[0],x[3]] for x in in_data if float(x[-1]) <= minutes]
#print in_data
#print x[4]
#print x[5]

data_edges = [(x[0],x[3], {'weight': float(haversine([x[4], x[5]], [x[1],x[2]]))}) for x in in_data if float(x[-1]) <= minutes]
# Add edges
G=nx.Graph()
G.add_edges_from(data_edges)

# Clique Analysis
find_cliq = nx.find_cliques(G)
lst_clqs,unq_places_clq = extract_clusters(find_cliq)

print("%d total places in analysis" % len(place_list))
print("%d places in problematic cliques:" % len(unq_places_clq))

print("Problematic cliques:")
for x in lst_clqs:
    print(x)

print("Alternatively, problematic clusters:")
for x in nx.connected_components(G):
    print(x)


geo_network(place_list, unq_places_clq, in_data, 'unop_network_map.html', minutes)

print("%.0f percent of places in a problematic clique" % (len(unq_places_clq)/len(place_list)*100))


# In[41]:

from pulp import *


prob = LpProblem("Maximise points kept",LpMaximize)


x = []
for place in unq_places_clq:
    x.append(LpVariable(place,0,1,LpInteger))


prob += pulp.lpSum(x[i] for i in range(len(unq_places_clq)))
for one_clique in lst_clqs:
    prob += pulp.lpSum(
        x[unq_places_clq.index(one_clique[i])]
        for i in range(len(one_clique))) <= 2

prob.writeLP("cliques.lp")
# Solve
prob.solve()
# The status of the solution is printed to the screen
print("Status:", LpStatus[prob.status])
# Optimum variable values
drop_points = []
for v in prob.variables():
    print(v.name, "=", v.varValue)
    if v.varValue == 0:
         drop_points.append(v.name)

print prob.objective


print("Number of points kept = ", int(value(prob.objective)))
# Dropping
print("Number of points dropped = ", len(unq_places_clq) - int(value(prob.objective)))
print drop_points


# In[42]:

"""
Test out our new number of cliques
"""
opt_edges = [x for x in data_edges if (x[0] not in drop_points and x[1] not in drop_points)]
opt_in_data = [x for x in in_data if (x[0] not in drop_points and x[3] not in drop_points)]
opt_place_list = [x for x in place_list if x[0] not in drop_points]
print opt_place_list
print opt_edges


# Add edges
opt_G=nx.Graph()
opt_G.add_edges_from(opt_edges)
pos = nx.spring_layout(opt_G)
nx.draw(opt_G,pos,node_color='b', with_labels=True)
# Clique Analysis
opt_find_cliq = nx.find_cliques(opt_G)
opt_lst_clqs,opt_unq_places_clq = extract_clusters(find_cliq)

print("located %d places in a problematic clique" % len(opt_unq_places_clq))

# Geographic Diagram (instead)
geo_network(opt_place_list, opt_unq_places_clq, opt_in_data, 'opt_network_map.html', minutes)


points = data_filtered[['lat','long']]

points.to_csv('points.csv', sep='\t', encoding='utf-8')
points.head()


f = open('points.csv', 'w')
w = csv.writer(f)
w.writerow(["place_A", "Lat_A", "Lon_A", "place_B", "Lat_B","Lon_B"])
for x in cross_places:
    w.writerow([x[0][0],x[0][1],x[0][2],x[1][0],x[1][1],x[1][2]])
f.close()

in_points = []
with open('points.csv') as f:
    reader = csv.reader(f)
    headers = next(f)
    for x in reader:
        in_points.append(x)
f.close()

print in_points

new_data_edges = [(x[0],x[3], {'weight': float(haversine([x[4], x[5]], [x[1],x[2]]))}) for x in in_data]


G_new=nx.Graph()
G_new.add_edges_from(new_data_edges)
pos = nx.spring_layout(G_new)
path = nx.shortest_path(G_new)
nx.draw(G_new,pos,node_color='b', with_labels=True, font_size=10)
 
# Clique Analysis
find_cliq = nx.find_cliques(G_new)
lst_clqs,unq_places_clq = extract_clusters(find_cliq)
print lst_clqs

new = points[['lat','long']]

from scipy.spatial.distance import pdist, squareform
distxy = squareform(pdist(new, metric='euclidean'))
print distxy


from scipy.cluster.hierarchy import linkage, dendrogram
R = dendrogram(linkage(distxy, method='complete'))


nx.clustering(G)
nx.clustering(opt_G)
nx.shortest_path(opt_G)
nx.all_pairs_shortest_path(opt_G, cutoff = 3)
nx.all_pairs_shortest_path(opt_G, cutoff = 4)
nx.dijkstra_path(G_new, '26_BLUE BOTTLE COFFEE','38_CHEESE BOARD PIZZA')
nx.dijkstra_path(G_new, '38_CHEESE BOARD PIZZA','158_TILDEN REGIONAL PARK')
nx.dijkstra_path(G_new,'142_STABLE CAFE','158_TILDEN REGIONAL PARK')
nx.dijkstra_path(G_new,'38_CHEESE BOARD PIZZA','142_STABLE CAFE')
nx.closeness_vitality(opt_G, weight='haversine')
nx.dijkstra_path(opt_G, '26_BLUE BOTTLE COFFEE','38_CHEESE BOARD PIZZA')
nx.dijkstra_path(opt_G, '38_CHEESE BOARD PIZZA','132_REDWOOD REGIONAL PARK')
nx.dijkstra_path(opt_G,'142_STABLE CAFE','132_REDWOOD REGIONAL PARK')
nx.dijkstra_path(opt_G,'38_CHEESE BOARD PIZZA','142_STABLE CAFE')
