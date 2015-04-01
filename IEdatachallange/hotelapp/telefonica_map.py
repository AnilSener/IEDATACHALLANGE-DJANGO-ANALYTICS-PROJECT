# -*- coding: utf-8 -*-
"""
Created on Fri Feb 13 04:57:49 2015

@author: root
"""

import fiona
import pymongo
from fiona.crs import from_string
import os
#import logging
#from pyproj import Proj, transform
import configparser
config = configparser.ConfigParser()
config.read('../app.conf')
from mongoengine.connection import connect,disconnect
connection=connect(config["MONGODB"]["DB_NAME"])
from hotelapp.models import TelefonicaMap,Property
#features = []
crs = None



with fiona.collection(config["DEFAULT"]["DC_BASE_DIR"]+"data/telefonica/MGrid_WKT_Bizkaia_WGS84/MGrid_WKT_Bizkaia_WGS84.shp", "r") as source:
    crsdict = from_string("+datum=WGS84 +ellps=WGS84 +no_defs +proj=longlat")
    for feat in source:
        #feat['properties'].update(...) # with your attributes
        #print(feat)
        #features.append(feat)
        tm=TelefonicaMap()
        tm.geometry=feat['geometry']
        tm.type=feat['type']
        tm.featureID=int(feat['id'])
        tm.save()
        prop=Property()

        prop.WKT=feat['properties']['WKT']
        prop.cell_id=int(float(feat['properties']['field_1']))
        prop.field_2=int(feat['properties']['field_2'])
        prop.field_3=float(feat['properties']['field_3'])
        prop.field_4=float(feat['properties']['field_4'])
        prop.field_5=float(feat['properties']['field_5'])
        prop.field_6=float(feat['properties']['field_6'])
        prop.field_7=float(feat['properties']['field_7'])
        prop.field_9=str(feat['properties']['field_9'])
        updated = TelefonicaMap.objects(featureID=int(feat['id'])).update_one(set__properties=prop)
        if not updated:
            TelefonicaMap.objects.update_one(push__properties=prop)
    crs = " ".join("+%s=%s" % (k,v) for k,v in crsdict.items())

with open("telefonica.crs", "w") as f:
    f.write(crs)

print(crsdict)
disconnect()
"""client = pymongo.MongoClient('localhost', 27017)
db = client['hotelapp']
collection = db['telefonica_map']
telefonica_feature_ids = collection.insert(features)"""




