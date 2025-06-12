import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import './Loading.css'; // Crea este archivo CSS para los estilos

export const Loading = () => {
  const navigate = useNavigate();

  useEffect(() => {
    // Simula un tiempo de carga (ej: 3 segundos)
    const timer = setTimeout(() => {
      navigate('/navegation'); // Navega a la página de navegación después de la carga
    }, 3000); // Ajusta el tiempo de carga según sea necesario

    return () => clearTimeout(timer); // Limpia el temporizador si el componente se desmonta
  }, [navigate]);

  return (
    <div className="loading-container">
      <h1 className="loading-text">LOADING...</h1>
    </div>
  );
};