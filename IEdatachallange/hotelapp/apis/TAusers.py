__author__ = 'root'

import re
from pymongo import Connection
import html5lib
from hotelapp.models import TAUser, HotelReview, Review
import urllib.request as urllib
from bs4 import BeautifulSoup
import configparser
config = configparser.ConfigParser()
config.read('../../app.conf')
from mongoengine.connection import connect,disconnect
connection=connect(config["MONGODB"]["DB_NAME"])

users = []
for review in Review.objects:
    users.append(str(review.user))

for hotelreview in HotelReview.objects:
    users.append(str(hotelreview.user))




def addUser(user):
    config = configparser.ConfigParser()
    config.read('../../app.conf')
    connection=connect(config["MONGODB"]["DB_NAME"])
    qs=TAUser.objects.filter(name=user)
    failed = []
    if len(qs[:])>0:
        u=qs[:1].get()
        u.save()
        print("User found in DB"+u.name)
        return u
    else:
        opener = urllib.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/4.0')] #Opens the page as Mozilla instead of Python
        try:
            linkSource = opener.open('http://www.tripadvisor.com/members/'+user).read()
            soup3 = BeautifulSoup(linkSource)
            aboutMe = soup3.findAll("div", {"class": "aboutMe profileBox"})[0].text
            if 'female' in aboutMe:
                gender = 'female'
            elif 'male' in aboutMe:
                gender = 'male'
            if  'Lives in' in aboutMe:
                home = aboutMe[aboutMe.index("Lives in ")+8:aboutMe.index(",")].strip()
            else:
                home = ''
            if "year" in aboutMe:
                age_interval = aboutMe[aboutMe.index("-")-2:aboutMe.index("year")].strip()
            else:
                age_interval = ''
            travelStyle = soup3.findAll('div', {"class": "tagBubble unclickable"})
            print(travelStyle)
            style = []
            for i in travelStyle:
                style.append(i.text)
            placesVisited = soup3.findAll('div', {"class": "cityName"})
            print(placesVisited)
            visited = []
            for i in placesVisited:
                visited.append(i.text)



            u = TAUser()
            u.name = user
            u.gender = gender
            u.age_interval=age_interval
            u.home=home
            #u.travelStyle = str(style)
            u.travelStyle = [s for s in style]
            #u.visited = str(visited)
            u.visited = [v for v in visited]
            u.save()
            print('user saved well as '+u.name)
            return u
        except Exception:
            u = TAUser()
            u.name = user
            u.save()
            print('user saved by name')
            failed.append(user)
            return u

        print(failed)

for user in users:
    addUser(user)

disconnect()