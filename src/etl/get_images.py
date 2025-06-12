# Street View Static API
SVS_API = "https://maps.googleapis.com/maps/api/streetview"

def generate_image_url(coordinates, API_KEY):
    """Generates the URL for the Street View Static API request."""
    params = {
        "size": "640x640",        # Max base size (640x640)
        "scale": 2,               # Doubles resolution to 1280x1280
        "location": coordinates,  # "latitude,longitude"
        "key": API_KEY,
        # Optional adjustments
        "heading": "0",           # 0-360° (compass direction)
        "fov": "120",             # Field of view (1-120°)
        "pitch": "0"              # Up/down angle (-90 to 90)
    }
    # Construct the full URL
    url = f"{SVS_API}?{'&'.join([f'{k}={v}' for k, v in params.items()])}"
    return url

def get_images(route, API_KEY):
    """
    Generates a list of image URLs along the route, along with their coordinates.
    """
    image_data_list = []
    for i in range(len(route)):
        point = route[i]
        lat = point['lat']
        lng = point['lng']
        coordinates = f"{lat},{lng}"
        image_url = generate_image_url(coordinates, API_KEY)

        # Array of metadata of images
        image_data_list.append({'url': image_url, 'lat': lat, 'lng': lng})

    return image_data_list