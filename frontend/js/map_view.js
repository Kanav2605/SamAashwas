// Leaflet GIS Map Visualization for CivicSense AI (SamAashwas) - Sticker Book Bus Stop Edition
let map;
let markersLayer = null;
let radiusLayer = null;

function initMap() {
  if (map) return;

  const defaultCenter = [12.95, 77.63]; // Bengaluru Central
  map = L.map('map', {
    center: defaultCenter,
    zoom: 13,
    zoomControl: true
  });

  // Flat & clean Carto Voyager tiles (fits the cream paper theme perfectly)
  L.tileLayer('https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png', {
    attribution: '&copy; <a href="https://carto.com/">CARTO</a> | &copy; OpenStreetMap contributors',
    maxZoom: 19
  }).addTo(map);

  markersLayer = L.layerGroup().addTo(map);
  radiusLayer = L.layerGroup().addTo(map);
}

function flyToCity(lat, lon, zoom = 12) {
  if (!map) initMap();
  map.flyTo([lat, lon], zoom, { duration: 1.2 });
}

function renderMapIncidents(masterTickets) {
  if (!map) initMap();
  markersLayer.clearLayers();
  radiusLayer.clearLayers();

  if (!masterTickets || masterTickets.length === 0) return;

  const bounds = [];

  masterTickets.forEach(ticket => {
    const lat = ticket.lat;
    const lon = ticket.lon;
    if (!lat || !lon) return;

    bounds.push([lat, lon]);

    // Flat color tokens based on urgency & report volume (NO GRADIENTS)
    let markerColor = '#FFC93C'; // mustard (Medium)
    if (ticket.urgency === 'Critical' || ticket.report_count >= 5) {
      markerColor = '#FF5A4E'; // tomato
    } else if (ticket.urgency === 'High' || ticket.report_count >= 2) {
      markerColor = '#FFB88A'; // peach
    } else if (ticket.status === 'RESOLVED') {
      markerColor = '#7BDCB5'; // mint
    }

    // 1. Draw 300m Spatial Clustering Gate Perimeter
    const circle = L.circle([lat, lon], {
      radius: 300,
      color: '#231F20',
      weight: 2,
      dashArray: '5, 5',
      fillColor: markerColor,
      fillOpacity: 0.18
    });
    radiusLayer.addLayer(circle);

    // 2. Custom circular sticker pin with report count & thick ink border
    const iconHtml = `
      <div style="
        background: ${markerColor};
        color: #231F20;
        border-radius: 50%;
        width: 30px;
        height: 30px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 12px;
        font-weight: 900;
        font-family: 'Fredoka', cursive, sans-serif;
        box-shadow: 2px 2px 0 #231F20;
        border: 2.5px solid #231F20;
        transform: rotate(-3deg);
      ">
        ${ticket.report_count}
      </div>
    `;

    const customIcon = L.divIcon({
      html: iconHtml,
      className: 'custom-map-pin',
      iconSize: [30, 30],
      iconAnchor: [15, 15]
    });

    const marker = L.marker([lat, lon], { icon: customIcon });

    const janTag = ticket.jan_sunwai_status === 'ESCALATED'
      ? '<span style="background: #B8A6FF; color: #231F20; border: 1.5px solid #231F20; padding: 2px 6px; border-radius: 9999px; font-weight: 800; font-size: 10px; box-shadow: 1px 1px 0 #231F20;">⚖️ Jan Sunwai</span>'
      : '';
    const missionTag = ticket.national_mission
      ? `<div style="font-size: 11px; color: #57534e; font-weight: 700; margin: 3px 0;">🇮🇳 ${ticket.national_mission.split('/')[0]}</div>`
      : '';

    const popupContent = `
      <div style="font-family: 'Nunito', sans-serif; font-size: 12px; color: #231F20; min-width: 220px; padding: 2px;">
        <strong style="color: #FF5A4E; font-family: 'Fredoka', cursive; font-size: 13px;">${ticket.master_ticket_id}</strong><br/>
        <strong style="font-size: 13px;">${ticket.title}</strong><br/>
        ${missionTag}
        <div style="margin: 6px 0; display: flex; gap: 4px; flex-wrap: wrap;">
          <span style="background: #FFEFD0; border: 1.5px solid #231F20; padding: 2px 6px; border-radius: 9999px; font-weight: 700;">${ticket.ward_name}</span>
          <span style="background: ${markerColor}; color: #231F20; border: 1.5px solid #231F20; padding: 2px 6px; border-radius: 9999px; font-weight: 800;">${ticket.urgency}</span>
          ${janTag}
        </div>
        <div style="margin-top: 4px;">👥 <strong>${ticket.report_count}</strong> Citizen Endorsements</div>
        <div>⏱️ SLA: <strong>${ticket.sla_hours_remaining}h</strong> remaining</div>
        <button onclick="openTicketModal('${ticket.master_ticket_id}')" style="margin-top: 8px; background: #FF5A4E; color: #FFFDF7; border: 2.5px solid #231F20; border-radius: 12px; padding: 6px 10px; cursor: pointer; width: 100%; font-family: 'Fredoka', cursive; font-weight: 800; font-size: 12px; box-shadow: 2px 2px 0 #231F20;">Inspect Master Incident &rarr;</button>
      </div>
    `;

    marker.bindPopup(popupContent);
    markersLayer.addLayer(marker);
  });

  if (bounds.length > 0) {
    map.fitBounds(bounds, { padding: [50, 50], maxZoom: 14 });
  }
}
