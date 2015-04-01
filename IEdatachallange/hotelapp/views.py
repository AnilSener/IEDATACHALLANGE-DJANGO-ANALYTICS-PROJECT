
from django.shortcuts import render_to_response,render
from django.conf import settings

# Create your view here.
from django.http import HttpResponse
import templates
# Create your view here.

def login(request):
    return render_to_response("index.html")

from django.contrib.auth import login
from mongoengine.queryset import DoesNotExist
from mongoengine.django.auth import User
from django.core.context_processors import csrf
"""
def login_view(request):
    print(len(request.POST))
    if len(request.POST)==0:
        return render_to_response("index.html")
    else:
        try:
            user = User.objects.get(username=request.POST['username'])
            if user.check_password(request.POST['password']):
                user.backend = 'mongoengine.django.auth.MongoEngineBackend'
                login(request, user)
                request.session.set_expiry(60 * 60 * 1) # 1 hour timeout
                return render(request,'/main/')
                #return HttpResponse(user)
            else:
                return HttpResponse('login failed')
        except DoesNotExist:
            return HttpResponse('user does not exist')
        except Exception:
            return HttpResponse('unknown error')
"""
from django.http import HttpResponse, HttpResponseRedirect,HttpResponsePermanentRedirect
from django.shortcuts import render_to_response, redirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.template import RequestContext
from hotelapp.forms import LoginForm
from django.contrib.auth import authenticate, login, logout
from mongoengine.django.auth import User
from django.conf import settings


def login_view( request ):
    # Login form submitted
    print(request.user.is_authenticated())

    if request.method == 'POST':
        error_msg = ''
        user=authenticate(username=request.POST['username'],password=request.POST['password'])
        try:
            #user = User.objects.get(username=request.POST['username'] )

            if user is not None and user.is_active:
                user.backend = 'mongoengine.django.auth.MongoEngineBackend'
                login(request, user )
                print("login successful")
                print("Authentication")
                print(request.user.is_authenticated())
                #return HttpResponseRedirect(reverse('login_success'))
                print(reverse('main'))
                #setting NH collection Villa de BilBao
                request.session['hotelID'] =  204269
                return main(request)
            else:
                print("login failed")
                print("pass: "+str(user.check_password(request.POST['password'])))
                print("active?: "+str(user.is_active))
                return _fail_login(request, 'invalid login' )
        except User.DoesNotExist:
            print("user doesn't exist")
            return _fail_login(request, 'invalid login' )
        form = LoginForm()
        return render_to_response('index.html',  context_instance=RequestContext(request) )

    # Login form needs rendering

    else:
        form = LoginForm()
        return render_to_response( 'index.html',context_instance=RequestContext(request) )

def _fail_login( request, msg ):
    messages.add_message( request, messages.ERROR, msg )
    return HttpResponseRedirect(reverse('login'))

def user_show( request ):
    username = request.user.username
    return render_to_response('map.html',
                               locals(),
                               context_instance=RequestContext(request))


from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your view here.
from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.core.urlresolvers import reverse




import json
from hotelapp.models import MapItem

from hotelapp.django.mongoserialize import MongoAwareEncoder

def get_Geojson(date,hour):
    jsonfile=MapItem.objects().filter(properties__date=date,properties__hour=hour).all().to_json()
    jsonString=json.loads(jsonfile)
    my_layer = {
    "type": "FeatureCollection",
    "features": jsonString,
    "crs": {
        "type": "link",
        "properties": {"href": "http://spatialreference.org/ref/epsg/4326", "type": "proj4"} }}

    return json.dumps(my_layer, cls=MongoAwareEncoder, ensure_ascii=False)

import configparser
config = configparser.ConfigParser()
config.read('../app.conf')
from hotelapp.models import BoundingBox,Hotel
from hotelapp.forms import testFormBootstrap3
import datetime
import pytz
#@login_required
def main(request,content={}):
    print(request.session['hotelID'])

    #bbox = json.dumps(TelMap.extent())
    #mapgeo=get_Geojson('2014-01-01',22)
    populationjson=None
    if(len(content)>0):
        populationjson=content["populationjson"]
        raw=content["date"].replace("-","")
        pophour=content["hour"]
    else:
        raw=datetime.datetime.now(pytz.timezone('Europe/Madrid')).strftime("%Y%m%d%H%M%S")
        pophour=datetime.datetime.now(pytz.timezone('Europe/Madrid')).strftime("%H")
    if request.is_ajax():

        return HttpResponse(populationjson, mimetype='application/json')
    else:

        if request.GET.get('id',None):
            form = testFormBootstrap3(instance=testFormBootstrap3.objects.get(id=request.GET.get('id',None)))
        else:
            form = testFormBootstrap3()
        print(raw)
        popyear=str(raw)[0:4]
        popmonth=str(raw)[4:6]
        popday=str(raw)[6:8]
        #I am just passing a hotelId for the demo
        userHotel=getUserHotel(request.session['hotelID'])

        #########
        userHotelJson=json.dumps(userHotel, cls=MongoAwareEncoder, ensure_ascii=False)

        return render_to_response('map.html',{"populationjson":populationjson,'userHotelJson':userHotelJson,'popyear':popyear,'popmonth':popmonth,'popday':popday,'pophour':pophour,'form': form,'bootstrap':3}, context_instance=RequestContext(request))

import pymongo
from django.http import JsonResponse
def getHotel(request):
    client = pymongo.MongoClient('localhost', 27017)
    db = client['hotelapp']
    collection = db['hotel']
    box = [[-3.4492757,42.9818774], [-2.4128145,43.4568551]]
    cursor=collection.find({"type": "Feature","geometry.coordinates": {"$geoWithin": {"$box": box}}})

    features=[]
    for feature in cursor:
        features.append(feature)

    my_layer = {
    "type": "FeatureCollection",
    "features": features,
    "crs": {
        "type": "link",
        "properties": {"href": "http://spatialreference.org/ref/epsg/4326", "type": "proj4"}}}
    hoteljson=json.dumps(my_layer, cls=MongoAwareEncoder, ensure_ascii=False)
    return JsonResponse(hoteljson, safe=False)

def getAttraction(request):
    client = pymongo.MongoClient('localhost', 27017)
    db = client['hotelapp']
    collection = db['attraction']
    box = [[-3.4492757,42.9818774], [-2.4128145,43.4568551]]
    cursor=collection.find({"type": "Feature","geometry.coordinates": {"$geoWithin": {"$box": box}}})



    features=[]
    for feature in cursor:
        features.append(feature)



    my_layer = {
    "type": "FeatureCollection",
    "features": features,
    "crs": {
        "type": "link",
        "properties": {"href": "http://spatialreference.org/ref/epsg/4326", "type": "proj4"}}}

    attractionjson=json.dumps(my_layer, cls=MongoAwareEncoder, ensure_ascii=False)
    return JsonResponse(attractionjson, safe=False)

from django.template import Template
def getPopulation(request):
    if request.method == 'POST':
        datetime=request.POST['date_time']
        print(str(datetime))
        date=datetime[:datetime.index(' ')]
        print(date)

        hour=int(datetime[datetime.index(' ')+1:datetime.index(':')])
        print(hour)

        client = pymongo.MongoClient('localhost', 27017)
        db = client['hotelapp']
        collection = db['map_item']
        cursor=collection.find({"type": "Feature","properties.date": date,"properties.hour":hour })
        features=[]
        for feature in cursor:
            features.append(feature)
        my_layer = {
        "type": "FeatureCollection",
        "features": features,
        "crs": {
            "type": "link",
            "properties": {"href": "http://spatialreference.org/ref/epsg/4326", "type": "proj4"} }}

        populationjson=json.dumps(my_layer, cls=MongoAwareEncoder, ensure_ascii=False)
        return main(request,content={"populationjson":populationjson,"date":date,"hour":hour})

def dateTimeViewBootstrap3(request):
    if request.method == 'POST': # If the form has been submitted...
        form = testFormBootstrap3(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            return render(request, 'map.html', {'form': form,'bootstrap':3})
    else:
        if request.GET.get('id',None):
            form = testFormBootstrap3(instance=testFormBootstrap3.objects.get(id=request.GET.get('id',None)))
        else:
            form = testFormBootstrap3()
        return render(request, 'map.html', {'form': form,'bootstrap':3})


from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_mongoengine.serializers import DocumentSerializer
from hotelapp.models import Hotel

class HotelSerializer(DocumentSerializer):
    class Meta:
        model = Hotel
        fields = ('id',  'name', 'geopoint','city')

@api_view(['GET'])
def get_hotels(request):
    result = Hotel.objects.all()

    data = HotelSerializer(result,many=True)
    print(data)
    return Response(data, status=status.HTTP_200_OK, content_type='application/json')


from hotelapp.models import Hotelattractionedge
def getGraphEdges(request):
    client = pymongo.MongoClient('localhost', 27017)
    db = client['hotelapp']
    collection = db['Hotelattractionedge']
    cursor=collection.find({"type": "Feature"})
    features=[]
    for feature in cursor:
        features.append(feature)

    return JsonResponse(json.dumps(features, cls=MongoAwareEncoder, ensure_ascii=False), safe=False)

def getUserHotel(hotelID):
    client = pymongo.MongoClient('localhost', 27017)
    db = client['hotelapp']
    collection = db['hotel']
    box = [[-3.4492757,42.9818774], [-2.4128145,43.4568551]]
    feature=collection.find_one({"type": "Feature","hotelID":hotelID})
    return feature

from hotelapp.models import HotelSentimentResults
def getHotelSentimentResults(request):
    json= HotelSentimentResults.objects(hotelID=request.session['hotelID']).to_json()
    return JsonResponse(json, safe=False)
