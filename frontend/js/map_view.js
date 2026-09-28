// Leaflet GIS Map Visualization for CivicSense AI (SamAashwas)
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

  // Dark-themed OpenStreetMap tiles
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

    // Color code based on urgency & report volume
    let markerColor = '#f59e0b'; // Medium
    if (ticket.urgency === 'Critical' || ticket.report_count >= 5) {
      markerColor = '#ef4444';
    } else if (ticket.urgency === 'High' || ticket.report_count >= 2) {
      markerColor = '#f97316';
    } else if (ticket.status === 'RESOLVED') {
      markerColor = '#10b981';
    }

    // 1. Draw 300m Spatial Clustering Gate Perimeter
    const circle = L.circle([lat, lon], {
      radius: 300,
      color: markerColor,
      weight: 1.5,
      dashArray: '4, 4',
      fillColor: markerColor,
      fillOpacity: 0.12
    });
    radiusLayer.addLayer(circle);

    // 2. Custom circular marker icon with report count
    const iconHtml = `
      <div style="
        background: ${markerColor};
        color: white;
        border-radius: 50%;
        width: 28px;
        height: 28px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 11px;
        font-weight: bold;
        box-shadow: 0 0 10px rgba(0,0,0,0.5);
        border: 2px solid white;
      ">
        ${ticket.report_count}
      </div>
    `;

    const customIcon = L.divIcon({
      html: iconHtml,
      className: 'custom-map-pin',
      iconSize: [28, 28],
      iconAnchor: [14, 14]
    });

    const marker = L.marker([lat, lon], { icon: customIcon });

    const janTag = ticket.jan_sunwai_status === 'ESCALATED'
      ? '<span style="background: #dc2626; color: white; padding: 2px 5px; border-radius: 3px; font-weight: bold; font-size: 10px;">⚖️ Jan Sunwai</span>'
      : '';
    const missionTag = ticket.national_mission
      ? `<div style="font-size: 11px; color: #475569; margin: 3px 0;">🇮🇳 ${ticket.national_mission.split('/')[0]}</div>`
      : '';

    const popupContent = `
      <div style="font-family: sans-serif; font-size: 12px; color: #1e293b; min-width: 220px;">
        <strong style="color: #1e3a8a;">${ticket.master_ticket_id}</strong><br/>
        <strong>${ticket.title}</strong><br/>
        ${missionTag}
        <div style="margin: 4px 0; display: flex; gap: 4px; flex-wrap: wrap;">
          <span style="background: #e2e8f0; padding: 2px 5px; border-radius: 3px;">${ticket.ward_name}</span>
          <span style="background: ${markerColor}; color: white; padding: 2px 5px; border-radius: 3px; font-weight: bold;">${ticket.urgency}</span>
          ${janTag}
        </div>
        <div>👥 <strong>${ticket.report_count}</strong> Citizen Endorsements</div>
        <div>⏱️ SLA: <strong>${ticket.sla_hours_remaining}h</strong> remaining</div>
        <button onclick="openTicketModal('${ticket.master_ticket_id}')" style="margin-top: 6px; background: #2563eb; color: white; border: none; padding: 5px 8px; border-radius: 4px; cursor: pointer; width: 100%; font-weight: 600;">Inspect Master Incident</button>
      </div>
    `;

    marker.bindPopup(popupContent);
    markersLayer.addLayer(marker);
  });

  if (bounds.length > 0) {
    map.fitBounds(bounds, { padding: [50, 50], maxZoom: 14 });
  }
}
