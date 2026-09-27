// CivicSense AI - Application Controller
let currentTickets = [];
let selectedTicketId = null;

document.addEventListener('DOMContentLoaded', () => {
  initMap();
  loadKPIStats();
  loadMasterTickets();
  loadPredictiveData();
});

// Tab Switcher
function switchTab(tabId) {
  document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
  document.querySelectorAll('.view-container').forEach(view => view.classList.remove('active'));

  const targetView = document.getElementById(tabId);
  if (targetView) targetView.classList.add('active');

  // Highlight clicked tab
  const btn = Array.from(document.querySelectorAll('.tab-btn')).find(b =>
    b.getAttribute('onclick').includes(tabId)
  );
  if (btn) btn.classList.add('active');

  // Trigger leaflet redraw if switching back to map
  if (tabId === 'command-center' && map) {
    setTimeout(() => {
      map.invalidateSize();
    }, 200);
  }
}

// Fetch KPI Stats
async function loadKPIStats() {
  try {
    const res = await fetch('/api/v1/analytics/stats');
    if (!res.ok) return;
    const stats = await res.json();

    document.getElementById('kpi-total-reports').innerText = stats.total_complaints;
    document.getElementById('kpi-master-tickets').innerText = stats.total_master_tickets;
    document.getElementById('kpi-dedup-rate').innerText = `${stats.deduplication_rate_pct}%`;
    document.getElementById('kpi-high-risk-wards').innerText = stats.high_risk_wards_count;
  } catch (e) {
    console.warn('Could not fetch stats, server might be offline:', e);
  }
}

// Load Master Tickets
async function loadMasterTickets() {
  const statusFilter = document.getElementById('status-filter').value;
  const url = statusFilter ? `/api/v1/master-tickets?status=${statusFilter}` : '/api/v1/master-tickets';

  try {
    const res = await fetch(url);
    if (!res.ok) return;
    currentTickets = await res.json();
    renderTicketList(currentTickets);
    renderMapIncidents(currentTickets);
  } catch (e) {
    console.error('Error fetching tickets:', e);
  }
}

function renderTicketList(tickets) {
  const listEl = document.getElementById('ticket-list');
  listEl.innerHTML = '';

  if (tickets.length === 0) {
    listEl.innerHTML = '<div style="padding: 1.5rem; text-align: center; color: var(--text-muted);">No incidents found.</div>';
    return;
  }

  tickets.forEach(t => {
    const card = document.createElement('div');
    card.className = `ticket-card ${selectedTicketId === t.master_ticket_id ? 'selected' : ''}`;
    card.onclick = () => openTicketModal(t.master_ticket_id);

    let badgeClass = 'badge-medium';
    if (t.urgency === 'Critical') badgeClass = 'badge-critical';
    else if (t.urgency === 'High') badgeClass = 'badge-high';
    else if (t.urgency === 'Low') badgeClass = 'badge-low';

    card.innerHTML = `
      <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 6px;">
        <span class="badge ${badgeClass}">${t.urgency}</span>
        <span class="badge-count">${t.report_count} reports</span>
      </div>
      <div style="font-weight: 600; font-size: 0.95rem; margin-bottom: 4px; color: #f1f5f9;">${t.title}</div>
      <div style="font-size: 0.75rem; color: var(--text-muted); margin-bottom: 6px;">
        📍 ${t.ward_name} &bull; 🏛️ ${t.department}
      </div>
      <div style="display: flex; justify-content: space-between; font-size: 0.75rem; color: #93c5fd;">
        <span>Status: <strong>${t.status}</strong></span>
        <span>⏱️ SLA: <strong>${t.sla_hours_remaining}h</strong></span>
      </div>
    `;

    listEl.appendChild(card);
  });
}

// Master Ticket Modal
function openTicketModal(ticketId) {
  selectedTicketId = ticketId;
  const ticket = currentTickets.find(t => t.master_ticket_id === ticketId);
  if (!ticket) return;

  document.getElementById('modal-ticket-id').innerText = ticket.master_ticket_id;
  document.getElementById('modal-ticket-title').innerText = ticket.title;
  document.getElementById('modal-dept').innerText = ticket.department;
  document.getElementById('modal-ward').innerText = ticket.ward_name;
  document.getElementById('modal-urgency').innerText = ticket.urgency;
  document.getElementById('modal-status').innerText = ticket.status;
  document.getElementById('modal-engineer').innerText = ticket.assigned_engineer;
  document.getElementById('modal-sla').innerText = `${ticket.sla_hours_remaining} hours remaining`;
  document.getElementById('modal-report-count').innerText = ticket.report_count;

  // Render linked citizen reports
  const reportsList = document.getElementById('modal-reports-list');
  reportsList.innerHTML = '';

  ticket.citizen_reports.forEach((r, idx) => {
    const reportItem = document.createElement('div');
    reportItem.style.background = '#1e293b';
    reportItem.style.padding = '8px 12px';
    reportItem.style.borderRadius = '6px';
    reportItem.style.border = '1px solid var(--border)';
    reportItem.style.fontSize = '0.8rem';

    reportItem.innerHTML = `
      <div style="display: flex; justify-content: space-between; color: #94a3b8; margin-bottom: 4px;">
        <strong>#${idx + 1} ${r.citizen_name} (${r.citizen_phone})</strong>
        <span>Channel: ${r.channel}</span>
      </div>
      <div style="color: #f8fafc; font-style: italic;">"${r.raw_text}"</div>
    `;
    reportsList.appendChild(reportItem);
  });

  document.getElementById('ticket-modal').style.display = 'flex';
}

function closeModal(event) {
  if (event && event.target !== document.getElementById('ticket-modal')) return;
  document.getElementById('ticket-modal').style.display = 'none';
}

async function updateTicketStatus(newStatus) {
  if (!selectedTicketId) return;
  try {
    const res = await fetch(`/api/v1/master-tickets/${selectedTicketId}`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ status: newStatus })
    });
    if (res.ok) {
      closeModal();
      loadMasterTickets();
      loadKPIStats();
    }
  } catch (e) {
    console.error('Error updating status:', e);
  }
}

// Load Predictive Data
async function loadPredictiveData() {
  try {
    const riskRes = await fetch('/api/v1/predictive-maintenance/ward-risk');
    const assetRes = await fetch('/api/v1/predictive-maintenance/assets');

    if (riskRes.ok) {
      const wards = await riskRes.json();
      renderWardRiskCards(wards);
    }

    if (assetRes.ok) {
      const assets = await assetRes.json();
      renderAssetTable(assets);
    }
  } catch (e) {
    console.error('Error loading predictive data:', e);
  }
}

function renderWardRiskCards(wards) {
  const container = document.getElementById('ward-risk-cards');
  container.innerHTML = '';

  wards.forEach(w => {
    const card = document.createElement('div');
    card.className = 'risk-card';

    let pillStyle = 'background: rgba(16, 185, 129, 0.2); color: #6ee7b7; border: 1px solid #10b981;';
    if (w.risk_level === 'CRITICAL') {
      pillStyle = 'background: rgba(239, 68, 68, 0.2); color: #f87171; border: 1px solid #ef4444;';
    } else if (w.risk_level === 'HIGH') {
      pillStyle = 'background: rgba(249, 115, 22, 0.2); color: #fb923c; border: 1px solid #f97316;';
    } else if (w.risk_level === 'MEDIUM') {
      pillStyle = 'background: rgba(245, 158, 11, 0.2); color: #fcd34d; border: 1px solid #f59e0b;';
    }

    card.innerHTML = `
      <div style="display: flex; justify-content: space-between; align-items: center;">
        <h3 style="font-size: 1.1rem; color: #fff;">${w.ward_name}</h3>
        <span class="risk-score-pill" style="${pillStyle}">${w.risk_score}</span>
      </div>
      <div style="font-size: 0.8rem; color: var(--text-muted);">
        🌧️ 48h Rain Forecast: <strong>${w.rainfall_forecast_48h_mm} mm</strong> &bull; Drainage Deficit: <strong>${w.drainage_vulnerability_score}%</strong>
      </div>
      <div style="font-size: 0.8rem; background: #0f172a; padding: 8px; border-radius: 4px; border-left: 3px solid #3b82f6;">
        <strong>Root Cause:</strong> ${w.primary_risk_factor}
      </div>
      <div style="font-size: 0.8rem; color: #93c5fd;">
        💡 <strong>Action:</strong> ${w.recommendation}
      </div>
    `;

    container.appendChild(card);
  });
}

function renderAssetTable(assets) {
  const tbody = document.getElementById('assets-table-body');
  tbody.innerHTML = '';

  assets.forEach(a => {
    const tr = document.createElement('tr');
    tr.style.borderBottom = '1px solid var(--border)';

    let probColor = '#10b981';
    if (a.failure_probability >= 70) probColor = '#ef4444';
    else if (a.failure_probability >= 50) probColor = '#f97316';

    tr.innerHTML = `
      <td style="padding: 8px; font-weight: bold; color: #60a5fa;">${a.asset_id}</td>
      <td style="padding: 8px;">${a.type}</td>
      <td style="padding: 8px;">${a.ward_id}</td>
      <td style="padding: 8px;">${a.structural_health_score}/100</td>
      <td style="padding: 8px; color: ${probColor}; font-weight: bold;">${a.failure_probability}%</td>
      <td style="padding: 8px; font-size: 0.8rem;">${a.recommended_action}</td>
    `;
    tbody.appendChild(tr);
  });
}

// Citizen Grievance Submission
async function handleCitizenSubmit(event) {
  event.preventDefault();

  const text = document.getElementById('complaint-text').value;
  const lat = parseFloat(document.getElementById('form-lat').value);
  const lon = parseFloat(document.getElementById('form-lon').value);
  const imageHint = document.getElementById('form-image-hint').value;
  const citizenName = document.getElementById('citizen-name').value;
  const citizenPhone = document.getElementById('citizen-phone').value;

  const resultContainer = document.getElementById('submission-result');
  resultContainer.style.display = 'block';
  resultContainer.innerHTML = '<div style="color: #60a5fa;">Submitting to AI Pipeline (NLP + Vision Verification + Deduplication)...</div>';

  try {
    const res = await fetch('/api/v1/complaints/submit', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        raw_text: text,
        lat: lat,
        lon: lon,
        citizen_name: citizenName,
        citizen_phone: citizenPhone,
        image_category_hint: imageHint || null
      })
    });

    if (res.ok) {
      const data = await res.json();
      const isDup = data.is_duplicate;
      const vision = data.image_verification;

      let visionBadge = '';
      if (vision) {
        visionBadge = vision.is_authentic
          ? `<span class="badge badge-low">Vision: ${vision.status_label}</span>`
          : `<span class="badge badge-critical">Vision: ${vision.status_label}</span>`;
      }

      resultContainer.innerHTML = `
        <div style="font-weight: bold; color: #34d399; margin-bottom: 6px;">
          ✓ Grievance Processed Successfully!
        </div>
        <div><strong>Assigned Ticket:</strong> ${data.master_ticket_id}</div>
        <div><strong>Department:</strong> ${data.department} (${data.issue_type})</div>
        <div><strong>Urgency:</strong> ${data.urgency} | <strong>Language:</strong> ${data.language_detected}</div>
        <div style="margin-top: 4px;">
          ${isDup
            ? '<span class="badge badge-high">Duplicate Merged: Linked to existing neighborhood master ticket</span>'
            : '<span class="badge badge-low">Unique Incident: New Master Ticket Created</span>'
          }
          ${visionBadge}
        </div>
      `;

      loadMasterTickets();
      loadKPIStats();
    } else {
      resultContainer.innerHTML = '<div style="color: #ef4444;">Failed to submit grievance. Please try again.</div>';
    }
  } catch (err) {
    resultContainer.innerHTML = `<div style="color: #ef4444;">Network error: ${err.message}</div>`;
  }
}

function detectLocation() {
  // Set random realistic coordinate in Koramangala / Indiranagar
  const coords = [
    { lat: 12.9352, lon: 77.6245 },
    { lat: 12.9716, lon: 77.6412 },
    { lat: 12.9121, lon: 77.6446 }
  ];
  const chosen = coords[Math.floor(Math.random() * coords.length)];
  document.getElementById('form-lat').value = chosen.lat;
  document.getElementById('form-lon').value = chosen.lon;
}
