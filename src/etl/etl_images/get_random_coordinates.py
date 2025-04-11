import random
import math
from geopy.distance import distance

# Generate a random point inside Area Madrid
def generate_random_coordinates(lat, lon, radius):
    # Random bearing (0 to 360 degrees)
    bearing = random.uniform(0, 360)
    # Random distance (with square root to ensure uniform distribution)
    dist = math.sqrt(random.random()) * radius
    # Calculate new coordinates
    d = distance(meters=dist)
    coordinates = d.destination(point=(lat, lon), bearing=bearing)
    return (coordinates.latitude, coordinates.longitude)