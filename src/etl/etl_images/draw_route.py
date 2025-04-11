# Libraries
import folium

# Area and route map
def draw_route_and_area_map(decoded_path, lat, lon, radius, zoom):
    # Create map centered at the start point
    route_map = folium.Map(location=[lat, lon], zoom_start=zoom)

    # Add circle for the area
    folium.Circle(
        radius=radius,
        location=[lat, lon],
        color="blue",
        fill=True,
        fill_opacity=0.2
    ).add_to(route_map)

    # Add polyline route
    folium.PolyLine(
        [(point['lat'], point['lng']) for point in decoded_path],
        color='blue',
        weight=5
    ).add_to(route_map)

    # Add start and end markers
    folium.Marker([decoded_path[0]['lat'], decoded_path[0]['lng']], tooltip='START').add_to(route_map)
    folium.Marker([decoded_path[-1]['lat'], decoded_path[-1]['lng']], tooltip='END').add_to(route_map)

    return route_map