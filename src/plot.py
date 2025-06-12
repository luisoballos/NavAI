from draw_route import draw_route_and_area_map
import folium
from geopy.geocoders import Nominatim
import webbrowser
import os

def create_folium_layers(route_buffer, buzzers, sidewalks_on_route, constructions, all_sidewalks, crosswalk_locations):
    # ... (la función create_folium_layers se mantiene igual) ...
    route_buffer_layer = folium.GeoJson(
        route_buffer.__geo_interface__,
        style_function=lambda x: {'color': 'blue', 'fillColor': 'blue', 'fillOpacity': 0.5, 'weight': 2},
        name='Route Buffer'
    )

    buzzers_layer = folium.GeoJson(
        buzzers.__geo_interface__,
        marker=folium.Marker(icon=folium.Icon(color='red', icon='info-sign')),
        name='Buzzers',
        tooltip=folium.GeoJsonTooltip(fields=['ID', 'TIPO', 'DISTRITO', 'ANTIGUEDAD'], aliases=['Buzzer ID: ', 'Tipo: ', 'Distrito: ', 'Antiguedad: '])
    )

    sidewalks_layer = folium.GeoJson(
        sidewalks_on_route.__geo_interface__,
        style_function=lambda x: {'color': 'gray', 'fillColor': 'gray', 'fillOpacity': 0.5, 'weight': 2},
        name='Sidewalks on Route',
        tooltip=folium.GeoJsonTooltip(fields=['ANCHO_MEDIO'], aliases=['Ancho Medio (m): '])
    )

    constructions_layer = folium.GeoJson(
        constructions.__geo_interface__,
        style_function=lambda x: {'color': 'orange', 'fillColor': 'orange', 'fillOpacity': 0.5, 'weight': 2},
        name='Constructions on Route',
        tooltip=folium.GeoJsonTooltip(fields=['ROAD_AREA', 'SIDEWALKS_AREA'], aliases=['Road Area (m2): ', 'Sidewalk Area (m2): ']) # Assuming 'descripcion' is a relevant column
    )

    crosswalk_layer = folium.FeatureGroup(name='Crosswalks')
    for lon, lat in crosswalk_locations:
        folium.CircleMarker(location=[lat, lon], radius=5, color='green', fill=True, fill_color='green', fill_opacity=0.7).add_to(crosswalk_layer)

    return route_buffer_layer, buzzers_layer, sidewalks_layer, constructions_layer, crosswalk_layer

def plot_map(route_buffer, buzzers, sidewalks_on_route, constructions, all_sidewalks, crosswalk_locations):
    # Fetch Madrid's coordinates using geopy
    geolocator = Nominatim(user_agent="madrid_locator")
    location = geolocator.geocode("Madrid, Spain")
    madrid_lat = location.latitude
    madrid_lon = location.longitude
    radius_meters = 1000
    zoom = 14

    # Create the Folium map
    route_map = draw_route_and_area_map(None, madrid_lat, madrid_lon, radius_meters, zoom)

    # Create Folium layers
    route_buffer_layer, buzzers_layer, sidewalks_layer, constructions_layer, crosswalk_layer = create_folium_layers(
        route_buffer, buzzers, sidewalks_on_route, constructions, all_sidewalks, crosswalk_locations
    )

    # Add layers to the map
    route_buffer_layer.add_to(route_map)
    buzzers_layer.add_to(route_map)
    sidewalks_layer.add_to(route_map)
    constructions_layer.add_to(route_map)
    crosswalk_layer.add_to(route_map)

    # Add layer control to the map
    folium.LayerControl().add_to(route_map)

    # --- Add JavaScript to get user's current location ---
    # Get the map's unique ID for JavaScript interaction
    map_id = route_map.get_name() # Obtén el ID de forma dinámica

    js_code_content = f"""
    console.log("Script de geolocalización cargado.");
    var map_obj = window['{map_id}']; // Acceder al objeto del mapa usando el ID dinámico

    if (map_obj) {{
        console.log("Objeto del mapa encontrado:", map_obj);
    }} else {{
        console.error("Error: Objeto del mapa con ID '{map_id}' no encontrado en el momento de la carga inicial del script.");
    }}

    function getLocation() {{
        console.log("Intentando obtener la ubicación...");
        if (navigator.geolocation) {{
            navigator.geolocation.getCurrentPosition(showPosition, showError, {{timeout: 10000, enableHighAccuracy: true}});
        }} else {{
            console.log("Geolocation is not supported by this browser.");
            alert("La geolocalización no es compatible con este navegador.");
        }}
    }}

    function showPosition(position) {{
        var lat = position.coords.latitude;
        var lon = position.coords.longitude;
        console.log("Posición actual obtenida: " + lat + ", " + lon);

        // Asegurarse de que map_obj esté disponible, si no, intentarlo de nuevo
        if (!map_obj) {{
            map_obj = window['{map_id}'];
        }}

        if (map_obj) {{
            var userLocationMarker = L.marker([lat, lon]).addTo(map_obj);
            userLocationMarker.bindPopup("<b>Tu ubicación actual</b>").openPopup();
            // map_obj.panTo([lat, lon]); // Opcional: centra el mapa en la ubicación
            console.log("Marcador de ubicación añadido.");
        }} else {{
            console.error("Error: map_obj no está definido al intentar añadir marcador después de obtener ubicación.");
        }}
    }}

    function showError(error) {{
        console.log("Error de geolocalización:", error);
        switch(error.code) {{
            case error.PERMISSION_DENIED:
                console.log("User denied the request for Geolocation.");
                break;
            case error.POSITION_UNAVAILABLE:
                console.log("Location information is unavailable.");
                alert("La información de ubicación no está disponible.");
                break;
            case error.TIMEOUT:
                console.log("The request to get user location timed out.");
                alert("La solicitud para obtener la ubicación del usuario ha excedido el tiempo límite.");
                break;
            case error.UNKNOWN_ERROR:
                console.log("An unknown error occurred.");
                alert("Ha ocurrido un error desconocido.");
                break;
        }}
    }}

    var tryInitializeMap = function() {{
        map_obj = window['{map_id}']; // Intenta obtener el objeto del mapa

        if (map_obj) {{
            console.log("Mapa encontrado. Llamando a getLocation().");
            getLocation();
        }} else {{
            console.log("Mapa aún no inicializado. Reintentando...");
            setTimeout(tryInitializeMap, 500); // Reintenta cada 500ms
        }}
    }};

    // Inicia el proceso de inicialización
    tryInitializeMap();
    """

    # Añadir el contenido JavaScript sin las etiquetas <script>
    route_map.get_root().script.add_child(folium.Element(js_code_content))

    # Define the filename
    filename = "route_map.html"

    # Save the map to the HTML file
    route_map.save(filename)
    print(f"Mapa guardado en {filename}")

    # Open the HTML file in the default web browser
    full_path = os.path.abspath(filename)
    webbrowser.open("file://" + full_path)