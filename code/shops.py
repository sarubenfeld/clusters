

import pandas as pd
import csv
import itertools
from math import radians, cos, sin, asin, sqrt


def haversine(origin,
              destination):
    """
    Find distance between a pair of lat/lng coordinates
    """
    # convert decimal degrees to radians
    lat1, lon1, lat2, lon2 = map(radians, [float(origin[0]), float(origin[1]),
                                           float(destination[0]), float(destination[1])])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    r = 3959  # Radius of earth in miles
    return '%.2f' % (c * r)

# Read in-data
##############
# Contains a data-dump of all coffee-shops in London (with co-ordinates)
data_csv = 'coffee_python_mined.csv'
data_pd = pd.read_csv(data_csv, sep=',', header=0)

# Clean a bit
##############
# Duplicates by coordinates (to 5dp)
data_pd['Latitude'] = data_pd.Latitude.round(decimals=5)
data_pd['Longitude'] = data_pd.Longitude.round(decimals=5)
data_pd = data_pd.drop_duplicates(['Latitude', 'Longitude'])

# Clean Name
data_pd['Name'] = data_pd.Name.str.upper()
data_pd['Name'] = data_pd.Name.str.strip()
print(data_pd['Name'].value_counts()[:10])

# Drop if Type is not 'cafe'
print(data_pd['Type'].value_counts()[:10])
data_pd = data_pd[data_pd['Type'].str.contains("cafe")]

# Isolate desired shop(s): STARBUCKS, CAFE NERO, COSTA COFFEE
########################################################
data_pd['Shop'] = ''
pd.options.mode.chained_assignment = None  # default='war

# STARBUCKS
match = data_pd.Name.str.contains('(^STARBUC)')
print(data_pd['Name'][match].value_counts()) # Check what hits we are getting
print("Total: ",sum(match))
data_pd['Shop'][match] = "SB"
# CAFE NERO
match = data_pd.Name.str.contains('(^CAF)(.*)( )(NER)')
print(data_pd['Name'][match].value_counts()) # Check what hits we are getting
print("Total: ",sum(match))
data_pd['Shop'][match] = "CN"
# COSTA COFFEE
match = data_pd.Name.str.contains('(^COST)(.*)( )(COF)')
print(data_pd['Name'][match].value_counts()) # Check what hits we are getting
print("Total: ",sum(match))
data_pd['Shop'][match] = "CC"

# Remove non-filtered and add an index
data_pd = data_pd[data_pd['Shop'] != ""]
data_pd['ID'] = data_pd.index

print(data_pd['Shop'].value_counts())

# Extract to a list
###################
all_stores_lst = data_pd[['Shop','Latitude','Longitude','ID']].values.tolist()
print(len(all_stores_lst))
