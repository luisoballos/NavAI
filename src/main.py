import plot
from etl.get_route import get_route
from etl.get_images import get_images
from image_analysis import analyze_image

import os
import json
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from geopy.geocoders import Nominatim
from shapely.geometry import LineString, Point

################
##### Init #####
################
# Import API KEY
with open('API_KEY.txt', 'r') as file:
    API_KEY = file.readline().strip()
    GEMINI_APIKEY = file.readline().strip()

# Set origin and destination coordinates
geolocator_origin = Nominatim(user_agent="origin_locator")
while True:
    try:
        origin_str = input("Por favor, introduce el origen (dirección o coordenadas): ")
        location_origin = geolocator_origin.geocode(origin_str)
        if location_origin:
            ORIGIN = [location_origin.latitude, location_origin.longitude]
            print(f"Origen establecido en: {ORIGIN}")
            break
        else:
            print("No se pudo geocodificar la ubicación de origen. Inténtalo de nuevo.")
    except Exception as e:
        print(f"Ocurrió un error al geocodificar el origen: {e}. Inténtalo de nuevo.")

geolocator_destination = Nominatim(user_agent="dest_locator")
while True:
    try:
        destination_str = input("Y el destino (dirección o coordenadas): ")
        location_destination = geolocator_destination.geocode(destination_str)
        if location_destination:
            DESTINATION = [location_destination.latitude, location_destination.longitude]
            print(f"Destino establecido en: {DESTINATION}")
            break
        else:
            print("No se pudo geocodificar la ubicación de destino. Inténtalo de nuevo.")
    except Exception as e:
        print(f"Ocurrió un error al geocodificar el destino: {e}. Inténtalo de nuevo.")

# ORIGIN = [40.40531937289522, -3.6822997311392442]
# DESTINATION = [40.4151718345378, -3.706590070402009]
TRAVEL_MODE = "WALK"

################
## Load .json ##
################
existing_results = []
if os.path.exists("image_analysis_results.json"):
    with open("image_analysis_results.json", 'r') as f:
        try:
            existing_results = json.load(f)
            print(f"Se cargaron {len(existing_results)} resultados de análisis previos desde 'image_analysis_results.json'")
        except json.JSONDecodeError:
            print(f"El archivo 'image_analysis_results.json' está corrupto o vacío. Se realizará un nuevo análisis.")

################
##### DDBB #####
################
# Import .geojson data
gdf_buzzers = gpd.read_file("data/processed/gdf_buzzers.geojson")
gdf_sidewalks = gpd.read_file("data/processed/gdf_sidewalks.geojson")
gdf_madrid_works = gpd.read_file("data/processed/madrid_accessibility_works_map.geojson")

# Ensure CRS and transform if necessary 
if gdf_buzzers.crs is None: 
    gdf_buzzers.crs = "EPSG:4326" 

if gdf_sidewalks.crs is None: 
    gdf_sidewalks.crs = "EPSG:25830" 
elif gdf_sidewalks.crs != "EPSG:4326":
    gdf_sidewalks = gdf_sidewalks.to_crs(epsg=4326) 

if gdf_madrid_works.crs is None: 
    gdf_madrid_works.crs = "EPSG:25830" 
elif gdf_madrid_works.crs != "EPSG:4326":
    gdf_madrid_works = gdf_madrid_works.to_crs(epsg=4326)

# Convert Timestamp columns to strings
for col in gdf_madrid_works.columns:
    if pd.api.types.is_datetime64_any_dtype(gdf_madrid_works[col]):
        gdf_madrid_works[col] = gdf_madrid_works[col].astype(str)
for col in gdf_buzzers.columns:
    if pd.api.types.is_datetime64_any_dtype(gdf_buzzers[col]):
        gdf_buzzers[col] = gdf_buzzers[col].astype(str)

################
#####Route #####
################
# Create route's geometry object
route = get_route(ORIGIN, DESTINATION, API_KEY, TRAVEL_MODE)
route_coords = [(point['lng'], point['lat']) for point in route]
route_line = LineString(route_coords)

# Create a GeoDataFrame for the route with the correct CRS
route_gdf = gpd.GeoDataFrame([1], geometry=[route_line], crs="EPSG:4326")

##### Intersect #####
# Create buffer around route
buffer_threshold = 0.0001
route_buffer = route_gdf.buffer(buffer_threshold).iloc[0]

# Buzzers on the route
buzzers_ontheroute = gdf_buzzers[gdf_buzzers.intersects(route_buffer)]
print("Buzzers on the route:")
print(buzzers_ontheroute)

#Constructions on the route
constructions_ontheroute = gdf_madrid_works[gdf_madrid_works.intersects(route_buffer)]
print("\nConstructions on the route:")
print(constructions_ontheroute)

#Mean width sidewalks on the route
sidewalk_width_ontheroute = gdf_sidewalks[gdf_sidewalks.intersects(route_buffer)]
print("\nAncho medio de las aceras en la ruta:")
print(sidewalk_width_ontheroute)

################
#####IMAGES#####
################
API_images = get_images(route, API_KEY)

crosswalk_locations = []
new_results = [] # To store results of new analysis
for image_data in API_images:
    found_in_existing = False
    for result in existing_results:
        if result.get('latitude') == image_data['lat'] and result.get('longitude') == image_data['lng']:
            #print(f"Usando resultado previo para: {image_data['url']}")
            if result.get('has_crosswalk'):
                crosswalk_locations.append((result['longitude'], result['latitude']))
            found_in_existing = True
            break

    if not found_in_existing:
        analysis_result = analyze_image(image_data, API_KEY)
        new_results.append(analysis_result.model_dump())
        #print(f"Analizando imagen: {image_data['url']}, Crosswalk detected: {analysis_result.has_crosswalk}")
        if analysis_result.has_crosswalk and analysis_result.latitude is not None and analysis_result.longitude is not None:
            crosswalk_locations.append((analysis_result.longitude, analysis_result.latitude))

# Save the new results along with the existing ones
all_results = existing_results + new_results
with open("image_analysis_results.json", 'w') as f:
    json.dump(all_results, f, indent=4)

print(f"\nImage analysis results saved to: {"image_analysis_results.json"} ({len(all_results)} total)")

################
#Visualizations#
################
plot.plot_map(route_buffer, buzzers_ontheroute, sidewalk_width_ontheroute, constructions_ontheroute, gdf_sidewalks, crosswalk_locations)

##################################
##### Accesibility Evaluation ####
##################################

def evaluate_accessibility(buzzers_ontheroute, crosswalk_locations, sidewalk_width_ontheroute):
    # La puntuación principal se basará en la proporción de pasos peatonales con avisadores
    score = 0

    # Criterio: Porcentaje de pasos peatonales con avisadores acústicos
    crosswalk_points = [Point(lon, lat) for lon, lat in crosswalk_locations]
    gdf_crosswalks = gpd.GeoDataFrame(geometry=crosswalk_points, crs="EPSG:4326")

    num_crosswalks = len(gdf_crosswalks)
    crosswalks_with_buzzers = 0

    if num_crosswalks > 0:
        # Usaremos un buffer pequeño para verificar si hay un buzzer cerca de cada cruce
        # Asumiendo que 0.00005 grados es ~5-7 metros (dependiendo de la latitud)
        # Considera proyectar a un CRS métrico si necesitas más precisión para el buffer
        crosswalk_buffer = gdf_crosswalks.buffer(0.00005) # Pequeño buffer alrededor de cada cruce

        for idx, crosswalk_geom in crosswalk_buffer.iterrows():
            # Verifica si este buffer de cruce intersecta con AL MENOS UN buzzer
            if buzzers_ontheroute.intersects(crosswalk_geom).any():
                crosswalks_with_buzzers += 1
        
        # Calcular el porcentaje
        score = (crosswalks_with_buzzers / num_crosswalks) * 100
        print(f"Pasos peatonales detectados: {num_crosswalks}")
        print(f"Pasos peatonales con avisadores: {crosswalks_with_buzzers}")
        print(f"Criterio (Avisadores en pasos peatonales): {score:.2f}%")
    else:
        # Si no hay pasos peatonales, el criterio de "avisadores en pasos peatonales" se cumple vacuamente.
        # Podríamos darle 100% en este aspecto.
        score = 100
        print("No se detectaron pasos peatonales en la ruta. Criterio de avisadores considerado 100% CUMPLIDO.")

    # Puedes imprimir el ancho medio de la acera para información, pero no se usará para la puntuación actual.
    required_sidewalk_width_meters = 1.5
    if not sidewalk_width_ontheroute.empty:
        mean_sidewalk_width = sidewalk_width_ontheroute['ANCHO_MEDIO'].mean()
        print(f"Ancho medio de las aceras en la ruta: {mean_sidewalk_width:.2f}m (requerido >= {required_sidewalk_width_meters}m)")
    else:
        print("No se encontraron datos de aceras en la ruta.")

    return int(score) # Devuelve la puntuación como un entero

accessibility_score = evaluate_accessibility(buzzers_ontheroute, crosswalk_locations, sidewalk_width_ontheroute)
print(f"\n--- Puntuación de Accesibilidad de la Ruta: {accessibility_score}/100 ---")