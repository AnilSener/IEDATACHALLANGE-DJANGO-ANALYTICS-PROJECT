__author__ = 'root'

import configparser
config = configparser.ConfigParser()
config.read('../../app.conf')
from mongoengine.connection import connect,disconnect
connection=connect(config["MONGODB"]["DB_NAME"])
#Call to API:
import requests as rq
import json
from hotelapp.models import Hotel,BoundingBox, Room
import math
box=BoundingBox()
box.lat_min=float(config["GEOLOCATION"]["MIN_LAT"])
box.lat_max=float(config["GEOLOCATION"]["MAX_LAT"])
box.lon_min=float(config["GEOLOCATION"]["MIN_LON"])
box.lon_max=float(config["GEOLOCATION"]["MAX_LON"])
max_radius=box.get_Max_Radius()

#url = []
for i in range(14,30): #Loop through dates of March
    for hotel in Hotel.objects: #Loop through hotels
        #print(str(hotel.hotelID))
        url = 'http://dev.api.ean.com/ean-services/rs/hotel/v3/avail?minorRev=28&apiKey=rdqjh2rkduun4tvh4kkhu6z5&cid=55505&customerIpAddress=89.140.177.130&customerUserAgent=Mozilla/5.0&locale=en_US&currencyCode=USD&hotelId='+str(hotel.hotelID )+'&arrivalDate=3/'+str(i)+'/2015&departureDate=3/'+str(i+1)+'/2015&includeDetails=true&includeRoomImages=false&room1=2'

        r = rq.get(url) # Replace the id if not found.
        room = json.loads(r.text)
        room = room["HotelRoomAvailabilityResponse"]
        #print(json.dumps(room, indent=2))

        h = Hotel()
        r = Room()
        try:
            r.hotelId = hotel #This is a reference field that references the hotel document for this loop
            r.name = room["hotelName"]
            r.arrival = room["arrivalDate"]
            r.departure = room["departureDate"]
            r.cancelPol = room["HotelRoomResponse"][1]["RateInfos"]["RateInfo"]["cancellationPolicy"]
            r.rate = room["HotelRoomResponse"][1]["RateInfos"]["RateInfo"]["ChargeableRateInfo"]
            r.rateDescrip = room["HotelRoomResponse"][1]["rateDescription"]
            r.occupancy = room["HotelRoomResponse"][1]["quotedOccupancy"]
            r.beds = room["HotelRoomResponse"][1]["BedTypes"]
            r.typeCode = str(room["HotelRoomResponse"][1]["roomTypeCode"])
            r.propertyId = str(room["HotelRoomResponse"][1]["propertyId"])
            r.valueAdds = room["HotelRoomResponse"][1]["ValueAdds"]
            r.save()


            print(r.arrival)

        except Exception:
            print("SOLD OUT") #When there is an exception its because the hotel is sold out
            #print(json.dumps(room, indent=2))
disconnect()