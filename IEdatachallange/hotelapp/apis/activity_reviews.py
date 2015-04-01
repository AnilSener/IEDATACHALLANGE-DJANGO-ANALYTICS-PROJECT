__author__ = 'root'

import re
import urllib.request as urllib
from bs4 import BeautifulSoup
from hotelapp.models import Attraction, Review,TAUser,AttractionProperty
import configparser
config = configparser.ConfigParser()
config.read('../../app.conf')
from mongoengine.connection import connect,disconnect
connection=connect(config["MONGODB"]["DB_NAME"])
from hotelapp.util import geo
from googlegeocoder import GoogleGeocoder
#import geocoder
from hotelapp.rest.TAusers import addUser

pages = ['http://www.tripadvisor.com/Attractions-g187453-Activities-Basque_Country.html#TtD']
for i in range(30,360,30):
    pages.append('http://www.tripadvisor.com/Attractions-g187453-Activities-oa'+str(i)+'-Basque_Country.html#TtD')


opener = urllib.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/4.0')] #Opens the page as Mozilla instead of Python
links= []
for page in pages:
    sourceCode = opener.open(page).read() #The page of attractions
    soup = BeautifulSoup(sourceCode)            #Parses the HTML
    for anchor in soup.findAll('a', href=True): #Find all links to attractions in page of attractions
        if "#REVIEWS" in str(anchor['href']):
            links.append(anchor['href'])
            sourceCode = opener.open('http://www.tripadvisor.com'+anchor['href']).read()
            soup2 = BeautifulSoup(sourceCode)
            review = soup2.find('a', {"class": "more"})
            print(review)
            reviewCount = int(re.findall(r'<a.+>(.+)</span>', str(review))[0].replace(',',''))
            pagesCount = int(reviewCount/10) * 10
            for p in range(10,pagesCount,10):
                t = anchor['href'].find('Reviews-')
                links.append(anchor['href'][0:t+7]+'-'+'or'+str(p)+'-'+anchor['href'][t+8:])
    checkLoc=None

userList=[]
attcnt=0
for link in links:
    linkSource = opener.open('http://www.tripadvisor.com'+link).read()
    soup3 = BeautifulSoup(linkSource)
    reviews = soup3.findAll('p', {"class", "partial_entry"})[1:11]
    #ratings = re.findall(b'<images class="sprite-rating_s_fill.+alt="(.+)">', linkSource)[1:11]
    ratings = soup3.findAll('img', {"class", "sprite-rating_s_fill"})[1:11]
    location_names = soup3.findAll('h1', {"class", "header"})
    #users = re.findall(b'<span.+user.+>(.+)</span>',linkSource)
    users = soup3.findAll('div', {"class", "username"})
    cities = soup3.findAll('div', {"class", "location"})
    addresses = soup3.findAll('span', {"class", "format_address"})
    mapcontainer=soup3.findAll('div', {"class", "mapContainer"})
    ranks = soup3.findAll('b', {"class", "rank_text"})
    types = soup3.findAll('div', {"class", "detail"})
    activities = re.findall(b'<b>Activities:</b>(.+)',linkSource)
    quotes = soup3.findAll('span', {"class", "noQuotes"})
    print("Review"+str(len(reviews)))
    print("Rating"+str(len(ratings)))
    print("User"+str(len(users)))
    #print(ratings[0].get("alt")[0:ratings[0].get("alt").index(" ")])
    qs=Attraction.objects.filter(properties__locationName=location_names[0].text)

    if len(qs[:])>0:
        a=qs[:1].get()
    else:
        checkLoc=location_names[0].text
        a = Attraction()
        attcnt+=1
        a.attractionID=attcnt
        a.type = "Feature"
        a.geometry=None
        address=addresses[0].text[9:]
        if len(mapcontainer)>0:
            print("Trial")
            a.geometry=[float(mapcontainer[0].get('data-lng')),float(mapcontainer[0].get('data-lat'))]
        else:
            try:
                geolocator = GoogleGeocoder()
                geolocation=None
                for coords in geolocator.get(address):
                    if(geo.checkCoordinate(coords.geometry.location.lng,coords.geometry.location.lat)):
                        geolocation =coords
                print("Google")
                print(geolocation.geometry.location.lng)
                a.geometry=[geolocation.geometry.location.lng,coords.geometry.location.lat]
            except Exception:
                print(address+"Address cannot be located")
        a.save()
        prop = AttractionProperty()
        prop.locationName = location_names[0].text
        if(len(cities)>1):
            prop.city = str(cities[1].text)
        for add in addresses:
            print(add.text)
        prop.address = addresses[0].text[9:]
        prop.rank =None
        if len(ranks)>0:
            prop.rank = int(ranks[0].text[1:])
        prop.activity = []
        if("," in str(activities)[3:-2]):
            prop.activity = [act for act in str(activities)[3:-2].split(",")]
        else:
            prop.activity.append(str(activities)[3:-2])
        prop.url='http://www.tripadvisor.com'+link
        prop.type= []
        if("," in str(types[0].text)):
            prop.type= [t for t in str(types[0].text).split(",")]
        else:
            prop.type.append(str(types[0].text))
        updated = Attraction.objects(attractionID=int(a.attractionID)).update_one(set__properties=prop)
        if not updated:
            Attraction.objects.update_one(push__properties=prop)
    #print(len(zip(reviews, ratings, users)))
    for review, rating, user, quote in zip(reviews, ratings, users, quotes):
        print("try")
        r = Review()
        r.review = str(review.text)
        try:
            r.rating = float(rating.get("alt")[0:rating.get("alt").index(" ")])
        except Exception:
            r.rating = None
        r.reviewLocation=a
        r.title = str(quote.text)
        u=addUser(user.text)
        r.user=u
        print("User recorded on review: "+u.name)
        r.save()



print(len(links))

disconnect()