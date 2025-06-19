import React, { useEffect } from 'react';
import { useMap } from 'react-leaflet';
import L from 'leaflet';

import './MapLegend.css';

const MapLegend = ({ legendItems, position = 'bottomright' }) => {
  const map = useMap();

  useEffect(() => {
    if (!map)
      return;

    const legend = L.control({ position: position });

    legend.onAdd = function () {
      const div = L.DomUtil.create('div', 'info legend');
      let labels = [];

      for (let i = 0; i < legendItems.length; i++) {
        labels.push(
          `<i style="background:${legendItems[i].color}"></i> ${legendItems[i].category}`
        );
      }

      div.innerHTML = '<h4>Leyenda de Accesibilidad</h4>' + labels.join('<br>');
      return div;
    };

    legend.addTo(map);

    return () => {
      legend.remove();
    };
  }, [map, legendItems, position]);

  return null;
};

export default MapLegend;