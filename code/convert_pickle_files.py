{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 130,
   "metadata": {
    "collapsed": false
   },
   "outputs": [],
   "source": [
    "import matplotlib.pyplot as plt\n",
    "import numpy as np\n",
    "import pandas as pd\n",
    "from mpl_toolkits.basemap import Basemap\n",
    "from shapely.geometry import Point, Polygon, MultiPoint, MultiPolygon\n",
    "from shapely.prepared import prep\n",
    "import fiona\n",
    "from matplotlib.collections import PatchCollection\n",
    "from descartes import PolygonPatch\n",
    "import json\n",
    "import datetime\n",
    "import cPickle as pickle\n",
    "import os"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 131,
   "metadata": {
    "collapsed": false
   },
   "outputs": [
    {
     "ename": "IOError",
     "evalue": "[Errno 2] No such file or directory: 'data/Yield.pkl'",
     "output_type": "error",
     "traceback": [
      "\u001b[0;31m---------------------------------------------------------------------------\u001b[0m",
      "\u001b[0;31mIOError\u001b[0m                                   Traceback (most recent call last)",
      "\u001b[0;32m<ipython-input-131-e37ededf703f>\u001b[0m in \u001b[0;36m<module>\u001b[0;34m()\u001b[0m\n\u001b[0;32m----> 1\u001b[0;31m \u001b[0mentry\u001b[0m \u001b[0;34m=\u001b[0m \u001b[0mpd\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mread_pickle\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0;34m'data/Yield.pkl'\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m",
      "\u001b[0;32m//anaconda/lib/python2.7/site-packages/pandas/io/pickle.pyc\u001b[0m in \u001b[0;36mread_pickle\u001b[0;34m(path)\u001b[0m\n\u001b[1;32m     58\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m     59\u001b[0m     \u001b[0;32mtry\u001b[0m\u001b[0;34m:\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0;32m---> 60\u001b[0;31m         \u001b[0;32mreturn\u001b[0m \u001b[0mtry_read\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mpath\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m\u001b[1;32m     61\u001b[0m     \u001b[0;32mexcept\u001b[0m\u001b[0;34m:\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m     62\u001b[0m         \u001b[0;32mif\u001b[0m \u001b[0mPY3\u001b[0m\u001b[0;34m:\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n",
      "\u001b[0;32m//anaconda/lib/python2.7/site-packages/pandas/io/pickle.pyc\u001b[0m in \u001b[0;36mtry_read\u001b[0;34m(path, encoding)\u001b[0m\n\u001b[1;32m     54\u001b[0m             \u001b[0;31m# compat pickle\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m     55\u001b[0m             \u001b[0;32mexcept\u001b[0m\u001b[0;34m:\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0;32m---> 56\u001b[0;31m                 \u001b[0;32mwith\u001b[0m \u001b[0mopen\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mpath\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0;34m'rb'\u001b[0m\u001b[0;34m)\u001b[0m \u001b[0;32mas\u001b[0m \u001b[0mfh\u001b[0m\u001b[0;34m:\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m\u001b[1;32m     57\u001b[0m                     \u001b[0;32mreturn\u001b[0m \u001b[0mpc\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mload\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mfh\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0mencoding\u001b[0m\u001b[0;34m=\u001b[0m\u001b[0mencoding\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0mcompat\u001b[0m\u001b[0;34m=\u001b[0m\u001b[0mTrue\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m     58\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n",
      "\u001b[0;31mIOError\u001b[0m: [Errno 2] No such file or directory: 'data/Yield.pkl'"
     ]
    }
   ],
   "source": [
    "entry = pd.read_pickle('data/Yield.pkl')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {
    "collapsed": false
   },
   "outputs": [],
   "source": [
    "entry"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {
    "collapsed": false
   },
   "outputs": [],
   "source": [
    "entry.viewkeys()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {
    "collapsed": false
   },
   "outputs": [],
   "source": [
    "entry['geometry']['location']"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {
    "collapsed": false
   },
   "outputs": [],
   "source": [
    "entry['name']"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {
    "collapsed": false
   },
   "outputs": [],
   "source": [
    "entry['place_id']"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {
    "collapsed": false
   },
   "outputs": [],
   "source": [
    "data_list = os.listdir('data/')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {
    "collapsed": false
   },
   "outputs": [],
   "source": [
    "dict_list = []\n",
    "for dat in data_list:\n",
    "    print dat\n",
    "    with open('data/'+dat, 'r') as f:\n",
    "        dict_list.append(pickle.load(f))"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {
    "collapsed": true
   },
   "outputs": [],
   "source": [
    "df = pd.DataFrame(dict_list)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {
    "collapsed": false
   },
   "outputs": [],
   "source": [
    "newdf = df[['name','geometry', 'place_id', 'types']]"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {
    "collapsed": false
   },
   "outputs": [],
   "source": [
    "newdf['lat'] = newdf['geometry'].apply(lambda x: x['location']['lat'])\n",
    "newdf['long'] = newdf['geometry'].apply(lambda x: x['location']['lng'])\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {
    "collapsed": false
   },
   "outputs": [],
   "source": [
    "newdf.drop('geometry',axis=1,inplace=True)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {
    "collapsed": false
   },
   "outputs": [],
   "source": [
    "newdf"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {
    "collapsed": false
   },
   "outputs": [],
   "source": [
    "newdf.to_csv('data/newdf.csv', sep='\\t', encoding='utf-8')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {
    "collapsed": false
   },
   "outputs": [],
   "source": [
    "ls"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {
    "collapsed": false
   },
   "outputs": [],
   "source": [
    "cd data"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {
    "collapsed": false
   },
   "outputs": [],
   "source": [
    "ls"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {
    "collapsed": true
   },
   "outputs": [],
   "source": [
    "data = pd.read_csv('newdf.csv', delimiter='\\t')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {
    "collapsed": false
   },
   "outputs": [],
   "source": [
    "data.head()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {
    "collapsed": false
   },
   "outputs": [],
   "source": [
    "data.columns"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {
    "collapsed": true
   },
   "outputs": [],
   "source": [
    "data.drop('Unnamed: 0', axis=1, inplace=True)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {
    "collapsed": false
   },
   "outputs": [],
   "source": [
    "data.head()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {
    "collapsed": false
   },
   "outputs": [],
   "source": [
    "\n",
    "\n",
    "import pandas as pd\n",
    "import csv\n",
    "import itertools\n",
    "from math import radians, cos, sin, asin, sqrt\n",
    "\n",
    "\n",
    "def haversine(origin,\n",
    "              destination):\n",
    "    \"\"\"\n",
    "    Find distance between a pair of lat/lng coordinates\n",
    "    \"\"\"\n",
    "    # convert decimal degrees to radians\n",
    "    lat1, lon1, lat2, lon2 = map(radians, [float(origin[0]), float(origin[1]),float(destination[0]), float(destination[1])])\n",
    "    dlon = lon2 - lon1\n",
    "    dlat = lat2 - lat1\n",
    "    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2\n",
    "    c = 2 * asin(sqrt(a))\n",
    "    r = 3959  # Radius of earth in miles\n",
    "    return '%.2f' % (c * r)\n",
    "\n",
    "# Initialize Cleaning\n",
    "##############\n",
    "# Duplicates by coordinates (to 5dp)\n",
    "data['lat'] = data.lat.round(decimals=5)\n",
    "data['long'] = data.long.round(decimals=5)\n",
    "data = data.drop_duplicates(['lat', 'long'])\n",
    "\n",
    "# clean name\n",
    "data['name'] = data.name.str.upper()\n",
    "data['name'] = data.name.str.strip()\n",
    "print(data['name'].value_counts()[:10])\n",
    "\n",
    "# new dataframe for selected \"types\"\n",
    "print(data['types'].value_counts()[:10])\n",
    "data_cafe = data[data['types'].str.contains(\"cafe\")]\n",
    "data_restaurants = data[data['types'].str.contains(\"restaurant\")]\n",
    "data_parks = data[data['types'].str.contains(\"park\")]\n",
    "data_lodging = data[data['types'].str.contains(\"lodging\")]\n",
    "data_store = data[data['types'].str.contains(\"store\")]"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {
    "collapsed": false
   },
   "outputs": [],
   "source": [
    "data"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {
    "collapsed": false
   },
   "outputs": [],
   "source": [
    "data_cafe"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {
    "collapsed": false
   },
   "outputs": [],
   "source": [
    "data_restaurants"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {
    "collapsed": false
   },
   "outputs": [],
   "source": [
    "data_parks"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {
    "collapsed": false
   },
   "outputs": [],
   "source": [
    "data_lodging"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {
    "collapsed": false
   },
   "outputs": [],
   "source": [
    "data_store"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {
    "collapsed": false
   },
   "outputs": [],
   "source": [
    "#grab desired places from user_submitted ranking\n",
    "########################################################\n",
    "data['places'] = ''\n",
    "pd.options.mode.chained_assignment = None  # default='war\n",
    " \n",
    "\n",
    "# pick 1\n",
    "match = data.name.str.contains('(^REDWOOD)(.*)( )(REGIONAL)(.*)( )(PARK)')\n",
    "print(data['name'][match].value_counts()) # Check what hits we are getting\n",
    "print(\"Total: \",sum(match))\n",
    "data['places'][match] = \"RRP\"\n",
    "\n",
    "# pick 2\n",
    "match = data.name.str.contains('(^TOMALES)(.*)( )(BAY)(.*)( )(RESORT)(.*)( )(&)(.*)( )(MARINA)')\n",
    "print(data['name'][match].value_counts()) # Check what hits we are getting\n",
    "print(\"Total: \",sum(match))\n",
    "data['places'][match] = \"TBRM\"\n",
    "\n",
    "#pick 3\n",
    "match = data.name.str.contains('(^STABLE)(.*)( )(CAFE)')\n",
    "print(data['name'][match].value_counts()) # Check what hits we are getting\n",
    "print(\"Total: \",sum(match))\n",
    "data['places'][match] = \"SC\"\n",
    "\n",
    "\n",
    "#pick 4\n",
    "match = data.name.str.contains('(^BROWN)(.*)( )(SUGAR)(.*)( )(KITCHEN)')\n",
    "print(data['name'][match].value_counts()) # Check what hits we are getting\n",
    "print(\"Total: \",sum(match))\n",
    "data['places'][match] = \"BSK\"\n",
    "\n",
    "\n",
    "#pick 5\n",
    "match = data.name.str.contains('(^BLUE)(.*)( )(BOTTLE)(.*)( )(COFFEE)')\n",
    "print(data['name'][match].value_counts()) # Check what hits we are getting\n",
    "print(\"Total: \",sum(match))\n",
    "data['places'][match] = \"BBC\"\n",
    "\n",
    "# #pick 6\n",
    "# match = data.name.str.contains('(^insert)(.*)( )(pick6)')\n",
    "# print(data['name'][match].value_counts()) # Check what hits we are getting\n",
    "# print(\"Total: \",sum(match))\n",
    "# data['places'][match] = \"abbrev6\"\n",
    "\n",
    " \n",
    "# remove non-filtered entries and add an index\n",
    "data_filtered = data[data['places'] != \"\"]\n",
    "data_filtered['place_id'] = data_filtered.index\n",
    " \n",
    "print(data_filtered['places'].value_counts())\n",
    " \n",
    "# extract selected places in optimization inputs to a list\n",
    "\n",
    "all_places_lst = data_filtered[['name','lat', 'long', 'place_id']].values.tolist()\n",
    "print(len(all_places_lst))\n",
    "print all_places_lst"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {
    "collapsed": false
   },
   "outputs": [],
   "source": [
    "data_filtered"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {
    "collapsed": false
   },
   "outputs": [],
   "source": [
    "mission = [37.7599, -122.4148]\n",
    "\n",
    "cut_off = 20\n",
    "# Alo concatenate the ID with the name\n",
    "place_list = [[str(x[3])+\"_\"+x[0],x[1],x[2]] for x in all_places_lst if\n",
    "                  float(haversine(mission , [x[1],x[2]] )) <= cut_off]\n",
    " \n",
    "print(\"Cut list contains %d places\" % len(place_list)) "
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {
    "collapsed": false
   },
   "outputs": [],
   "source": [
    "\n",
    "cross_places = [[place_list[i],place_list[j]] \n",
    "                for i in range(len(place_list)) \n",
    "                for j in range(len(place_list)) \n",
    "                if i!=j] \n",
    "print(len(cross_places))  \n",
    " \n",
    "\n",
    "# # Filter out observations which are out of specified range\n",
    "# cut_off = (20/60)*10\n",
    "# cross_places = [x for x in cross_places if\n",
    "#                 (float(haversine( [x[0][1],x[0][2]] , [x[1][1],x[1][2]] )) <= cut_off)]\n",
    " \n",
    "# # Cut down crosses to:\n",
    "# print(len(cross_places))\n",
    "\n",
    "# export distances to calculate to a CSV\n",
    "#########################################\n",
    "f = open('walk_to_calculate.csv', 'w')\n",
    "w = csv.writer(f)\n",
    "w.writerow([\"place_A\", \"Lat_A\", \"Lon_A\", \"Store_B\", \"Lat_B\",\"Lon_B\"])\n",
    "for x in cross_places:\n",
    "    w.writerow([x[0][0],x[0][1],x[0][2],x[1][0],x[1][1],x[1][2]])\n",
    "f.close()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {
    "collapsed": true
   },
   "outputs": [],
   "source": [
    "\"\"\"\n",
    "Helper function to plot map\n",
    "\"\"\"\n",
    "def geo_network(all_places, places_in_group, connections, name='network_map.html', minutes=10):\n",
    "    \"\"\"\n",
    "    Helper function:\n",
    "    Plot the network on an easy-to-read google-map\n",
    "    \"\"\"\n",
    "    map = []\n",
    "    for x in all_places:\n",
    "        if x[0] in places_in_group:\n",
    "            # places in cliques\n",
    "            map.append(\"<marker name = \\\"%s\\\" lat = \\\"%.5f\\\" lng = \\\"%.5f\\\" col = \\\"red\\\"/>\"\n",
    "                       % (x[0],x[1],x[2]))\n",
    "        else:\n",
    "            # places not in cliques\n",
    "            map.append(\"<marker name = \\\"%s\\\" lat = \\\"%.5f\\\" lng = \\\"%.5f\\\" col = \\\"green\\\"/>\"\n",
    "                       % (x[0],x[1],x[2]))\n",
    "    for x in connections:\n",
    "        if float(x[-1]) <= minutes:\n",
    "            # Connections\n",
    "            map.append(\"<line latfrom = \\\"%.5f\\\" longfrom = \\\"%.5f\\\" latto = \\\"%.5f\\\" longto = \\\"%.5f\\\"/>\"\n",
    "                       % (float(x[1]),float(x[2]),float(x[4]),float(x[5]))) \n",
    "    # Map part 1\n",
    "    htmltext = \"\"\"<!DOCTYPE html >\n",
    " \n",
    "<style type=\"text/css\">\n",
    "                        html, body {\n",
    "                            height: 100%;\n",
    "                            width: 100%;\n",
    "                            padding: 0;\n",
    "                            margin: 0;\n",
    "                        }\n",
    "                        .labels {\n",
    "                            color: black;\n",
    "                            background-color: white;\n",
    "                            font-family: \"Lucida Grande\", \"Arial\", sans-serif;\n",
    "                    font-size: 10px;\n",
    "                            text-align: center;\n",
    "                    width: 45px;\n",
    "                            border: 0 solid black;\n",
    "                            white-space: nowrap;\n",
    "                        }\n",
    "                    </style>\n",
    " \n",
    "                    <html>\n",
    "                    <head>\n",
    "                    <meta name=\"viewport\" content=\"initial-scale=1.0, user-scalable=yes\" />\n",
    "                    <meta http-equiv=\"content-type\" content=\"text/html; charset=UTF-8\"/>\n",
    "                    <title>Network</title>\n",
    "                    <xml id=\"myxml\">\"\"\"\n",
    "    # Map part 2\n",
    "    for x in map:\n",
    "        htmltext += x + \"\\n\"\n",
    "     \n",
    "    # Map part 3\n",
    "    htmltext += \"\"\"\n",
    "            </xml>\n",
    "            <script type=\"text/javascript\" src=\"https://maps.googleapis.com/maps/api/js?&libraries=geometry\"></script>\n",
    "            <script type=\"text/javascript\" src=\"http://google-maps-utility-library-v3.googlecode.com/svn/trunk/markerwithlabel/src/markerwithlabel.js\"></script>\n",
    "            <script>\n",
    "            var XML = document.getElementById(\"myxml\");\n",
    "            if(XML.documentElement == null)\n",
    "            XML.documentElement = XML.firstChild;\n",
    "            var MARKERS = XML.getElementsByTagName(\"marker\");\n",
    "            var LINES = XML.getElementsByTagName(\"line\");\n",
    "            function initialize() {\n",
    "                 var mapOptions = {\n",
    "                                center: new google.maps.LatLng(37.76324,-122.41548),\n",
    "                                zoom: 12,\n",
    "                                styles:\n",
    "                                [\n",
    "                                {\"featureType\":\"administrative\",\"stylers\":[{ \"saturation\":-80},{\"visibility\":\"off\"}]},\n",
    "                                {\"featureType\":\"landscape.natural\",\"elementType\":\"geometry\",\"stylers\":[{\"color\":\"#d0e3b4\"}]},\n",
    "                                {\"featureType\":\"landscape.natural.terrain\",\"elementType\":\"geometry\",\"stylers\":[{\"visibility\":\"off\"}]},\n",
    "                                {\"featureType\":\"poi\",\"elementType\":\"labels\",\"stylers\":[{\"visibility\":\"on\"}]},\n",
    "                                {\"featureType\":\"poi.business\",\"elementType\":\"all\",\"stylers\":[{\"visibility\":\"off\"}]},\n",
    "                                {\"featureType\":\"poi.medical\",\"elementType\":\"geometry\",\"stylers\":[{\"color\":\"#fbd3da\"}]},\n",
    "                                {\"featureType\":\"poi.park\",\"elementType\":\"geometry\",\"stylers\":[{\"color\":\"#bde6ab\"}]},\n",
    "                                {\"featureType\":\"road\",\"elementType\":\"geometry.stroke\",\"stylers\":[{\"visibility\":\"off\"}]},\n",
    "                                {\"featureType\":\"road\",\"elementType\":\"labels\",\"stylers\":[{\"visibility\":\"off\"}]},\n",
    "                                {\"featureType\":\"road.highway\",\"elementType\":\"geometry.fill\",\"stylers\":[{\"color\":\"#ffe15f\"}]},\n",
    "                                {\"featureType\":\"road.highway\",\"elementType\":\"geometry.stroke\",\"stylers\":[{\"color\":\"#efd151\"}]},\n",
    "                                {\"featureType\":\"road.arterial\",\"elementType\":\"geometry.fill\",\"stylers\":[{\"color\":\"#ffffff\"}]},\n",
    "                                {\"featureType\":\"road.local\",\"elementType\":\"geometry.fill\",\"stylers\":[{\"color\":\"black\"}]},\n",
    "                                {\"featureType\":\"transit\",\"stylers\":[{\"visibility\":\"off\"}]},\n",
    "                                {\"featureType\":\"water\",\"elementType\":\"geometry\",\"stylers\":[{\"color\":\"#a2daf2\"}]}\n",
    "                                ]\n",
    "                        };\n",
    "                var map = new google.maps.Map(document.getElementById('map'),\n",
    "                    mapOptions);\n",
    "                var bounds = new google.maps.LatLngBounds();\n",
    "                for (var i = 0; i < MARKERS.length; i++) {\n",
    "                    var name = MARKERS[i].getAttribute(\"name\");\n",
    "                    var point_i = new google.maps.LatLng(\n",
    "                        parseFloat(MARKERS[i].getAttribute(\"lat\")),\n",
    "                        parseFloat(MARKERS[i].getAttribute(\"lng\")));\n",
    "                    var col =  MARKERS[i].getAttribute(\"col\")\n",
    "                    if (col == \"green\") {\n",
    "                        var ic = \"https://storage.googleapis.com/support-kms-prod/SNP_2752129_en_v0\"\n",
    "                    } else {\n",
    "                        var ic = \"https://storage.googleapis.com/support-kms-prod/SNP_2752125_en_v0\"\n",
    "                    }\n",
    "                    var marker = new MarkerWithLabel({\n",
    "                        position: point_i,\n",
    "                        map: map,\n",
    "                        icon: ic,\n",
    "                        //labelContent: name,\n",
    "                        labelAnchor: new google.maps.Point(22, 0),\n",
    "                        labelClass: \"labels\", // the CSS class for the label\n",
    "                        labelStyle: {opacity: 0.75},\n",
    "                    })\n",
    "                    bounds.extend(point_i);\n",
    "                };          \n",
    "            for (var i = 0; i < LINES.length; i++) {\n",
    "                var point_a = new google.maps.LatLng(\n",
    "                        parseFloat(LINES[i].getAttribute(\"latfrom\")),\n",
    "                        parseFloat(LINES[i].getAttribute(\"longfrom\")));\n",
    "                var point_b = new google.maps.LatLng(\n",
    "                        parseFloat(LINES[i].getAttribute(\"latto\")),\n",
    "                        parseFloat(LINES[i].getAttribute(\"longto\")));\n",
    "                var flightPlanCoordinates = [\n",
    "                    point_a,\n",
    "                    point_b\n",
    "                ];\n",
    "                var flightPath = new google.maps.Polyline({\n",
    "                    path: flightPlanCoordinates,\n",
    "                    geodesic: true,\n",
    "                    strokeColor: 'black',\n",
    "                    strokeOpacity: 1,\n",
    "                    strokeWeight: 1\n",
    "                });\n",
    "                flightPath.setMap(map);\n",
    "            };\n",
    "            }\n",
    "            google.maps.event.addDomListener(window, 'load', initialize);\n",
    "            </script>\n",
    "            </head>\n",
    "            <body>\n",
    "            <center>\n",
    " \n",
    "<div id=\"map\" style=\"width:95%; height:1200px;\"></div>\n",
    " \n",
    "            <center>\n",
    "            </body>\n",
    "            </html>       \n",
    "    \"\"\"\n",
    "    with open(name, 'w') as f:\n",
    "        f.write(htmltext)\n",
    "    f.close() "
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {
    "collapsed": false
   },
   "outputs": [],
   "source": [
    "\n",
    "import csv\n",
    "import networkx as nx  \n",
    "from pylab import *\n",
    " \n",
    "def is_problematic(grp):\n",
    "    if len(grp) > 2:\n",
    "        return True\n",
    "    return False\n",
    " \n",
    "def extract_clusters(clusters):  \n",
    "    \"\"\"\n",
    "    From a list of clusters/groups, extract unique stores\n",
    "    and the cluster if it is problematic\n",
    "    \"\"\"\n",
    "    lst_clqs = []  # Contains all the groups\n",
    "    unq_places_clq = [] # Contains stores in a clique\n",
    "    for c in clusters:\n",
    "        if is_problematic(c):\n",
    "            lst_clqs.append(c)\n",
    "            for x in c:\n",
    "                if x not in unq_places_clq:\n",
    "                    unq_places_clq.append(x)\n",
    "    return [lst_clqs,unq_places_clq]\n",
    " \n",
    "minutes = 60  # Adjusted to get a good example screenshot\n",
    " \n",
    "# Read in calculated distances\n",
    "#[store_a],[lat_a],[lon_a],[store_b],[lat_b],[lon_b],[time_min]\n",
    "in_data = []\n",
    "with open('walk_to_calculate.csv') as f:\n",
    "    reader = csv.reader(f)\n",
    "    headers = next(f)\n",
    "    for x in reader:\n",
    "        in_data.append(x)\n",
    "f.close()\n",
    " \n",
    "# Define an edge (or a connection) if a store is within 5 minutes of another store\n",
    "data_edges = [[x[0],x[3]] for x in in_data if float(x[-1]) <= minutes]\n",
    " \n",
    "# Add edges\n",
    "G=nx.Graph()\n",
    "G.add_edges_from(data_edges)\n",
    " \n",
    "# Clique Analysis\n",
    "find_cliq = nx.find_cliques(G)\n",
    "lst_clqs,unq_places_clq = extract_clusters(find_cliq)\n",
    "                 \n",
    "print(\"%d total places in analysis\" % len(place_list))\n",
    "print(\"%d places in problematic cliques:\" % len(unq_places_clq))  \n",
    " \n",
    "print(\"Problematic cliques:\")\n",
    "for x in lst_clqs:\n",
    "    print(x)\n",
    "     \n",
    "print(\"Alternatively, problematic clusters:\")\n",
    "for x in nx.connected_components(G):\n",
    "    print(x)\n",
    "     \n",
    "\n",
    "geo_network(place_list, unq_places_clq, in_data, 'unop_network_map.html', minutes) \n",
    " \n",
    "print(\"%.0f percent of stores in a problematic clique\" % (len(unq_places_clq)/len(place_list)*100))\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {
    "collapsed": false
   },
   "outputs": [],
   "source": [
    "from pulp import *\n",
    " \n",
    "\n",
    "prob = LpProblem(\"Maximise points kept\",LpMaximize)\n",
    " \n",
    "\n",
    "x = []\n",
    "for place in unq_places_clq:\n",
    "    x.append(LpVariable(place,0,1,LpInteger)) \n",
    "\n",
    "\n",
    "prob += pulp.lpSum(x[i] for i in range(len(unq_places_clq)))\n",
    "for one_clique in lst_clqs:   \n",
    "    prob += pulp.lpSum(\n",
    "        x[unq_places_clq.index(one_clique[i])] \n",
    "        for i in range(len(one_clique))) <= 2\n",
    "\n",
    "prob.writeLP(\"cliques.lp\")\n",
    "# Solve\n",
    "prob.solve()\n",
    "# The status of the solution is printed to the screen\n",
    "print(\"Status:\", LpStatus[prob.status])\n",
    "# Optimum variable values\n",
    "drop_points = []\n",
    "for v in prob.variables():\n",
    "    print(v.name, \"=\", v.varValue)\n",
    "    if v.varValue == 0:\n",
    "         drop_points.append(v.name)\n",
    "# Optimised objective function\n",
    "print(\"Number of points kept = \", int(value(prob.objective)))   \n",
    "# Dropping\n",
    "print(\"Number of points dropped = \", len(unq_places_clq) - int(value(prob.objective)))\n",
    "print drop_points"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {
    "collapsed": false
   },
   "outputs": [],
   "source": [
    "\"\"\"\n",
    "Test out our new number of cliques\n",
    "\"\"\"\n",
    "opt_edges = [x for x in data_edges if (x[0] not in drop_points and x[1] not in drop_points)]\n",
    "opt_in_data = [x for x in in_data if (x[0] not in drop_points and x[3] not in drop_points)]\n",
    "opt_place_list = [x for x in place_list if x[0] not in drop_points]\n",
    "# Add edges\n",
    "opt_G=nx.Graph()\n",
    "opt_G.add_edges_from(opt_edges)\n",
    "# Clique Analysis\n",
    "opt_find_cliq = nx.find_cliques(opt_G)\n",
    "opt_lst_clqs,opt_unq_places_clq = extract_clusters(find_cliq)\n",
    "print(\"located %d places in a problematic clique\" % len(opt_unq_places_clq))\n",
    "# Geographic Diagram (instead)\n",
    "geo_network(opt_place_list, opt_unq_places_clq, opt_in_data, 'opt_network_map.html', minutes)      \n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {
    "collapsed": false
   },
   "outputs": [],
   "source": []
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {
    "collapsed": true
   },
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 2",
   "language": "python",
   "name": "python2"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 2
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython2",
   "version": "2.7.11"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 0
}
