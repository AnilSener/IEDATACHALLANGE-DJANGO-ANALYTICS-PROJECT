import configparser
config = configparser.ConfigParser()
config.read('../../app.conf')
from hotelapp.models import BoundingBox
box=BoundingBox()
box.lat_min=float(config["GEOLOCATION"]["MIN_LAT"])
box.lat_max=float(config["GEOLOCATION"]["MAX_LAT"])
box.lon_min=float(config["GEOLOCATION"]["MIN_LON"])
box.lon_max=float(config["GEOLOCATION"]["MAX_LON"])

def checkCoordinate(lng,lat):
    return lng>=box.lon_min and lng<=box.lon_max and lat>=box.lat_min and lat<=box.lat_max
