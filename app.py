#!/usr/bin/env python3
from docopt import docopt
import geocoder
from math import degrees, radians, cos, asin, sin, cos, sqrt, atan2
from geopy.geocoders import Nominatim
from geopy import distance
import csv


def createBoundaries(lat, lon, radius):
    R = 6371 #radius of the earth
    maxLat = round(lat + degrees(radius/R), 5)
    minLat = round(lat - degrees(radius/R), 5)
    maxLon = round(lon + degrees(asin(radius/R) / cos(radians(lat))), 5)
    minLon = round(lon - degrees(asin(radius/R) / cos(radians(lat))), 5)
    return {minLat, maxLat, minLon, maxLon, lat, lon}

def searchForLocations(boundaryBox):
    minLat, minLon, maxLat, maxLon, lat, lon = boundaryBox
    nearbyStores = []
    # loop through the listings of the stores in the db
    for store in getStoresFromDB():
        try:
            #extracting latitude and longitude from the listing
            storeLat = float(store['latitude'][0])
            storeLon = float(store['longitude'][0])
            #checking to see if lon and lat in the range of distance radius
            if (storeLat > minLat) and (storeLat < maxLat) and (storeLon < minLon) and (storeLon > maxLon):
                distance = calculateDistance((storeLat, storeLon), (lat, lon))
                store['distance'] = distance
                nearbyStores.append(store)
        #except errors in data type or values
        except(TypeError, ValueError): 
            continue
    if len(nearbyStores) < 1:
        return "No stores nearby"

    return nearbyStores

def calculateDistance(storeCoordinates, addressCoordinates):
    R = 6373.0
    lat1 = radians(storeCoordinates[0])
    lon1 = radians(storeCoordinates[1])
    lat2 = radians(addressCoordinates[0])
    lon2 = radians(addressCoordinates[1])

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c
    return round(distance, 3)


def getStoresFromDB():
    store = {}
    with open("store-locations.csv") as f:
        for entry in csv.DictReader(f):
            store['name'] = entry['Store Name']
            store['location'] = entry['Store Location'],
            store['address'] = entry['Address'],
            store['city'] = entry['City'],
            store['state'] = entry['State'],
            store['zipcode'] = entry['Zip Code'],
            store['latitude'] = float(entry['Latitude']),
            store['longitude'] = float(entry['Longitude']),
            store['county'] = entry['County']
            yield store

def findNearestStore(address):

    #Library returns the lat and lon of the given address
    geolocator = Nominatim(user_agent="store_locator")
    location = geolocator.geocode(address)

    #Create a bounding box to eliminate obviously far locations in the database
    boundaryBox = createBoundaries(location.latitude, location.longitude, 25)

    #find nearby locations
    nearbyLocations = searchForLocations(boundaryBox)

    #rearrange locations by distance from given address
    return nearbyLocations



if __name__ == '__main__':
    usage = '''
    Find Store
    find_store will locate the nearest store (as the vrow flies) from
    store-locations.csv, print the matching store address, as well as
    the distance to that store.

    Usage:
    find_store --address="<address>"
    find_store --address="<address>" [--units=(mi|km)] [--output=text|json]
    find_store --zip=<zip>
    find_store --zip=<zip> [--units=(mi|km)] [--output=text|json]

    Options:
    --zip=<zip>            Find nearest store to this zip code. If there are multiple best-matches, return the first.
    --address="<address>"  Find nearest store to this address. If there are multiple best-matches, return the first.
    --units=(mi|km)        Display units in miles or kilometers [default: mi]
    --output=(text|json)   Output in human-readable text, or in JSON (e.g. machine-readable) [default: text]

    '''
    args = docopt(usage) 
    if args["--address"]:
        address = args["--address"]
        if args["--units"]:
            units = args["--units"]
        else:
            units = 'km'
        nearbyStores = findNearestStore(address)
        print(nearbyStores)