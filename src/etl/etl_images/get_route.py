import requests

def get_route(ORIGIN, DESTINATION, API_KEY, TRAVEL_MODE):
    headers = {
        "X-Goog-Api-Key": API_KEY,
        "X-Goog-FieldMask": "routes.duration,routes.distanceMeters,routes.polyline.encodedPolyline"
    }

    payload = {
        "origin": {
            "location": {
                "latLng": {
                    "latitude": ORIGIN[0],
                    "longitude": ORIGIN[1]
                }
            }
        },
        "destination": {
            "location": {
                "latLng": {
                    "latitude": DESTINATION[0],
                    "longitude": DESTINATION[1]
                }
            }
        },
        "travelMode": TRAVEL_MODE,
        #"routingPreference": "TRAFFIC_UNAWARE",
        "computeAlternativeRoutes": False,
        "routeModifiers": {
            "avoidTolls": False,
            "avoidHighways": False,
            "avoidFerries": False
        },
        "languageCode": "en-US",
        "units": "IMPERIAL"
    }

    response = requests.post(ROUTES_API, json=payload, headers=headers)
    return(response)