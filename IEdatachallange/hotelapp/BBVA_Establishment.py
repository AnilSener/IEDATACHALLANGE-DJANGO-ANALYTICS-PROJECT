__author__ = 'root'


import geocoder
import pandas as pd
from geopy.geocoders import Nominatim
import numpy as np
from mongoengine.connection import connect,disconnect
import configparser

config = configparser.ConfigParser()
config.read('../app.conf')
connection=connect(config["MONGODB"]["DB_NAME"]);


from hotelapp.models import bbvaEstablishment

data= pd.read_csv(config["DEFAULT"]["DC_BASE_DIR"]+'data/bbva/customer_zipcodes000.csv', sep='\t')
print(data.head())



for i in range(data.shape[0]):
    print(i)
    if str(data.ix[i,4])!="unknown":
        b = bbvaEstablishment()
        #g = geocoder.google([float(data.ix[i,0]),float(data.ix[i,1])], method='reverse') #I tried geopy but it was giving bad results. I guess we don't need the actuall address
        b.type = "Feature"
        b.sector = data.ix[i,3]
        b.date = data.ix[i,2]
        b.clientZip = str(data.ix[i,4])
        b.merchants = data.ix[i,5]
        b.cards = data.ix[i,6]
        b.transactions = data.ix[i,7]
        b.average = data.ix[i,8]
        b.max= data.ix[i,9]
        b.min = data.ix[i,10]
        b.sd= data.ix[i,11]

        b.geometry = [data.ix[i,1],data.ix[i,0]]
        #if g!=None:
        #b.zipcode = g.postal
        b.save()


