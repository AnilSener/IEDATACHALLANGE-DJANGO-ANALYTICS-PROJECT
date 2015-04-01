
import re
import html5lib
import lxml
import urllib.request as urllib
from bs4 import BeautifulSoup
from hotelapp.models import TAHotel,HotelReview,TAUser
import configparser
config = configparser.ConfigParser()
config.read('../../app.conf')
from mongoengine.connection import connect,disconnect
connection=connect(config["MONGODB"]["DB_NAME"])
from hotelapp.util import geo
from googlegeocoder import GoogleGeocoder
from hotelapp.rest.TAusers import addUser
pages = ['http://www.tripadvisor.com/Hotels-g187453-Basque_Country-Hotels.html']
for i in range(30,210,30):
    pages.append('http://www.tripadvisor.com/Hotels-g187453-oa'+str(i)+'-Basque_Country-Hotels.html#TtD')
print(len(pages))
opener = urllib.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0')]  #Opens the page as Mozilla instead of Python

links=[]
for page in pages:
    sourceCode = opener.open(page).read() #The page of attractions
    soup = BeautifulSoup(sourceCode, "html5lib")            #Parses the HTML
    for anchor in soup.findAll('a', href=True): #Find all links to attractions in page of attractions
        if "#REVIEWS" in str(anchor['href']):
            links.append(anchor['href'])
            sourceCode = opener.open('http://www.tripadvisor.com'+anchor['href']).read()
            soup2 = BeautifulSoup(sourceCode)
            review = soup2.find('span', {"property": "v:count"}).text
            print(review)
            reviewCount = int(review.replace(',',''))
            pagesCount = int(reviewCount/10) * 10
            for p in range(10,pagesCount,10):
                t = anchor['href'].find('Reviews-')
                links.append(anchor['href'][0:t+7]+'-'+'or'+str(p)+'-'+anchor['href'][t+8:])

for link in links:
    linkSource = opener.open('http://www.tripadvisor.com'+str(link)).read()
    soup3 = BeautifulSoup(linkSource, "lxml")
    reviews = soup3.findAll('p', {"class", "partial_entry"})
    helpfuls = soup3.findAll('div', {"class", "helpful"})
    adjhelpfuls=[]
    for help in helpfuls:
        adjhelpfuls.append(help.get("id")[help.get("id").index("q")+1:help.get("id").index("_")])
    #print(adjhelpfuls)
    adjresponses=[]
    for help in adjhelpfuls:
        response = soup3.find(id="response_"+str(help))
        if (response!=None):
            adjresponses.append(response)
    #print(adjresponses)
    adjreviews=[]
    for review in reviews:
        isresponse=False
        for response in adjresponses:
            #print("#####REVIEW####")
            #print(review.text)
            #print("#####RESPONSE####")
            #print(response.text)
            if review.text.strip()[:10]==response.text.strip()[:10]:
                isresponse=True
                break;
        print(str(isresponse))
        if not isresponse:
            adjreviews.append(review)
    """adjreviews=[]
    for review in reviews:
        if "partnerRvw" in review:
            print("not normal")
            print(review)
            continue;
        else:
            print(review)
            adjreviews.append(review)"""
    #ratings = re.findall(b'<img class="sprite-rating_s_fill.+alt="(.+)">', linkSource)[-16:-6]
    ratings = soup3.findAll('img', {"class", "sprite-rating_s_fill"})[6:16]
    location_name = soup3.findAll('h1', {"class", "header"})[0].text
    users = re.findall(b'<span.+user.+>(.+)</span>',linkSource)
    #cities = soup3.findAll('div', {"class": "location"})
    address = soup3.findAll('span', {"class", "format_address"})[0].text
    quotes = soup3.findAll('span', {"class", "noQuotes"})
    mc=re.findall(b'<div class="mapContainer" data-lat="(.+)"', linkSource)
    mapcontainer= []
    if len(mc)>0:
        mapcontainer= mc[0]
        html = BeautifulSoup('<div class="mapContainer" data-lat="'+str(mapcontainer)[2:]+'data-lng="'+str(mapcontainer)[str(mapcontainer).index("-")+4:]+'">')
        mapcontainer= html.findAll("div",{"class", "mapContainer"})
    print(mapcontainer)
    ranks = soup3.findAll('b', {"class", "rank_text"})
    qs=TAHotel.objects.filter(hotelName=location_name)
    h = TAHotel()
    if len(qs[:])>0:
        h=qs[:1].get()
    else:
        h.hotelName = location_name #Because the format of the variables is byte, they must be converted to strings or ints/floats
        #h.city = str(city)
        h.address = str(address)
        h.geometry=None
        if len(mapcontainer)>0:
            print("Trial")
            h.geometry=[float(mapcontainer[0].get('data-lng')),float(mapcontainer[0].get('data-lat'))]
        else:
            try:
                geolocator = GoogleGeocoder()
                geolocation=None
                for coords in geolocator.get(h.address):
                    if(geo.checkCoordinate(coords.geometry.location.lng,coords.geometry.location.lat)):
                        geolocation =coords
                print("Google")
                print(geolocation.geometry.location.lng)
                h.geometry=[geolocation.geometry.location.lng,geolocation.geometry.location.lat]
            except Exception:
                print(h.address+"Address cannot be located")
        print(h.geometry)
        h.save()
    for review, rating, user, quote in zip(adjreviews, ratings, users, quotes):
        r = HotelReview()
        r.review = str(review.text)
        #r.rating = int(str(rating)[2])
        r.rating = int(rating.get("alt")[0:rating.get("alt").index(" ")])
        r.reviewLocation =h
        r.title = str(quote.text)
        u=addUser(str(user)[2:-1])
        r.user=u
        print("User recorded on review: "+u.name)
        r.save()


print(len(links))

disconnect()