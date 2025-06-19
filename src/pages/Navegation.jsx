import React, { useState, useEffect, useRef } from 'react';
import { Link } from 'react-router-dom';
import { MapContainer, TileLayer, Polyline, Marker, Popup, GeoJSON } from 'react-leaflet';
import L from 'leaflet';

import 'leaflet/dist/leaflet.css';
import './Navegation.css';
import MapLegend from '../components/MapLegend';

// Leaflet icons
import icon from 'leaflet/dist/images/marker-icon.png';
import iconShadow from 'leaflet/dist/images/marker-shadow.png';
let DefaultIcon = L.icon({
  iconUrl: icon,
  shadowUrl: iconShadow,
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41]
});
L.Marker.prototype.options.icon = DefaultIcon;

const LEGEND_ITEMS = [
  { category: "Totalmente accesible", color: "green" },
  { category: "Parcialmente accesible", color: "orange" },
  { category: "Poco accesible", color: "red" },
  { category: "Desconocida", color: "blue" },
];

export const Navegation = () => {
  const [routeData, setRouteData] = useState(null);
  const [loadingMap, setLoadingMap] = useState(true);
  const mapRef = useRef(null);

  useEffect(() => {
    const storedRouteData = localStorage.getItem('routeData');
    if (storedRouteData) {
      const data = JSON.parse(storedRouteData);
      setRouteData(data);
      setLoadingMap(false);

      if (data.global_accessibility_score !== undefined) {
      alert(`Puntuación de accesibilidad de la ruta: ${data.global_accessibility_score}/100`);
    }
    } else {
      console.error("No route data available.");
      setLoadingMap(false);
    }
  }, []);

  const getSegmentColor = (category) => {
    const foundCategory = LEGEND_ITEMS.find(item => item.category === category);
    return foundCategory ? foundCategory.color : "blue";
  };


  if (loadingMap) {
    return (
      <div className="navigation-container">
        <div className="map-loading-overlay">
          <p>Cargando mapa y datos de accesibilidad...</p>
        </div>
      </div>
    );
  }

  if (!routeData || !routeData.decoded_route_points || routeData.decoded_route_points.length === 0) {
    return (
      <div className="navigation-container">
        <p>No se encontraron datos de ruta o la ruta está vacía. Vuelve a la página de inicio para buscar una ruta.</p>
        <Link to="/" className="close-button">Volver al Inicio</Link>
      </div>
    );
  }

  const globalAccessibilityScore = routeData.global_accessibility_score || 0;


  return (
    <div className="navigation-container">
      <Link to="/" className="close-button">
        <span className="material-icons">X</span>
      </Link>
      <div className="map-controls-overlay">
        <button className="map-settings-button">
          <i className="fa-solid fa-gear"></i>
        </button>
      </div>

      {/* Map View */}
      <div className="map-viewer-wrapper">
        <MapContainer
          center={[40.416775, -3.703790]}
          zoom={13}
          style={{ height: '100%', width: '100%' }}
          whenCreated={mapInstance => { mapRef.current = mapInstance }}
        >
          <TileLayer
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          />

          {/* MapLegend component */}
          <MapLegend legendItems={LEGEND_ITEMS} position="bottomright" />

          {/* Draw the main route segments */}
          {routeData.segment_accessibility && routeData.segment_accessibility.map((segment, index) => (
            <Polyline
              key={`segment-${index}`}
              positions={[[segment.start_point.lat, segment.start_point.lng], [segment.end_point.lat, segment.end_point.lng]]}
              color={getSegmentColor(segment.analysis.category)}
              weight={6}
              opacity={0.7}
            >
              <Popup>
                <strong>Segmento {index + 1}:</strong><br />
                Categoría: {segment.analysis.category}<br />
                Ancho medio acera: {segment.analysis.mean_sidewalk_width ? segment.analysis.mean_sidewalk_width.toFixed(2) + 'm' : 'N/A'}<br />
                Avisadores: {segment.analysis.has_buzzers ? 'Sí' : 'No'}<br />
                Obras recientes: {segment.analysis.has_constructions ? 'Sí' : 'No'}
              </Popup>
            </Polyline>
          ))}

          {/* Start and End markers */}
          <Marker position={[routeData.decoded_route_points[0].lat, routeData.decoded_route_points[0].lng]} />
          <Marker position={[routeData.decoded_route_points[routeData.decoded_route_points.length - 1].lat, routeData.decoded_route_points[routeData.decoded_route_points.length - 1].lng]} />

          {routeData.intersected_data?.buzzers && JSON.parse(routeData.intersected_data.buzzers).features && (
            <GeoJSON
              key="buzzers-layer"
              data={JSON.parse(routeData.intersected_data.buzzers)}
              pointToLayer={( _ , latlng) => L.circleMarker(latlng, { radius: 5, color: 'red', fillColor: 'red', fillOpacity: 0.7 })}
              onEachFeature={(feature, layer) => {
                if (feature.properties && feature.properties.NOMBRE) {
                  layer.bindPopup(`<strong>Avisador:</strong> ${feature.properties.NOMBRE}`);
                } else {
                  layer.bindPopup("Avisador");
                }
              }}
            />
          )}
          {routeData.intersected_data?.constructions && JSON.parse(routeData.intersected_data.constructions).features && (
            <GeoJSON
              key="constructions-layer"
              data={JSON.parse(routeData.intersected_data.constructions)}
              style={() => ({ color: 'orange', weight: 3, opacity: 0.5, fillColor: 'orange', fillOpacity: 0.2 })}
              onEachFeature={(feature, layer) => {
                if (feature.properties && feature.properties.NOMBRE) {
                  layer.bindPopup(`<strong>Obra:</strong> ${feature.properties.NOMBRE}`);
                } else {
                  layer.bindPopup("Obra");
                }
              }}
            />
          )}
          {routeData.intersected_data?.sidewalks_on_route && JSON.parse(routeData.intersected_data.sidewalks_on_route).features && (
            <GeoJSON
              key="sidewalks-layer"
              data={JSON.parse(routeData.intersected_data.sidewalks_on_route)}
              style={() => ({ color: 'gray', weight: 2, opacity: 0.5 })}
              onEachFeature={(feature, layer) => {
                if (feature.properties && feature.properties.ANCHO_MEDIO) {
                  layer.bindPopup(`<strong>Ancho medio:</strong> ${feature.properties.ANCHO_MEDIO.toFixed(2)}m`);
                } else {
                  layer.bindPopup("Acera (Ancho no disponible)");
                }
              }}
            />
          )}

        </MapContainer>
      </div>
      <div className="accessibility-info">
        <p>Puntuación de Accesibilidad de la Ruta: <strong>{globalAccessibilityScore}/100</strong></p>
        <p className="accessibility-description">
          {globalAccessibilityScore >= 80 ? 'Esta ruta es altamente accesible.' :
            globalAccessibilityScore >= 50 ? 'Esta ruta es parcialmente accesible con algunas limitaciones.' :
              'Esta ruta presenta desafíos significativos de accesibilidad.'}
        </p>
      </div>
    </div>
  );
};