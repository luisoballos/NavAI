import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './Home.css';

export const Home = () => {
  const navigate = useNavigate();
  const [origin, setOrigin] = useState('');
  const [destination, setDestination] = useState('');
  const [impairment, setImpairment] = useState(null); // 'wheelchair' o 'blind'
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSearch = async () => {
    setLoading(true);
    setError(null);
    console.log("Buscando ruta:", { origin, destination, impairment });

    try {
      const response = await fetch('http://127.0.0.1:5000/api/route_analysis', { // ¡Asegúrate
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ origin, destination, impairment }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Error desconocido al obtener la ruta.');
      }

      const data = await response.json();
      console.log("Datos de la ruta recibidos:", data);

      // Save data to send it to Navigation.jsx
      localStorage.setItem('routeData', JSON.stringify(data));

      navigate('/navegation');

    } catch (err) {
      setError(err.message);
      console.error("Error al buscar la ruta:", err);
    } finally {
      setLoading(false);
    }
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
            placeholder="Set the origin (e.g., Plaza de España, Madrid)"
            value={origin}
            onChange={(e) => setOrigin(e.target.value)}
            disabled={loading}
          />
        </div>
        <div className="search-input-group">
          <label htmlFor="destination-search" className="visually-hidden">Set the destination</label>
          <input
            type="text"
            id="destination-search"
            placeholder="Set the destination (e.g., Puerta del Sol, Madrid)"
            value={destination}
            onChange={(e) => setDestination(e.target.value)}
            disabled={loading}
          />
        </div>
        <button className="search-button" onClick={handleSearch} disabled={loading}>
          {loading ? 'Buscando Ruta...' : 'Search Route'}
        </button>
        {error && <p className="error-message" style={{color: 'red'}}>{error}</p>}
      </div>

      <div className="impairment-section">
        <h2 className="impairment-title">SELECT YOUR IMPAIRMENT</h2>
        <div className="impairment-options">
          <button
            className={`impairment-button ${impairment === 'wheelchair' ? 'active' : ''}`}
            onClick={() => setImpairment('wheelchair')}
            disabled={loading}
          >
            <img src="/wheelchair_icon.png" alt="Wheelchair impairment" />
          </button>
          <button
            className={`impairment-button ${impairment === 'blind' ? 'active' : ''}`}
            onClick={() => setImpairment('blind')}
            disabled={loading}
          >
            <img src="/blind_icon.png" alt="Blind impairment" />
          </button>
        </div>
      </div>
    </div>
  );
};