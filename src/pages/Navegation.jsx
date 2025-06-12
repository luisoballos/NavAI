import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import './Navegation.css';

export const Navegation = () => {
  const [loadingMap, setLoadingMap] = useState(true);
  const [ accessibilityScore , setAccessibilityScore] = useState(0);

  useEffect(() => {
    const fetchAccessibilityData = async () => {
      try {
        const response = await fetch('/accessibility_score.json');
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        setAccessibilityScore(data.score);
      } catch (error) {
        console.error("Error fetching accessibility score:", error);
        setAccessibilityScore(0);
      } finally {
        setLoadingMap(false);
      }
    };

    fetchAccessibilityData();
  }, []);

  const mapUrl = '/route_map.html';

  return (
    <div className="navigation-container">
      {/* Botón "cerrar" */}
      <Link to="/" className="close-button">
        <span className="material-icons">X</span>
      </Link>
      <div className="map-controls-overlay">
        <button className="map-settings-button">
          <i class="fa-solid fa-gear"></i>
        </button>
      </div>

      <div className="map-viewer-wrapper">
        {loadingMap ? (
          <div className="map-loading-overlay">
            <p>Cargando mapa...</p>
          </div>
        ) : (
          <iframe
            src={mapUrl}
            width="100%"
            height="100%"
            style={{ border: 'none' }}
            title="Mapa de Ruta con Accesibilidad"
          >
            Tu navegador no soporta iframes.
          </iframe>
        )}
      </div>
      <div className="accessibility-info">
        <p>Puntuación de Accesibilidad de la Ruta: <strong>{accessibilityScore}/100</strong></p>
      </div>
    </div>
  );
};