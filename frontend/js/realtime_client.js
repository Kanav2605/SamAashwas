/**
 * SamAashwas - Real-Time Civic Intelligence & WebSocket Synchronization Client
 * Handles sub-50ms event streaming, live squad fleet telemetry on GIS maps,
 * instantaneous citizen login reactivity, and real-time KPI odometer updates.
 */

let realtimeSocket = null;
let realtimeEventSource = null;
let realtimePingStart = 0;
let realtimeLatency = 12;
let realtimeEventCount = 0;
let liveFleetMarkers = {};

function initRealtimeClient() {
  initLiveClock();
  connectWebSocket();
}

function initLiveClock() {
  const clockEl = document.getElementById('live-ist-clock');
  function updateClock() {
    if (!clockEl) return;
    const now = new Date();
    const options = { timeZone: 'Asia/Kolkata', hour12: false, hour: '2-digit', minute: '2-digit', second: '2-digit' };
    const timeStr = now.toLocaleTimeString('en-IN', options);
    const dateStr = now.toLocaleDateString('en-IN', { timeZone: 'Asia/Kolkata', day: '2-digit', month: 'short' });
    clockEl.innerHTML = `<strong>${timeStr}</strong> <span style="opacity: 0.75; font-size: 0.8em;">IST • ${dateStr}</span>`;
  }
  updateClock();
  setInterval(updateClock, 1000);
}

function connectWebSocket() {
  const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
  const host = window.location.host || '127.0.0.1:8000';
  const wsUrl = `${protocol}//${host}/ws/live`;

  updateRealtimeStatus('connecting', 'Connecting Live Feed...');

  try {
    realtimeSocket = new WebSocket(wsUrl);

    realtimeSocket.onopen = () => {
      updateRealtimeStatus('connected', '🟢 LIVE');
      sendPing();
      setInterval(sendPing, 10000);
    };

    realtimeSocket.onmessage = (event) => {
      try {
        const payload = JSON.parse(event.data);
        handleRealtimeMessage(payload);
      } catch (err) {
        console.error("Failed to parse realtime packet:", err);
      }
    };

    realtimeSocket.onclose = () => {
      updateRealtimeStatus('disconnected', '🟡 Reconnecting...');
      fallbackToSSE();
      setTimeout(connectWebSocket, 4000);
    };

    realtimeSocket.onerror = (err) => {
      console.warn("WebSocket stream error, failing over to SSE:", err);
      fallbackToSSE();
    };

  } catch (err) {
    console.warn("WebSocket initialization exception, using SSE fallback:", err);
    fallbackToSSE();
  }
}

function sendPing() {
  if (realtimeSocket && realtimeSocket.readyState === WebSocket.OPEN) {
    realtimePingStart = performance.now();
    realtimeSocket.send(JSON.stringify({ action: "PING", timestamp: Date.now() }));
  }
}

function fallbackToSSE() {
  if (realtimeEventSource) return;
  try {
    realtimeEventSource = new EventSource('/api/v1/stream/events');
    realtimeEventSource.onmessage = (event) => {
      try {
        const payload = JSON.parse(event.data);
        handleRealtimeMessage(payload);
      } catch (err) {}
    };
    realtimeEventSource.onerror = () => {
      realtimeEventSource.close();
      realtimeEventSource = null;
    };
  } catch (err) {
    console.error("SSE fallback failed:", err);
  }
}

function updateRealtimeStatus(state, label) {
  const badge = document.getElementById('realtime-status-pill');
  if (!badge) return;

  if (state === 'connected') {
    badge.innerHTML = `<span class="live-dot-pulse"></span> <span style="font-weight: 800;">${label}</span> <span class="latency-tag">${realtimeLatency}ms</span>`;
    badge.style.background = '#ecfdf5';
    badge.style.color = '#065f46';
    badge.style.border = '1px solid #10b981';
  } else if (state === 'connecting') {
    badge.innerHTML = `<span style="font-size: 0.75rem;">⏳ ${label}</span>`;
    badge.style.background = '#fef3c7';
    badge.style.color = '#92400e';
    badge.style.border = '1px solid #f59e0b';
  } else {
    badge.innerHTML = `<span style="font-size: 0.75rem;">⚠️ ${label}</span>`;
    badge.style.background = '#f1f5f9';
    badge.style.color = '#475569';
    badge.style.border = '1px solid #cbd5e1';
  }
}

function handleRealtimeMessage(payload) {
  realtimeEventCount++;
  const countBadge = document.getElementById('realtime-packet-count');
  if (countBadge) {
    countBadge.innerText = `${realtimeEventCount} msgs`;
  }

  if (payload.type === 'PONG') {
    if (realtimePingStart > 0) {
      realtimeLatency = Math.max(4, Math.round(performance.now() - realtimePingStart));
      updateRealtimeStatus('connected', '🟢 LIVE');
    }
    return;
  }

  const data = payload.data || {};

  // 1. Live Fleet Telemetry Update
  if (payload.type === 'FLEET_TELEMETRY_PULSE' && data.squads) {
    updateMapFleetTelemetry(data.squads);
  }

  // 2. New Citizen Grievance Lodged Real-time
  else if (payload.type === 'NEW_GRIEVANCE_LODGED') {
    handleNewGrievanceEvent(data);
  }

  // 3. Citizen Presence Login / Session Broadcast
  else if (payload.type === 'CITIZEN_PRESENCE_LOGIN') {
    handleCitizenPresenceEvent(data);
  }

  // 4. Civic Activity Stream / Automated Audit Event
  else if (payload.type === 'CIVIC_ACTIVITY_STREAM_EVENT') {
    handleCivicActivityEvent(data);
  }

  // Append to Real-Time Wire Feed Drawer
  appendRealtimeWireItem(payload);
}

function updateMapFleetTelemetry(squads) {
  if (typeof map === 'undefined' || !map) return;

  squads.forEach(sq => {
    if (liveFleetMarkers[sq.id]) {
      // Smoothly move existing marker
      liveFleetMarkers[sq.id].setLatLng([sq.lat, sq.lon]);
    } else {
      // Create modern vehicle marker with pulsing halo
      if (typeof L !== 'undefined' && L.divIcon) {
        const vehicleIcon = L.divIcon({
          className: 'custom-fleet-pin',
          html: `
            <div style="position: relative; width: 34px; height: 34px; background: #0f172a; border: 2px solid #ffffff; border-radius: 50%; box-shadow: 0 4px 10px rgba(0,0,0,0.3); display: flex; align-items: center; justify-content: center; font-size: 16px;">
              🚑
              <span style="position: absolute; top: -3px; right: -3px; width: 10px; height: 10px; background: #10b981; border: 1.5px solid white; border-radius: 50%; animation: pulse-beacon 1.5s infinite;"></span>
            </div>
          `,
          iconSize: [34, 34],
          iconAnchor: [17, 17]
        });

        const m = L.marker([sq.lat, sq.lon], { icon: vehicleIcon }).addTo(map);
        m.bindPopup(`
          <div style="font-family: var(--font-body); padding: 4px;">
            <strong style="color: #0f172a; font-size: 0.9rem;">${sq.name}</strong><br>
            <span style="font-size: 0.78rem; color: #475569;">Speed: <strong>${sq.speed_kmh} km/h</strong> • Status: <strong style="color: #059669;">${sq.status}</strong></span>
          </div>
        `);
        liveFleetMarkers[sq.id] = m;
      }
    }
  });

  // Update telemetry panel counters if visible
  const squadCountEl = document.getElementById('fleet-active-squad-count');
  if (squadCountEl) squadCountEl.innerText = `${squads.length} Units Active`;
}

function handleNewGrievanceEvent(complaint) {
  // Play subtle tactile audio ping
  if (window.civicAudio && typeof window.civicAudio.playClick === 'function') {
    window.civicAudio.playClick();
  }

  // Increment KPI counters smoothly
  incrementKpiCounter('kpi-total-grievances');
  incrementKpiCounter('kpi-active-tickets');

  // Flash real-time toast
  showModernToast(`⚡ <strong>Live Report Lodged:</strong> ${complaint.category || 'Civic Issue'} in ${complaint.ward || 'Municipal Ward'}`, 'info', 4500);

  // If map is loaded, drop animated ripple marker
  if (typeof map !== 'undefined' && map && complaint.lat && complaint.lon) {
    if (typeof L !== 'undefined') {
      const pingIcon = L.divIcon({
        className: 'new-incident-ping',
        html: `
          <div style="position: relative; width: 28px; height: 28px; background: #ea580c; border: 2px solid white; border-radius: 50%; box-shadow: 0 0 15px #ea580c; display: flex; align-items: center; justify-content: center; font-size: 13px; color: white;">
            ⚠️
            <span class="incident-radar-halo"></span>
          </div>
        `,
        iconSize: [28, 28],
        iconAnchor: [14, 14]
      });

      const incidentMarker = L.marker([complaint.lat, complaint.lon], { icon: pingIcon }).addTo(map);
      incidentMarker.bindPopup(`
        <div style="font-family: var(--font-body); padding: 4px;">
          <strong style="color: #ea580c;">⚡ Just Lodged in Real-Time</strong><br>
          <strong>${complaint.category || 'Grievance'}</strong><br>
          <span style="font-size: 0.8rem; color: #475569;">${complaint.description || ''}</span><br>
          <span style="font-size: 0.74rem; color: #64748b;">ID: ${complaint.complaint_id || complaint.id || 'Pending'}</span>
        </div>
      `).openPopup();

      // Pan slightly if within city view
      setTimeout(() => {
        if (map.getBounds().contains([complaint.lat, complaint.lon])) {
          map.panTo([complaint.lat, complaint.lon], { animate: true });
        }
      }, 500);
    }
  }

  // Prepend to Master Tickets Table if view is active
  prependRealtimeTicketRow(complaint);
}

function handleCitizenPresenceEvent(user) {
  showModernToast(`👤 <strong>Citizen Online:</strong> ${user.name} logged in from ${user.city}!`, 'success', 3500);
  const activeCountEl = document.getElementById('realtime-online-citizens');
  if (activeCountEl) {
    const cur = parseInt(activeCountEl.innerText) || 12;
    activeCountEl.innerText = `${cur + 1} Citizens Active`;
  }
}

function handleCivicActivityEvent(eventData) {
  // Update Public Ticker smoothly
  const tickerEl = document.getElementById('public-ticker-text');
  if (tickerEl && eventData.message) {
    tickerEl.innerHTML = `⚡ <strong>REAL-TIME CIVIC FEED:</strong> ${eventData.message} (${eventData.ward || eventData.city || 'Smart Grid'})`;
  }
}

function prependRealtimeTicketRow(complaint) {
  const tbody = document.getElementById('command-tickets-tbody');
  if (!tbody) return;

  const row = document.createElement('tr');
  row.className = 'realtime-new-row';
  row.innerHTML = `
    <td><strong style="color: var(--theme-primary); font-family: var(--font-mono);">${complaint.complaint_id || 'CMP-LIVE'}</strong></td>
    <td><span class="badge badge-warning">NEW (Live)</span></td>
    <td><strong>${complaint.category || 'Civic'}</strong></td>
    <td>${complaint.ward || 'Ward Central'}</td>
    <td><span style="font-size: 0.8rem; color: #64748b;">Just now</span></td>
    <td>
      <button class="btn-sm btn-outline" onclick="quickTrackDemo('${complaint.complaint_id || ''}')">Track</button>
    </td>
  `;

  tbody.insertBefore(row, tbody.firstChild);
}

function incrementKpiCounter(elementId) {
  const el = document.getElementById(elementId);
  if (!el) return;
  const rawText = el.innerText.replace(/[^0-9]/g, '');
  const curVal = parseInt(rawText) || 0;
  const nextVal = curVal + 1;
  el.innerText = nextVal.toLocaleString('en-IN');
  el.classList.add('kpi-counter-bump');
  setTimeout(() => el.classList.remove('kpi-counter-bump'), 600);
}

function appendRealtimeWireItem(payload) {
  const listEl = document.getElementById('realtime-wire-list');
  if (!listEl) return;

  const item = document.createElement('div');
  item.className = 'wire-item';
  const timeStr = new Date().toLocaleTimeString('en-IN', { hour12: false, hour: '2-digit', minute: '2-digit', second: '2-digit' });

  let typeBadge = '<span class="wire-tag tag-blue">PULSE</span>';
  let desc = 'Telemetry heartbeat received';

  if (payload.type === 'NEW_GRIEVANCE_LODGED') {
    typeBadge = '<span class="wire-tag tag-orange">GRIEVANCE</span>';
    desc = `New ticket lodged: ${payload.data.category || 'Civic'} in ${payload.data.ward || 'Ward'}`;
  } else if (payload.type === 'CITIZEN_PRESENCE_LOGIN') {
    typeBadge = '<span class="wire-tag tag-green">CITIZEN</span>';
    desc = `${payload.data.name} authenticated (${payload.data.city})`;
  } else if (payload.type === 'CIVIC_ACTIVITY_STREAM_EVENT') {
    typeBadge = '<span class="wire-tag tag-purple">AI ACTION</span>';
    desc = payload.data.message || 'Automated multi-agent pass complete';
  } else if (payload.type === 'FLEET_TELEMETRY_PULSE') {
    typeBadge = '<span class="wire-tag tag-teal">FLEET</span>';
    desc = `Squad patrol vectors updated (${payload.data.active_squad_count} squads)`;
  }

  item.innerHTML = `
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 2px;">
      ${typeBadge}
      <span style="font-family: var(--font-mono); font-size: 0.72rem; color: #94a3b8;">${timeStr}</span>
    </div>
    <div style="font-size: 0.82rem; color: #1e293b; font-weight: 600;">${desc}</div>
  `;

  listEl.insertBefore(item, listEl.firstChild);
  if (listEl.children.length > 25) {
    listEl.removeChild(listEl.lastChild);
  }
}

function toggleRealtimeWireDrawer() {
  const drawer = document.getElementById('realtime-wire-drawer');
  if (!drawer) return;
  drawer.classList.toggle('active');
  if (window.civicAudio && typeof window.civicAudio.playClick === 'function') {
    window.civicAudio.playClick();
  }
}

function showModernToast(message, type = 'info', duration = 3800) {
  let container = document.getElementById('modern-toast-container');
  if (!container) {
    container = document.createElement('div');
    container.id = 'modern-toast-container';
    document.body.appendChild(container);
  }

  const toast = document.createElement('div');
  toast.className = `modern-toast toast-${type}`;
  toast.innerHTML = `
    <div style="display: flex; align-items: center; gap: 8px;">
      <div style="flex: 1; font-size: 0.85rem;">${message}</div>
      <button type="button" style="background: none; border: none; font-size: 1.1rem; cursor: pointer; color: #64748b;" onclick="this.parentElement.parentElement.remove()">×</button>
    </div>
  `;

  container.appendChild(toast);
  setTimeout(() => {
    toast.classList.add('toast-show');
  }, 10);

  setTimeout(() => {
    toast.classList.remove('toast-show');
    setTimeout(() => toast.remove(), 300);
  }, duration);
}

// Global exposure
window.initRealtimeClient = initRealtimeClient;
window.toggleRealtimeWireDrawer = toggleRealtimeWireDrawer;
window.showModernToast = showModernToast;

// Auto-initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
  initRealtimeClient();
});
