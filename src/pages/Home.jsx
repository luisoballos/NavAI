import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './Home.css';

export const Home = () => {
  const navigate = useNavigate();
  const [origin, setOrigin] = useState('');
  const [destination, setDestination] = useState('');
  const [impairment, setImpairment] = useState(null); // 'wheelchair' o 'blind'

  const handleSearch = () => {
    // Enviar los datos al backend
    // 1. Llamar a una API en tu backend de Python con origin, destination, impairment.
    // 2. El backend procesaría la ruta, generaría el mapa HTML y la puntuación.
    // 3. El backend devolvería una confirmación o la puntuación.
    // 4. Navegarías a '/loading' y luego a '/navegation'.

    // Para la demo actual, solo simularemos la navegación y el loading.
    console.log("Buscando ruta:", { origin, destination, impairment });
    navigate('/loading'); // Navega a la pantalla de carga
  };

  return (
    <div className="home-container">
      <h1 className="app-title">NavAI</h1>

      <div className="search-section">
        <div className="search-input-group">
          <label htmlFor="origin-search" className="visually-hidden">Set the origin</label>
          <input
            type="text"
            id="origin-search"
            placeholder="Set the origin"
            value={origin}
            onChange={(e) => setOrigin(e.target.value)}
          />
        </div>
        <div className="search-input-group">
          <label htmlFor="destination-search" className="visually-hidden">Set the destination</label>
          <input
            type="text"
            id="destination-search"
            placeholder="Set the destination"
            value={destination}
            onChange={(e) => setDestination(e.target.value)}
          />
        </div>
        {/* Aquí podrías tener un botón de búsqueda que active handleSearch */}
        <button className="search-button" onClick={handleSearch}>Search Route</button>
      </div>

      <div className="impairment-section">
        <h2 className="impairment-title">SELECT YOUR IMPAIRMENT</h2>
        <div className="impairment-options">
          <button
            className={`impairment-button ${impairment === 'wheelchair' ? 'active' : ''}`}
            onClick={() => setImpairment('wheelchair')}
          >
            <img src="/wheelchair_icon.png" alt="Wheelchair impairment" />
          </button>
          <button
            className={`impairment-button ${impairment === 'blind' ? 'active' : ''}`}
            onClick={() => setImpairment('blind')}
          >
            <img src="/blind_icon.png" alt="Blind impairment" />
          </button>
        </div>
      </div>
    </div>
  );
};