from get_random_coordinates import generate_random_coordinates
from get_route import get_route
from draw_route import draw_route_and_area_map
from get_images import get_images
import webbrowser

from geopy.geocoders import Nominatim
from googlemaps.convert import decode_polyline
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# Initialization
SVS_API = "https://maps.googleapis.com/maps/api/streetview"                 # Street View Static API
ROUTES_API = "https://routes.googleapis.com/directions/v2:computeRoutes"    # Directions API

TRAVEL_MODE = "WALK"

# Import API KEY
API_KEY = open('../API_KEY.txt', 'r').read().strip('\n')

# Fetch Madrid's coordinates using geopy
geolocator = Nominatim(user_agent="madrid_locator")
location = geolocator.geocode("Madrid, Spain")
madrid_lat = location.latitude
madrid_lon = location.longitude
radius_meters = 1000
zoom = 15

# Set origin and destination coordinates
# Generate random coordinates
# ORIGIN = generate_random_coordinates(madrid_lat, madrid_lon, radius_meters)
# DESTINATION = generate_random_coordinates(madrid_lat, madrid_lon, radius_meters)

# Known coordinates
ORIGIN = [40.40531937289522, -3.6822997311392442]
DESTINATION = [40.4151718345378, -3.706590070402009]

# Get route
response = get_route(ORIGIN, DESTINATION)
route = response.json()['routes'][0]
polyline = route['polyline']['encodedPolyline']
decoded_route = decode_polyline(polyline)

# Create and save the map
route_map = draw_route_and_area_map(decoded_route, madrid_lat, madrid_lon, radius_meters, zoom)
route_map.save('madrid_map.html')
# Display the map
webbrowser.open('madrid_map.html')

# Get the Street View images
API_images = get_images(decoded_route, API_KEY, SVS_API)