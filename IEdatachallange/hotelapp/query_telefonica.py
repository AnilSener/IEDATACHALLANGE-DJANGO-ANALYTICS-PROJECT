__author__ = 'root'
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 13 06:26:39 2015

@author: root
"""

import json
from hotelapp.django.mongoserialize import MongoAwareEncoder
import pymongo

client = pymongo.MongoClient('localhost', 27017)
db = client['hotelapp']
collection = db['telefonica_map']
cursor=collection.find({"type": "Feature"})
import configparser

config = configparser.ConfigParser()
config.read('../app.conf')


features=[]
for feature in cursor:
    features.append(feature)

my_layer = {
    "type": "FeatureCollection",
    "features": features,
    "crs": {
        "type": "link",
        "properties": {"href": "telefonica.crs", "type": "proj4"} }}

with open("/root/Desktop/DataChallenge/telefonica2.geojson", "w") as f:
    f.write(json.dumps(my_layer, cls=MongoAwareEncoder, ensure_ascii=False))

import geojson
