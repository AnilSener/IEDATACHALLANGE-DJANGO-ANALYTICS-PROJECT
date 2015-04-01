__author__ = 'root'

import configparser
config = configparser.ConfigParser()
config.read('../../app.conf')

from mongoengine.connection import connect,disconnect
connection=connect(config["MONGODB"]["DB_NAME"])
#Call to API:
import requests as rq
import json
from hotelapp.models import Hotel,BoundingBox,HotelProperty
import math

box=BoundingBox()
box.lat_min=float(config["GEOLOCATION"]["MIN_LAT"])
box.lat_max=float(config["GEOLOCATION"]["MAX_LAT"])
box.lon_min=float(config["GEOLOCATION"]["MIN_LON"])
box.lon_max=float(config["GEOLOCATION"]["MAX_LON"])
max_radius=box.get_Max_Radius()
#cities = ['bilbao', 'barakaldo', 'getxo', 'portugalete', 'santurtzi', 'basauri', 'leioa', 'sestao', 'galdakao', 'durango', 'erandio', 'amorebieta-etxano', 'bermeo', 'mungia', 'gernika-lumo']
#for city in cities:
r = rq.get('http://dev.api.ean.com/ean-services/rs/hotel/v3/list?apiKey=rdqjh2rkduun4tvh4kkhu6z5&cid=55505&customerIpAddress=89.140.177.130&customerUserAgent=Mozilla/5.0&locale=en_US&currencyCode=USD&countryCode=ESP&latitude='+str((box.lat_max+box.lat_min)/2)+'&longitude='+str((box.lon_max+box.lon_min)/2)+'&searchRadiusUnit=KM&searchRadius='+str(math.ceil(max_radius))) # Replace the id if not found.

#r = rq.get('http://dev.api.ean.com/ean-services/rs/hotel/v3/list?apiKey=rdqjh2rkduun4tvh4kkhu6z5&cid=55505&customerIpAddress=89.140.177.130&customerUserAgent=Mozilla/5.0&locale=en_US&currencyCode=USD&countryCode=ESP&city=amorebieta-etxano') # Replace the id if not found.
print(r.text)
hotels = json.loads(r.text)
hotels = hotels["HotelListResponse"]["HotelList"]["HotelSummary"]
#print(json.dumps(hotels, indent=2))

for hotel in hotels:

    if  float(hotel["latitude"]) >= box.lat_min and float(hotel["latitude"]) <= box.lat_max and float(hotel["longitude"]) >= box.lon_min and float(hotel["longitude"]) <= box.lon_max:
        h = Hotel()
        qs=Hotel.objects.filter(hotelID=hotel["hotelId"])
        if len(qs[:])>0:
            h=qs[:1].get()
        h.type = "Feature"
        h.hotelID = hotel["hotelId"]
        h.geometry = [hotel["longitude"],hotel["latitude"]]
        h.save()
        prop = HotelProperty()
        prop.name = hotel["name"]
        prop.address1 = hotel["address1"]
        prop.highRate = hotel["highRate"]

        prop.deepLink = hotel["deepLink"]
        prop.lowRate = hotel["lowRate"]
        try:
            prop.address2 = hotel["address2"]
        except Exception:
            prop.address2 = None
        prop.shortDescription = hotel["shortDescription"]
        prop.proximityDistance = hotel["proximityDistance"]
        prop.propertyCategory = hotel["propertyCategory"]
        prop.highRate = hotel["highRate"]
        prop.hotelRating = hotel["hotelRating"]
        try:
            prop.TripAdvisorRating = hotel["TripAdvisorRating"]
        except Exception:
            prop.TripAdvisorRating = None
        prop.city = hotel["city"]
        prop.confidenceRating = hotel["confidenceRating"]
        prop.locationDescription = hotel["locationDescription"]
        try:
            s = rq.get('http://dev.api.ean.com/ean-services/rs/hotel/v3/info?minorRev=28&apiKey=rdqjh2rkduun4tvh4kkhu6z5&cid=55505&customerIpAddress=89.140.177.130&customerUserAgent=Mozilla/5.0&locale=en_US&currencyCode=USD&hotelId='+str(h.hotelID))
            rooms = json.loads(s.text)
            prop.numberOfRooms = rooms["HotelInformationResponse"]["HotelDetails"]["numberOfRooms"]
        except Exception:
            prop.numberOfRooms = 0

        updated = Hotel.objects(hotelID=int(hotel["hotelId"])).update_one(set__properties=prop)
        if not updated:
            Hotel.objects.update_one(push__properties=prop)

disconnect()