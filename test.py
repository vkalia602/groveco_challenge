from app import findNearestStore, createBoundaries, searchForLocations, calculateDistance
from geopy.geocoders import Nominatim
import unittest

class TestAppMethods(unittest.TestCase):
    def testFindNearestStore(self):
        expectedNearestStore = [{
        'name': 'Freeport', 
        'location': ('SWC SWC Sunrise Hwy & Buffalo St',), 
        'address': ('248 Sunrise Hwy',), 
        'city': ('Freeport',), 
        'state': ('NY',), 
        'zipcode': ('11520-3943',), 
        'latitude': (40.6555849,), 
        'longitude': (-73.5717874,), 
        'county': 'Nassau County', 
        'distance': 12707.892
        },
        {'name': 'Freeport', 
        'location': ('SWC SWC Sunrise Hwy & Buffalo St',), 
        'address': ('248 Sunrise Hwy',), 
        'city': ('Freeport',), 
        'state': ('NY',), 
        'zipcode': ('11520-3943',), 
        'latitude': (40.6555849,), 
        'longitude': (-73.5717874,), 
        'county': 'Nassau County', 
        'distance': 12707.892
        }]

        address = "248 Sunrise Hwy, Freeport, NY"
        actual = findNearestStore(address)

        self.assertEqual(expectedNearestStore, actual)


    def testCreateBoundaries(self):
        lat = 37.7973773
        lon = -122.3952405
        radius = 25
        
        actual = createBoundaries(lat, lon, radius)
        expected = {37.7973773, -122.67977, 37.57255, 38.02221, -122.11071, -122.3952405}

        self.assertEqual(expected, actual)
    
    def testCalculateDistance(self):
        expected = 12707.447
        storeCoordinates = (40.6510591, -73.8753639)
        addressCoordinates = (-73.59321060764293, -73.29685)
        actual = calculateDistance(storeCoordinates, addressCoordinates)

        self.assertEqual(expected, actual)

    def testSearchForLocations(self):
        '''Sad path to test if no locations found'''
        lat = 37.7973773
        lon = -122.3952405
        radius = 25
        expected = "No stores nearby"
        boundaryBox = createBoundaries(lat, lon, radius)
        actual = searchForLocations(boundaryBox)

        self.assertEqual(expected, actual)


    
if __name__ == '__main__':
    unittest.main()