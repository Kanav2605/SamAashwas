// Live City Simulation & Digital Twin Fleet Telemetry
// Real-time squad patrol animation on Leaflet map, live radio dispatch console, and crew telemetry

let isSimulationActive = false;
let simulationInterval = null;
let squadMarkers = {};
let currentFleetData = null;
let radioLogCounter = 0;

async function toggleCitySimulation() {
  const btn = document.getElementById('btn-toggle-simulation');
  isSimulationActive = !isSimulationActive;

  if (btn) {
    btn.classList.toggle('active', isSimulationActive);
    btn.innerHTML = isSimulationActive 
      ? '⏹️ Stop City Simulation' 
      : '🚜 Live City Simulation &amp; Squad Fleet';
  }

  const container = document.getElementById('fleet-telemetry-panel');
  if (container) {
    container.style.display = isSimulationActive ? 'block' : 'none';
  }

  if (isSimulationActive) {
    if (window.civicAudio && typeof window.civicAudio.playRisingTone === 'function') {
      window.civicAudio.playRisingTone();
    }
    await fetchAndRenderFleet();
    simulationInterval = setInterval(animateSquadPatrolStep, 4000);
  } else {
    if (simulationInterval) clearInterval(simulationInterval);
    removeSquadMarkers();
    if (window.civicAudio && typeof window.civicAudio.playClick === 'function') {
      window.civicAudio.playClick();
    }
  }
}

async function fetchAndRenderFleet() {
  const activeCity = (typeof currentSelectedCity !== 'undefined' && currentSelectedCity) ? currentSelectedCity : 'bengaluru';
  try {
    const res = await fetch(`/api/v1/dispatch/fleet-telemetry?city=${encodeURIComponent(activeCity)}`);
    if (res.ok) {
      const data = await res.json();
      currentFleetData = data;
      renderFleetCards(data);
      renderSquadMarkersOnMap(data);
      initRadioChatter(data.radio_chatter);
    }
  } catch (err) {
    console.error("Failed to fetch fleet telemetry:", err);
  }
}

function renderFleetCards(data) {
  const grid = document.getElementById('fleet-squads-grid');
  if (!grid || !data.squads) return;

  grid.innerHTML = data.squads.map(s => {
    const badgeClass = s.status === 'EN_ROUTE' ? 'en_route' : (s.status === 'OPERATIONAL' ? 'operational' : 'active');
    const statusLabel = s.status === 'EN_ROUTE' ? 'En Route (24 km/h)' : (s.status === 'OPERATIONAL' ? 'Clearing Site' : 'Active Repairs');

    return `
      <div class="squad-card" onclick="openSquadDossier('${s.squad_id}')" style="cursor: pointer;" title="Click to inspect live telemetry dossier">
        <div class="squad-card-header">
          <div class="squad-title">${s.icon} ${s.name}</div>
          <span class="squad-badge ${badgeClass}">${statusLabel}</span>
        </div>
        <div style="font-size: 0.74rem; color: var(--text-muted); font-weight: 700; margin-bottom: 6px;">
          ${s.vehicle_type}
        </div>
        <div class="squad-telemetry-row">
          <span>Target Incident:</span>
          <strong style="color: var(--tomato);">${s.assigned_ticket_id}</strong>
        </div>
        <div class="squad-telemetry-row">
          <span>Lead Officer:</span>
          <span>${s.lead_officer}</span>
        </div>
        <div class="squad-telemetry-row">
          <span>Crew Headcount:</span>
          <span>👷 ${s.personnel_count} Specialists</span>
        </div>
        <div class="squad-telemetry-row">
          <span>Vehicle Fuel:</span>
          <span>⛽ ${s.fuel_level_pct}% • ETA: <strong>${s.eta_minutes}m</strong></span>
        </div>
        <div style="font-size: 0.70rem; color: var(--ink); margin-top: 6px; padding-top: 6px; border-top: 1px dashed var(--ink); font-style: italic;">
          "${s.current_action}"
        </div>
      </div>
    `;
  }).join('');
}

function renderSquadMarkersOnMap(data) {
  if (typeof map === 'undefined' || !map) return;
  if (!data.squads) return;

  data.squads.forEach(s => {
    const iconHtml = `
      <div style="
        background: #231F20;
        color: #FFC93C;
        border: 2px solid #FFFDF7;
        border-radius: 50%;
        width: 38px;
        height: 38px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 18px;
        box-shadow: 2px 2px 0 #231F20;
        animation: pulseSiren 1.5s infinite;
      ">
        ${s.icon}
      </div>
    `;

    const squadIcon = L.divIcon({
      html: iconHtml,
      className: 'squad-vehicle-icon',
      iconSize: [38, 38],
      iconAnchor: [19, 19]
    });

    if (squadMarkers[s.squad_id]) {
      squadMarkers[s.squad_id].setLatLng([s.lat, s.lon]);
    } else {
      const marker = L.marker([s.lat, s.lon], { icon: squadIcon });
      marker.bindPopup(`
        <div style="font-family: 'Nunito', sans-serif; font-size: 12px; color: #231F20; min-width: 200px;">
          <strong style="color: #FF5A4E; font-size: 13px; font-family: 'Fredoka', cursive;">${s.icon} ${s.name}</strong><br>
          <span style="font-size: 11px; font-weight: 700;">${s.vehicle_type}</span>
          <hr style="margin: 4px 0; border: none; border-top: 1px solid #231F20;">
          <div>📍 Action: <strong>${s.current_action}</strong></div>
          <div>⏱️ ETA to Site: <strong>${s.eta_minutes} mins</strong></div>
          <div>👥 Crew: <strong>${s.personnel_count} personnel</strong></div>
          <button onclick="openSquadDossier('${s.squad_id}')" style="margin-top: 6px; background: #FFC93C; color: #231F20; border: 2px solid #231F20; border-radius: 8px; padding: 4px 8px; cursor: pointer; width: 100%; font-weight: 800; font-size: 11px;">Inspect Squad Dossier &rarr;</button>
        </div>
      `);
      marker.addTo(map);
      squadMarkers[s.squad_id] = marker;
    }
  });
}

function removeSquadMarkers() {
  if (typeof map === 'undefined' || !map) return;
  Object.keys(squadMarkers).forEach(k => {
    map.removeLayer(squadMarkers[k]);
  });
  squadMarkers = {};
}

function animateSquadPatrolStep() {
  if (!isSimulationActive || !currentFleetData || !currentFleetData.squads) return;

  currentFleetData.squads.forEach(s => {
    // Slight jitter/interpolation towards target or along patrol route
    const dLat = (Math.random() - 0.48) * 0.0008;
    const dLon = (Math.random() - 0.48) * 0.0008;
    s.lat += dLat;
    s.lon += dLon;

    // Modulate speed
    if (s.status === 'EN_ROUTE') {
      s.speed_kmh = Math.max(12, Math.min(38, Math.round((s.speed_kmh + (Math.random() - 0.5) * 4) * 10) / 10));
    }

    if (squadMarkers[s.squad_id]) {
      squadMarkers[s.squad_id].setLatLng([s.lat, s.lon]);
    }
  });

  renderFleetCards(currentFleetData);
  appendRadioChatterStep();
}

function initRadioChatter(logs) {
  const consoleEl = document.getElementById('radio-chatter-console');
  if (!consoleEl || !logs) return;

  consoleEl.innerHTML = logs.map(l => `
    <div class="radio-line">
      [${l.timestamp}] <span class="radio-sender">${l.sender}:</span> ${l.message}
    </div>
  `).join('');
  consoleEl.scrollTop = consoleEl.scrollHeight;
}

function appendRadioChatterStep() {
  const consoleEl = document.getElementById('radio-chatter-console');
  if (!consoleEl) return;

  const now = new Date();
  const timeStr = now.toTimeString().split(' ')[0];

  const simulationEvents = [
    { sender: "Squad Alpha-1", msg: "Asphalt compaction in progress. Subgrade density confirmed. Sealing edges." },
    { sender: "Control Room", msg: "Copy Alpha-1. Stand by for routing to Ward 4 culvert inspection after completion." },
    { sender: "Squad Bravo-3", msg: "Sanitation tipper full. En route to designated dry waste collection facility." },
    { sender: "Squad Gamma-2", msg: "Streetlight luminaire energized and lum flux verified at 4200 lumens. Clear on channel 4." },
    { sender: "Control Room", msg: "Telemetry sync complete. 100% field fleet GPS tracking operational." }
  ];

  const ev = simulationEvents[radioLogCounter % simulationEvents.length];
  radioLogCounter++;

  const lineEl = document.createElement('div');
  lineEl.className = 'radio-line';
  lineEl.innerHTML = `[${timeStr}] <span class="radio-sender">${ev.sender}:</span> ${ev.msg}`;
  consoleEl.appendChild(lineEl);
  consoleEl.scrollTop = consoleEl.scrollHeight;

  // Very soft walkie-talkie audio click
  if (window.civicAudio && typeof window.civicAudio.playClick === 'function') {
    window.civicAudio.playClick();
  }
}

function openSquadDossier(squadId) {
  if (!currentFleetData || !currentFleetData.squads) return;
  const s = currentFleetData.squads.find(x => x.squad_id === squadId);
  if (!s) return;

  alert(`🚜 ${s.name} Telemetry Dossier\n\nCallsign: ${s.callsign}\nVehicle: ${s.vehicle_type}\nLead Officer: ${s.lead_officer}\nPersonnel: ${s.personnel_count} crew members\nFuel Level: ${s.fuel_level_pct}%\nCurrent Action: ${s.current_action}\nAssigned Master Ticket: ${s.assigned_ticket_id}\n\nEquipment Onboard:\n• ${s.equipment.join('\n• ')}`);
}

// Expose globals
window.toggleCitySimulation = toggleCitySimulation;
window.openSquadDossier = openSquadDossier;
