from django.db import models
from mongoengine import *


# Create your models here.
"""class User(Document):
    user_name = StringField(required=True,max_length=50)
    password = StringField(required=True,max_length=50)
    email = StringField(required=True,max_length=50)
    first_name = StringField(required=True,max_length=50)
    last_name = StringField(required=True,max_length=50)
"""

class Tweet(Document):
    geometry = PolygonField()
    geopoint = GeoPointField()
    placeId = StringField()
    placeFullName = StringField()
    placeName = StringField()
    countryCode = StringField()
    placeType = StringField()
    language = StringField()
    text = StringField()
    createdAt = DateTimeField()
    retweetCount = LongField()
    favoriteCount = LongField()
    trends = ListField()
    hashtags = ListField()
    symbols = ListField()
    urls = ListField()
    twitteruser = ReferenceField("TwitterUser")

class TwitterUser(Document):
    userID = StringField()
    userName = StringField()
    #tweetObjIDs = ListField()
    retweetCount = LongField()
    friendsCount = LongField()
    followersCount = LongField()
    isGeoEnabled = BooleanField
    language = StringField()
    def gettweetObjIDs(self):
        return self.tweetObjIDs
#ross = User(user_name='anilsener@student.ie.edu',password='anilsener',email='ross@example.com', first_name='Ross', last_name='Lawley').save()


#Misael
"""
class Hotel(Document):
    name = StringField()
    geopoint = GeoPointField()
    address1 = StringField()
    highRate = IntField()
    hotelID = IntField()
    deepLink = URLField()
    lowRate = IntField()
    address2 = StringField()
    shortDescription = StringField()
    proximityDistance = IntField()
    propertyCategory = IntField()
    highRate = IntField()
    hotelRating = IntField()
    TripAdvisorRating = IntField()
    city = StringField()
    confidenceRating = IntField()
    locationDescription = StringField()
    numberOfRooms = IntField()
    @property
    def popupContent(self):
      return '<images src="{}" /><p><{}</p>'.format(
          self.name,
          self.shortDescription,
          self.address1)
    meta = {
        'indexes': [[("geopoint", "2dsphere")],[("hotelID",1)]]
    }
    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Hotels in Biscaya"
"""
#Misael
class HotelProperty(EmbeddedDocument):
    name = StringField()
    address1 = StringField()
    highRate = IntField()
    deepLink = URLField()
    lowRate = IntField()
    address2 = StringField()
    shortDescription = StringField()
    proximityDistance = IntField()
    propertyCategory = IntField()
    hotelRating = IntField()
    TripAdvisorRating = IntField()
    city = StringField()
    confidenceRating = IntField()
    locationDescription = StringField()
    numberOfRooms = IntField()
    clusterCounts = ListField(IntField())
    clusterAverages = ListField(FloatField())
    @property
    def popupContent(self):
      return '<images src="{}" /><p><{}</p>'.format(
          self.name,
          self.shortDescription,
          self.address1)

class Hotel(Document):
    hotelID = IntField()
    type = StringField()
    geometry = PointField(auto_index=True)
    properties= EmbeddedDocumentField('HotelProperty')

    meta = {
        'indexes': [[("hotelID",1)]]
    }

    class Meta:
        verbose_name_plural = "Hotels"


"""class Attraction(Document):
    locationName = StringField()
    user = StringField()
    city = StringField()
    address = StringField()
    rank = IntField()
    type = StringField()
    activity = StringField()
    geopoint = GeoPointField()"""

class AttractionProperty(EmbeddedDocument):
    locationName = StringField()
    user = StringField()
    city = StringField()
    address = StringField()
    rank = IntField()
    type = ListField(StringField())
    activity = ListField(StringField())


class Attraction(Document):
    attractionID = IntField()
    type = StringField()
    geometry = PointField(auto_index=True)
    properties= EmbeddedDocumentField('AttractionProperty')
    class Meta:
        verbose_name_plural = "Attractions"

class TAUser(Document):
    _id = ObjectIdField()
    name = StringField()
    gender = StringField()
    age_interval = StringField()
    home = StringField()
    travelStyle = ListField(StringField())
    visited = ListField(StringField())

class Review(Document):
    _id = ObjectIdField()
    review = StringField()
    rating = FloatField()
    reviewLocation = ReferenceField("Attraction")
    user = ReferenceField("TAUser")
    #sentiScore = FloatField()
    title = StringField()


class TAHotel(Document):
    hotelName = StringField()
    city = StringField()
    address = StringField()
    rank = IntField()
    geometry = PointField(auto_index=True)
    clusters = ListField()

class HotelReview(Document):
    _id = ObjectIdField()
    review = StringField()
    rating = FloatField()
    user = ReferenceField(TAUser)
    reviewLocation = ReferenceField(TAHotel)
    #sentiScore = FloatField()
    title = StringField()


class HotelSentiment(Document):
    _id = ObjectIdField()
    reviewID = ReferenceField(HotelReview)
    type = StringField()
    seq_no = IntField()
    word = StringField()
    lemma_word = StringField()
    pos_tag = StringField()
    pos_senti_score = FloatField()
    neg_senti_score = FloatField()
    obj_senti_score = FloatField()

class AttractionSentiment(Document):
    _id = ObjectIdField()
    reviewID = ReferenceField(Review)
    type = StringField()
    seq_no = IntField()
    word = StringField()
    lemma_word = StringField()
    pos_tag = StringField()
    pos_senti_score = FloatField()
    neg_senti_score = FloatField()
    obj_senti_score = FloatField()



import math
class BoundingBox(object):
    def __init__(self, *args, **kwargs):
        self.lat_min = None
        self.lon_min = None
        self.lat_max = None
        self.lon_max = None

    def get_Max_Radius(self):

        assert self.lat_min >= -90.0 and self.lat_min  <= 90.0 and self.lat_max >= -90.0 and self.lat_max  <= 90.0
        assert self.lon_min >= -180.0 and self.lon_min  <= 180.0 and self.lon_max >= -180.0 and self.lon_max  <= 180.0

        R = 6373.0

        lat1 = math.radians(self.lat_min)
        lon1 = math.radians(self.lon_min)
        lat2 = math.radians(self.lat_max)
        lon2 = math.radians(self.lon_max)

        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = (math.sin(dlat/2))**2 + math.cos(lat1) * math.cos(lat2) * (math.sin(dlon/2))**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        distance = R * c
        radius=distance/2
        return radius
    def get_Center(self):
        return [(self.lon_min+self.lon_max)/2,(self.lat_min+self.lat_max)/2]

class Property(EmbeddedDocument):
    WKT = StringField()
    cell_id = LongField()
    field_2 = LongField()
    field_3 = DecimalField(precision=15,force_string=True)
    field_4 = DecimalField(precision=15,force_string=True)
    field_5 = DecimalField(precision=15,force_string=True)
    field_6 = DecimalField(precision=15,force_string=True)
    field_7 = DecimalField(precision=15,force_string=True)
    field_9 = StringField()
    date = StringField()
    hour = IntField()
    n_people = DecimalField(precision=2)


class TelefonicaMap(Document):
    type = StringField()
    properties= EmbeddedDocumentField('Property')
    featureID = LongField()
    geometry = PolygonField()
    """meta = {
        'allow_inheritence':True,'_cls' : 'MapItem.TelefonicaMap',
    '_types' : ['MapItem']
    }"""
    """class Meta:
        db_table='telefonica_map'"""
class TelefonicaPopulation(Document):
    cell_id = LongField()
    date = StringField()
    hour = IntField()
    n_people = DecimalField(precision=2)
    """meta = {
        'allow_inheritence':True,'_cls' : 'MapItem.TelefonicaPopulation',
    '_types' : ['MapItem']
    }"""
    """class Meta:
        db_table='telefonica_population'"""
#Querying embedded document field
#print(TelefonicaMap.objects(properties__cell_id=42242442323224).get())
#print(MapItem.objects(properties__cell_id=42242442323224).get().type)
#mapobj=TelefonicaMap.objects(properties__cell_id=42242442323224).get()
#popobj=TelefonicaPopulation.objects(cell_id=42242442323224).all()
#print(popobj)
#print(mapobj.type)
"""connection=(

)
TelefonicaMap.query.join()"""


class MapItem(Document):
    type = StringField()
    properties= EmbeddedDocumentField('Property')
    featureID = LongField()
    geometry = PolygonField()
    class Meta:
        verbose_name_plural = "Population"
"""
from djgeojson.fields import PointField
from django.db import models

class MushroomSpot(models.Model):
    geom = PointField()
    description = models.TextField()
    picture = models.ImageField()

    @property
    def popupContent(self):
      return '<images src="{}" /><p><{}</p>'.format(
          self.picture.url,
          self.description)"""

class Room(Document):
        name = StringField()
        arrival = DateTimeField()
        departure = DateTimeField()
        cancelPol = StringField()
        rate = DictField()
        rateDescrip = StringField()
        occupancy = IntField()
        beds = DictField()
        typeCode = StringField()
        propertyId = StringField()
        valueAdds = DictField()
        hotelId = ReferenceField("Hotel")

class bbvaEstablishment(Document):
    type = StringField()
    sector = StringField()
    date = DateTimeField()
    geometry = PointField(auto_index=True)
    clientZip = StringField()
    merchants = IntField()
    cards = IntField()
    transactions = IntField()
    average = FloatField()
    max= FloatField()
    min = FloatField()
    sd= FloatField()

class Hotelattractionedge(Document):
    type = StringField()
    hotelID = StringField()
    attractionID = StringField()
    hotelName = StringField()
    attractionName = StringField()
    userCount = IntField()

class Cluster(Document):
    cluster = StringField()
    attractions = ListField(StringField())
    types = ListField(StringField())

class HotelSentimentResults(Document):
    hotelID = IntField()
    roomScore = FloatField()
    foodScore = FloatField()
    staffScore = FloatField()

import django_tables2 as tables

class HotelTopicsTable(tables.Table):
    hotelID = IntField()
    roomScore = FloatField()
    foodScore = FloatField()
    staffScore = FloatField()
