from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import pandas as pd
import geopandas as gpd
from geopy.geocoders import Nominatim
from shapely.geometry import LineString

# Project-specific imports
from etl.get_route import get_route
from etl.get_images import get_images
from image_analysis import analyze_image

app = Flask(__name__)
CORS(app)

################
##### Init #####
################
# Load Google API key
API_KEY = None
try:
    with open('API_KEY.txt', 'r') as file:
        API_KEY = file.readline().strip()
except FileNotFoundError:
    print("Error: API_KEY.txt not found.")
    API_KEY = os.environ.get("GOOGLE_API_KEY")

if API_KEY is None:
    print("WARNING: Google API Key not loaded.")

################
##### DDBB #####
################
# Load GeoDataFrames
try:
    gdf_buzzers = gpd.read_file("data/processed/gdf_buzzers.geojson")
    if gdf_buzzers.crs is None:
        gdf_buzzers.crs = "EPSG:4326"
    for col in gdf_buzzers.columns:
        if pd.api.types.is_datetime64_any_dtype(gdf_buzzers[col]):
            gdf_buzzers[col] = gdf_buzzers[col].astype(str)

    gdf_sidewalks = gpd.read_file("data/processed/gdf_sidewalks.geojson")
    if gdf_sidewalks.crs is None:
        gdf_sidewalks.crs = "EPSG:25830"
    elif gdf_sidewalks.crs != "EPSG:4326":
        gdf_sidewalks = gdf_sidewalks.to_crs(epsg=4326)
    for col in gdf_sidewalks.columns:
        if pd.api.types.is_datetime64_any_dtype(gdf_sidewalks[col]):
            gdf_sidewalks[col] = gdf_sidewalks[col].astype(str)

    gdf_madrid_works = gpd.read_file("data/processed/madrid_accessibility_works_map.geojson")
    if gdf_madrid_works.crs is None:
        gdf_madrid_works.crs = "EPSG:25830"
    elif gdf_madrid_works.crs != "EPSG:4326":
        gdf_madrid_works = gdf_madrid_works.to_crs(epsg=4326)
    for col in gdf_madrid_works.columns:
        if pd.api.types.is_datetime64_any_dtype(gdf_madrid_works[col]):
            gdf_madrid_works[col] = gdf_madrid_works[col].astype(str)

except Exception as e:
    print(f"Error loading GeoDataFrames: {e}. Some functionality may be impaired.")
    gdf_buzzers = gpd.GeoDataFrame(geometry=[])
    gdf_sidewalks = gpd.GeoDataFrame(geometry=[])
    gdf_madrid_works = gpd.GeoDataFrame(geometry=[])

def analyze_segment_accessibility(segment_line: LineString, buffer_threshold=0.0001):
    """
    Performs an accessibility analysis for a given route segment,
    categorizing it based on sidewalk width, finished accessibility works, and buzzers.
    """
    segment_buffer = segment_line.buffer(buffer_threshold)

    # Init
    category = "Desconocida"
    mean_sidewalk_width = 0.0

    # Calculate mean sidewalk width
    sidewalks_intersect = gdf_sidewalks[gdf_sidewalks.intersects(segment_buffer)]
    if not sidewalks_intersect.empty and 'ANCHO_MEDIO' in sidewalks_intersect.columns:
        mean_sidewalk_width = sidewalks_intersect['ANCHO_MEDIO'].mean()
        # mean_sidewalk_width = round(sidewalks_intersect[sidewalk_width_column_name].mean(), 2)
    
    # Determine initial category based on sidewalk width
    CRITICAL_WIDTH_THRESHOLD = 0.9 # 0.8 is mean wheelchair width (subjective value)
    SUBOPTIMAL_WIDTH_THRESHOLD = 1.5 # comfortable passing for two people or wheelchair + pedestrian (subjective value)

    if mean_sidewalk_width <= CRITICAL_WIDTH_THRESHOLD and mean_sidewalk_width > 0:
        category = "Poco accesible"
    elif mean_sidewalk_width <= SUBOPTIMAL_WIDTH_THRESHOLD and mean_sidewalk_width > 0:
        category = "Parcialmente accesible"
    elif mean_sidewalk_width > SUBOPTIMAL_WIDTH_THRESHOLD:
        category = "Totalmente accesible"
    else: # If 0.0 or no data found
        category = "Desconocida"

    # Check for intersection with finished accessibility construction works
    has_finished_works = not gdf_madrid_works[gdf_madrid_works.intersects(segment_buffer)].empty
    # Check for intersection with acoustic buzzers
    has_buzzers = not gdf_buzzers[gdf_buzzers.intersects(segment_buffer)].empty

    # Check for intersections with finished construction works
    # Finished works is strongly positive, unless it is extremely narrow
    if has_finished_works:
        if category == "Parcialmente accesible" or category == "Desconocida":
            category = "Totalmente accesible"
            
    # Buzzers are significantly positive
    elif has_buzzers:
        if category == "Desconocida":
            category = "Poco accesible"
        elif category == "Poco accesible":
            category = "Parcialmente accesible"
        elif category == "Parcialmente accesible":
            category = "Totalmente accesible"

    # Check for segments with no data
    if category == "Desconocida":
        if has_buzzers:
            category = "Poco accesible"


    # Returns accessibility category and calculated mean sidewalk width
    return {
        "category": category,
        "mean_sidewalk_width": mean_sidewalk_width,
        "has_buzzers": has_buzzers,
        "has_constructions": has_finished_works,
    }


# Route API
@app.route('/api/route_analysis', methods=['POST'])
def route_analysis():
    data = request.get_json()
    origin_str = data.get('origin')
    destination_str = data.get('destination')

    if not origin_str or not destination_str:
        return jsonify({"error": "Origin and destination are required."}), 400

    if API_KEY is None:
        return jsonify({"error": "API Key not loaded. Cannot process request."}), 500

    # Geocoding origin and destination addresses
    geolocator_origin = Nominatim(user_agent="route_origin_locator")
    location_origin = geolocator_origin.geocode(origin_str)
    if not location_origin:
        return jsonify({"error": "Could not geocode origin."}), 400
    ORIGIN_COORDS = [location_origin.latitude, location_origin.longitude]

    geolocator_destination = Nominatim(user_agent="route_dest_locator")
    location_destination = geolocator_destination.geocode(destination_str)
    if not location_destination:
        return jsonify({"error": "Could not geocode destination."}), 400
    DESTINATION_COORDS = [location_destination.latitude, location_destination.longitude]

    TRAVEL_MODE = "WALK"

    try:
        # Step 1: Get route from Route API
        google_route_points = get_route(ORIGIN_COORDS, DESTINATION_COORDS, API_KEY, TRAVEL_MODE)
        if not google_route_points:
            return jsonify({"error": "Could not get route from Google."}), 500

        route_coords_tuples = [(p['lng'], p['lat']) for p in google_route_points]
        route_line = LineString(route_coords_tuples)

        # Step 2: Perform segment accessibility analysis
        segment_analysis_results = []
        for i in range(len(google_route_points) - 1):
            segment_coords_from_google = [
                (google_route_points[i]['lng'], google_route_points[i]['lat']),
                (google_route_points[i+1]['lng'], google_route_points[i+1]['lat'])
            ]
            segment_geom = LineString(segment_coords_from_google)
            segment_info = analyze_segment_accessibility(segment_geom)
            segment_analysis_results.append({
                "start_point": google_route_points[i],
                "end_point": google_route_points[i+1],
                "coordinates": [google_route_points[i], google_route_points[i+1]],
                "analysis": segment_info
            })

        # Step 3: Get Street View Images and analyze with Google Gemini API
        image_data_list = get_images(google_route_points, API_KEY) # Uses Google Street View Static API
        crosswalk_detections = []
        if API_KEY:
            for img_data in image_data_list:
                detection_result = analyze_image(img_data, API_KEY) # Uses Google Gemini API
                crosswalk_detections.append(detection_result.model_dump())
        else:
            print("WARNING: API Key not available. Skipping image analysis.")

        # Step 4: Calculate global accessibility score
        num_accessible_segments = sum(1 for s in segment_analysis_results if s['analysis']['category'] == 'Totalmente accesible')
        total_segments = len(segment_analysis_results)
        global_accessibility_score = (num_accessible_segments / total_segments) * 100 if total_segments > 0 else 100

        # Step 5: Convert intersected GeoDataFrames to GeoJSON for frontend display
        buffer_threshold = 0.0001
        route_buffer = route_line.buffer(buffer_threshold)

        buzzers_ontheroute_json = gdf_buzzers[gdf_buzzers.intersects(route_buffer)].to_json()
        constructions_ontheroute_json = gdf_madrid_works[gdf_madrid_works.intersects(route_buffer)].to_json()
        sidewalk_width_ontheroute_json = gdf_sidewalks[gdf_sidewalks.intersects(route_buffer)].to_json()

        return jsonify({
            "decoded_route_points": google_route_points,
            "segment_accessibility": segment_analysis_results,
            "global_accessibility_score": int(global_accessibility_score),
            "intersected_data": {
                "buzzers": buzzers_ontheroute_json,
                "constructions": constructions_ontheroute_json,
                "sidewalks_on_route": sidewalk_width_ontheroute_json,
                "crosswalks_detected_from_images": [d for d in crosswalk_detections if d['has_crosswalk']]
            }
        })

    except Exception as e:
        print(f"Error in /api/route_analysis route: {e}")
        return jsonify({"error": f"An error occurred while processing your request: {e}"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)