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

data_list = os.listdir('data/')

dict_list = []
for dat in data_list:
    print dat
    with open('data/'+dat, 'r') as f:
        dict_list.append(pickle.load(f))


df = pd.DataFrame(dict_list)
