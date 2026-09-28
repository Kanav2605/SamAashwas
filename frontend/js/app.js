// CivicSense AI (SamAashwas) - Main Application Controller
let currentTickets = [];
let selectedTicketId = null;
let isRecording = null;
let speechRecognizer = null;
let allWardsData = [];

document.addEventListener('DOMContentLoaded', () => {
  // Restore language preference
  const savedLang = localStorage.getItem('civicsense_lang') || 'en';
  if (typeof setLanguage === 'function') setLanguage(savedLang);

  // Restore sunlight mode preference
  if (localStorage.getItem('civicsense_sunlight') === 'true') {
    document.body.classList.add('sunlight-mode');
    updateSunlightButtonText();
  }

  // Restore lite mode preference
  if (localStorage.getItem('civicsense_lite') === 'true') {
    document.body.classList.add('lite-data-mode');
  }

  initMap();
  loadKPIStats();
  loadMasterTickets();
  loadPredictiveData();
  loadWardGovernanceData();
});

// Tab Switcher for Desktop & Mobile
function switchTab(tabId) {
  document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
  document.querySelectorAll('.mobile-nav-item').forEach(btn => btn.classList.remove('active'));
  document.querySelectorAll('.view-container').forEach(view => view.classList.remove('active'));

  const targetView = document.getElementById(tabId);
  if (targetView) targetView.classList.add('active');

  // Highlight desktop tab
  const desktopBtn = document.querySelector(`.tab-btn[data-tab="${tabId}"]`);
  if (desktopBtn) desktopBtn.classList.add('active');

  // Highlight mobile nav button
  const mobileBtn = document.querySelector(`.mobile-nav-item[data-tab="${tabId}"]`);
  if (mobileBtn) mobileBtn.classList.add('active');

  // Redraw leaflet if switching to map
  if (tabId === 'command-center' && typeof map !== 'undefined' && map) {
    setTimeout(() => {
      map.invalidateSize();
    }, 200);
  }

  if (tabId === 'jan-sunwai-view') {
    loadWardGovernanceData();
  }
}

// Fetch KPI Stats with National Missions & Jan Sunwai
async function loadKPIStats() {
  try {
    const res = await fetch('/api/v1/analytics/stats');
    if (!res.ok) return;
    const stats = await res.json();

    document.getElementById('kpi-total-reports').innerText = stats.total_complaints;
    document.getElementById('kpi-master-tickets').innerText = stats.total_master_tickets;
    document.getElementById('kpi-dedup-rate').innerText = `${stats.deduplication_rate_pct}%`;
    document.getElementById('kpi-high-risk-wards').innerText = stats.high_risk_wards_count;
    
    const janCountEl = document.getElementById('kpi-jan-sunwai-count');
    if (janCountEl) {
      janCountEl.innerText = stats.jan_sunwai_escalated_count || 0;
    }
  } catch (e) {
    console.warn('Could not fetch stats:', e);
  }
}

// Load Master Tickets with Filters
async function loadMasterTickets() {
  const statusFilter = document.getElementById('status-filter').value;
  let url = '/api/v1/master-tickets';

  if (statusFilter === 'JAN_SUNWAI') {
    url = '/api/v1/master-tickets?jan_sunwai_only=true';
  } else if (statusFilter) {
    url = `/api/v1/master-tickets?status=${statusFilter}`;
  }

  try {
    const res = await fetch(url);
    if (!res.ok) return;
    currentTickets = await res.json();
    const zoneFilterEl = document.getElementById('zone-filter-select');
    const zoneVal = zoneFilterEl ? zoneFilterEl.value : '';
    if (zoneVal) {
      currentTickets = currentTickets.filter(t => 
        (t.mcd_zone && t.mcd_zone.toLowerCase().includes(zoneVal.toLowerCase())) || 
        (t.ward_name && t.ward_name.toLowerCase().includes(zoneVal.toLowerCase()))
      );
    }
    renderTicketList(currentTickets);
    renderMapIncidents(currentTickets);
    renderLiteWardGrid(currentTickets);
  } catch (e) {
    console.error('Error fetching tickets:', e);
  }
}

function renderTicketList(tickets) {
  const listEl = document.getElementById('ticket-list');
  listEl.innerHTML = '';

  if (tickets.length === 0) {
    listEl.innerHTML = '<div style="padding: 1.5rem; text-align: center; color: var(--text-muted);">No incidents found for this filter.</div>';
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

    const janSunwaiTag = t.jan_sunwai_status === 'ESCALATED'
      ? `<span class="badge badge-jan-sunwai">⚖️ Jan Sunwai Docket</span>`
      : '';

    const missionTag = t.national_mission
      ? `<span class="badge badge-mission">${t.national_mission.split('/')[0].trim()}</span>`
      : '';

    const corporatorName = t.corporator && t.corporator.name ? t.corporator.name : 'Ward Councillor';

    card.innerHTML = `
      <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 6px; gap: 6px; flex-wrap: wrap;">
        <div style="display: flex; gap: 4px; flex-wrap: wrap; align-items: center;">
          <span class="badge ${badgeClass}">${t.urgency}</span>
          ${janSunwaiTag}
          ${missionTag}
        </div>
        <span class="badge-count">${t.report_count} reports</span>
      </div>
      <div style="font-weight: 600; font-size: 0.92rem; margin-bottom: 4px; color: var(--text-main);">${t.title}</div>
      <div style="font-size: 0.75rem; color: var(--text-muted); margin-bottom: 6px;">
        📍 ${t.ward_name} &bull; 🏛️ ${corporatorName}
      </div>
      <div style="display: flex; justify-content: space-between; font-size: 0.75rem; color: #93c5fd;">
        <span>Status: <strong>${t.status}</strong></span>
        ${t.is_sla_breached || t.sla_hours_remaining <= 0
          ? `<span style="color: #ef4444; font-weight: bold;">⚠️ SLA: Overdue (${t.sla_hours_remaining}h)</span>`
          : `<span>⏱️ SLA: <strong>${t.sla_hours_remaining}h</strong></span>`
        }
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
  document.getElementById('modal-sla').innerText = ticket.is_sla_breached
    ? `⚠️ Overdue / Breached! (${ticket.sla_hours_remaining}h remaining of ${ticket.citizen_charter_sla_hours || 48}h Citizen Charter)`
    : `${ticket.sla_hours_remaining} hours remaining (${ticket.citizen_charter_sla_hours || 48}h Citizen Charter)`;
  document.getElementById('modal-report-count').innerText = ticket.report_count;

  // National Mission & Jan Sunwai
  document.getElementById('modal-mission').innerText = ticket.national_mission || "Swachh Bharat / AMRUT Urban Mission";
  const janTag = document.getElementById('modal-jan-sunwai-tag');
  const janBtn = document.getElementById('modal-btn-jan-sunwai');
  if (ticket.jan_sunwai_status === 'ESCALATED') {
    janTag.style.display = 'inline-block';
    janBtn.disabled = true;
    janBtn.innerText = '⚖️ Already Docketed in Jan Sunwai';
    janBtn.style.opacity = '0.6';
  } else {
    janTag.style.display = 'none';
    janBtn.disabled = false;
    janBtn.innerText = '⚖️ Docket for Friday Jan Sunwai';
    janBtn.style.opacity = '1';
  }

  // Representative details
  const corp = ticket.corporator || {};
  const mla = ticket.mla || {};
  document.getElementById('modal-corporator').innerText = corp.name ? `${corp.name} (${corp.phone || 'N/A'})` : 'Ward Councillor';
  document.getElementById('modal-mla').innerText = mla.name ? `${mla.name} (${mla.constituency || 'Constituency'})` : 'Constituency MLA';

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
        <span>Channel: <strong>${r.channel}</strong></span>
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
      loadWardGovernanceData();
    }
  } catch (e) {
    console.error('Error updating status:', e);
  }
}

async function escalateModalToJanSunwai() {
  if (!selectedTicketId) return;
  try {
    const res = await fetch(`/api/v1/master-tickets/${selectedTicketId}/escalate-jan-sunwai`, {
      method: 'POST'
    });
    if (res.ok) {
      const data = await res.json();
      alert(`Docketed! ${data.message}`);
      closeModal();
      loadMasterTickets();
      loadKPIStats();
      loadWardGovernanceData();
    }
  } catch (e) {
    console.error('Error escalating to Jan Sunwai:', e);
  }
}

// Load Predictive Data & Monsoon Risk
async function loadPredictiveData() {
  try {
    const riskRes = await fetch('/api/v1/predictive-maintenance/ward-risk');
    const assetRes = await fetch('/api/v1/predictive-maintenance/assets');

    if (riskRes.ok) {
      const wards = await riskRes.json();
      allWardsData = wards;
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

    const desiltingPct = w.desilting_readiness_pct || 75;

    card.innerHTML = `
      <div style="display: flex; justify-content: space-between; align-items: center;">
        <h3 style="font-size: 1.05rem; color: var(--text-main);">${w.ward_name}</h3>
        <span class="risk-score-pill" style="${pillStyle}">${w.risk_score}</span>
      </div>
      <div style="font-size: 0.78rem; color: var(--text-muted);">
        🌧️ 48h Rain Forecast: <strong>${w.rainfall_forecast_48h_mm} mm</strong> &bull; Drainage Deficit: <strong>${w.drainage_vulnerability_score}%</strong>
      </div>
      <div>
        <div style="display: flex; justify-content: space-between; font-size: 0.72rem; margin-bottom: 2px;">
          <span>Pre-Monsoon Desilting Readiness</span>
          <strong>${desiltingPct}%</strong>
        </div>
        <div class="progress-bar">
          <div class="progress-fill" style="width: ${desiltingPct}%; background: ${desiltingPct < 60 ? '#ef4444' : '#10b981'};"></div>
        </div>
      </div>
      <div style="font-size: 0.78rem; background: #0f172a; padding: 8px; border-radius: 4px; border-left: 3px solid #3b82f6;">
        <strong>Root Cause:</strong> ${w.primary_risk_factor}
      </div>
      <div style="font-size: 0.78rem; color: #93c5fd;">
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

// Load Ward Governance & Jan Sunwai Dashboard
async function loadWardGovernanceData() {
  try {
    const [wardRes, ticketRes] = await Promise.all([
      fetch('/api/v1/predictive-maintenance/ward-risk'),
      fetch('/api/v1/master-tickets?jan_sunwai_only=true')
    ]);

    if (wardRes.ok) {
      const wards = await wardRes.json();
      renderWardGovernanceCards(wards);
    }

    if (ticketRes.ok) {
      const janTickets = await ticketRes.json();
      renderJanSunwaiTable(janTickets);
    }
  } catch (err) {
    console.error('Error loading Ward Governance data:', err);
  }
}

function renderWardGovernanceCards(wards) {
  const container = document.getElementById('ward-governance-cards');
  if (!container) return;
  container.innerHTML = '';

  wards.forEach(w => {
    const corp = w.corporator || { name: 'Ward Councillor', designation: 'Parshad', phone: '+91-98450-XXXXX' };
    const desiltingPct = w.desilting_readiness_pct || 75;
    const schedule = w.ward_sabha_schedule || 'Every 1st Saturday, 10:30 AM';

    const card = document.createElement('div');
    card.className = 'ward-gov-card';
    card.innerHTML = `
      <div style="display: flex; justify-content: space-between; align-items: flex-start;">
        <div>
          <h3 style="font-size: 1.05rem; color: #60a5fa;">${w.ward_name}</h3>
          <span style="font-size: 0.75rem; color: var(--text-muted);">${w.ward_id} &bull; Bangalore ULB</span>
        </div>
        <span class="badge badge-low">Active Council</span>
      </div>

      <div style="background: #0f172a; padding: 10px; border-radius: 6px; font-size: 0.8rem; display: flex; flex-direction: column; gap: 4px;">
        <div>🏛️ <strong>Corporator:</strong> ${corp.name} (${corp.designation || 'Parshad'})</div>
        <div>📞 <strong>Helpline:</strong> <a href="tel:${corp.phone}" style="color: #38bdf8; text-decoration: none;">${corp.phone || 'N/A'}</a></div>
        <div>🗓️ <strong>Ward Sabha:</strong> ${schedule}</div>
      </div>

      <div>
        <div style="display: flex; justify-content: space-between; font-size: 0.75rem; margin-bottom: 4px;">
          <span>Pre-Monsoon Desilting Progress</span>
          <strong>${desiltingPct}%</strong>
        </div>
        <div class="progress-bar">
          <div class="progress-fill" style="width: ${desiltingPct}%; background: ${desiltingPct < 60 ? '#ef4444' : '#10b981'};"></div>
        </div>
      </div>
    `;
    container.appendChild(card);
  });
}

function renderJanSunwaiTable(tickets) {
  const tbody = document.getElementById('jan-sunwai-table-body');
  const badgeTotal = document.getElementById('jan-sunwai-badge-total');
  if (!tbody) return;
  tbody.innerHTML = '';

  if (badgeTotal) badgeTotal.innerText = `${tickets.length} Docketed Cases`;

  if (tickets.length === 0) {
    tbody.innerHTML = '<tr><td colspan="7" style="padding: 1.5rem; text-align: center; color: var(--text-muted);">No grievances currently escalated to Jan Sunwai.</td></tr>';
    return;
  }

  tickets.forEach(t => {
    const tr = document.createElement('tr');
    tr.style.borderBottom = '1px solid var(--border)';
    const corpName = t.corporator && t.corporator.name ? t.corporator.name : 'Ward Officer';

    tr.innerHTML = `
      <td style="padding: 8px; font-weight: bold; color: #f87171;">${t.master_ticket_id}</td>
      <td style="padding: 8px; font-weight: 600;">${t.title}</td>
      <td style="padding: 8px; font-size: 0.78rem;">${t.ward_name}<br><span style="color: #94a3b8;">${corpName}</span></td>
      <td style="padding: 8px;"><span class="badge badge-mission">${t.national_mission || 'Civic Mission'}</span></td>
      <td style="padding: 8px; text-align: center;"><span class="badge-count">${t.report_count}</span></td>
      <td style="padding: 8px; font-weight: bold; color: #fb923c;">${t.sla_hours_remaining}h left</td>
      <td style="padding: 8px;">
        <button class="btn-primary" style="font-size: 0.75rem; padding: 4px 8px;" onclick="openTicketModal('${t.master_ticket_id}')">Inspect</button>
      </td>
    `;
    tbody.appendChild(tr);
  });
}

// 2G Lite Data Mode Toggle & Grid Rendering
function toggleLiteMode() {
  document.body.classList.toggle('lite-data-mode');
  const isLite = document.body.classList.contains('lite-data-mode');
  localStorage.setItem('civicsense_lite', isLite ? 'true' : 'false');
  const btn = document.getElementById('btn-lite-toggle');
  if (btn) btn.innerText = isLite ? "📶 Lite Mode ON" : "📶 2G Lite Data";
  renderLiteWardGrid(currentTickets);
}

function renderLiteWardGrid(tickets) {
  const container = document.getElementById('lite-wards-container');
  if (!container) return;
  container.innerHTML = '';

  const wardGroups = {};
  tickets.forEach(t => {
    wardGroups[t.ward_name] = wardGroups[t.ward_name] || [];
    wardGroups[t.ward_name].push(t);
  });

  Object.keys(wardGroups).forEach(wardName => {
    const items = wardGroups[wardName];
    const el = document.createElement('div');
    el.style.background = '#1e293b';
    el.style.border = '1px solid var(--border)';
    el.style.borderRadius = '6px';
    el.style.padding = '10px';

    el.innerHTML = `
      <div style="font-weight: bold; color: #60a5fa; margin-bottom: 4px;">${wardName}</div>
      <div style="font-size: 0.75rem; color: #cbd5e1;">Active Master Incidents: <strong>${items.length}</strong></div>
      <div style="font-size: 0.75rem; color: #f87171;">Critical / High: <strong>${items.filter(i => i.urgency === 'Critical' || i.urgency === 'High').length}</strong></div>
    `;
    container.appendChild(el);
  });
}

// Outdoor Sunlight Readability Mode Toggle
function toggleSunlightMode() {
  document.body.classList.toggle('sunlight-mode');
  const isSunlight = document.body.classList.contains('sunlight-mode');
  localStorage.setItem('civicsense_sunlight', isSunlight ? 'true' : 'false');
  updateSunlightButtonText();
}

function updateSunlightButtonText() {
  const btn = document.getElementById('btn-sunlight-toggle');
  if (!btn) return;
  const isSunlight = document.body.classList.contains('sunlight-mode');
  btn.innerText = isSunlight ? "🌙 Indoor / Dark Mode" : "☀️ Outdoor Sunlight Mode";
}

// Vernacular Audio / Speech-to-Text Grievance Simulation
function toggleVoiceRecording() {
  const btnLabel = document.getElementById('voice-btn-label');
  const statusLabel = document.getElementById('voice-status-label');
  const recordBtn = document.getElementById('voice-record-btn');
  const langSelect = document.getElementById('voice-lang-select');
  const chosenLang = langSelect ? langSelect.value : 'hi-IN';

  if (!isRecording) {
    isRecording = true;
    recordBtn.classList.add('voice-btn-pulse');
    recordBtn.style.background = '#dc2626';
    btnLabel.innerText = "Listening...";
    statusLabel.innerText = `Recording speech in ${chosenLang} (speak now)...`;

    // Attempt browser Web Speech API if supported
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (SpeechRecognition) {
      try {
        speechRecognizer = new SpeechRecognition();
        speechRecognizer.lang = chosenLang;
        speechRecognizer.continuous = false;
        speechRecognizer.interimResults = false;

        speechRecognizer.onresult = (event) => {
          const transcript = event.results[0][0].transcript;
          document.getElementById('complaint-text').value = transcript;
          statusLabel.innerText = `Transcribed: "${transcript}"`;
          stopRecordingUI();
        };

        speechRecognizer.onerror = () => {
          simulateVernacularVoice(chosenLang);
        };

        speechRecognizer.start();
        return;
      } catch (e) {
        // Fall through to simulation
      }
    }

    // High fidelity vernacular speech-to-text simulation fallback
    setTimeout(() => {
      simulateVernacularVoice(chosenLang);
    }, 2000);
  } else {
    stopRecordingUI();
  }
}

function stopRecordingUI() {
  isRecording = false;
  const recordBtn = document.getElementById('voice-record-btn');
  const btnLabel = document.getElementById('voice-btn-label');
  if (recordBtn) {
    recordBtn.classList.remove('voice-btn-pulse');
    recordBtn.style.background = '#2563eb';
  }
  if (btnLabel) btnLabel.innerText = "Start Speaking";
  if (speechRecognizer) {
    try { speechRecognizer.stop(); } catch(e) {}
  }
}

let lastInputSource = 'text';
let lastSpokenLanguage = 'hi-IN';

function simulateVernacularVoice(lang) {
  lastInputSource = 'voice';
  lastSpokenLanguage = lang;
  const sampleMap = {
    'hi-IN': "सड़क पर गहरा गड्ढा है, 27th मेन रोड के पास, कभी भी दुर्घटना हो सकती है, वार्ड 3",
    'kn-IN': "ರಸ್ತೆಯಲ್ಲಿ ದೊಡ್ಡ ಗುಂಡಿ ಬಿದ್ದಿದೆ, ವಾಹನ ಸವಾರರಿಗೆ ಅಪಘಾತವಾಗುವ ಸಂಭವವಿದೆ ಬೇಗ ಸರಿಮಾಡಿ, ವಾರ್ಡ್ 3",
    'ta-IN': "தெரு விளக்கு 4 நாட்களாக எரியவில்லை, இரவு நேரத்தில் மிகவும் இருட்டாக உள்ளது, வார்டு 1",
    'hinglish': "Bhaiya road par street light 4 din se band hai, near Sharma General Store, Ward 1",
    'en-IN': "Dangerous open transformer sparking near school entrance, Ward 1"
  };

  const text = sampleMap[lang] || sampleMap['hinglish'];
  document.getElementById('complaint-text').value = text;
  const statusLabel = document.getElementById('voice-status-label');
  if (statusLabel) {
    statusLabel.innerHTML = `✓ Voice transcribed (${lang}): <em>"${text}"</em>`;
  }
  stopRecordingUI();
}

function fillSampleGrievance(langKey) {
  lastInputSource = 'voice';
  lastSpokenLanguage = langKey === 'hi' ? 'hi-IN' : (langKey === 'kn' ? 'kn-IN' : (langKey === 'ta' ? 'ta-IN' : (langKey === 'hg' ? 'hinglish' : 'en-IN')));
  const samples = {
    hi: "सड़क पर गहरा गड्ढा है, 27th मेन रोड के पास, कभी भी दुर्घटना हो सकती है, वार्ड 3",
    kn: "ರಸ್ತೆಯಲ್ಲಿ ದೊಡ್ಡ ಗುಂಡಿ ಬಿದ್ದಿದೆ, ವಾಹನ ಸವಾರರಿಗೆ ಅಪಘಾತವಾಗುವ ಸಂಭವವಿದೆ ಬೇಗ ಸರಿಮಾಡಿ, ವಾರ್ಡ್ 3",
    ta: "தெரு விளக்கு 4 நாட்களாக எரியவில்லை, இரவு நேரத்தில் மிகவும் இருட்டாக உள்ளது, வார்டு 1",
    hg: "Bhaiya road par street light 4 din se band hai, near Sharma General Store, Ward 1",
    en: "Sewer pipeline leakage and dirty water overflowing on main road, Ward 2"
  };
  const text = samples[langKey] || samples.en;
  document.getElementById('complaint-text').value = text;
  const statusLabel = document.getElementById('voice-status-label');
  if (statusLabel) {
    statusLabel.innerHTML = `Selected sample (${langKey}): <em>"${text}"</em>`;
  }
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
  resultContainer.innerHTML = '<div style="color: #60a5fa;">Submitting to AI Pipeline (Multilingual NLP + Vision Verification + Deduplication)...</div>';

  try {
    let endpoint = '/api/v1/complaints/submit';
    let reqBody = {
      raw_text: text,
      lat: lat,
      lon: lon,
      citizen_name: citizenName,
      citizen_phone: citizenPhone,
      image_category_hint: imageHint || null
    };

    if (lastInputSource === 'voice' && !imageHint) {
      endpoint = '/api/v1/complaints/voice-note';
      reqBody = {
        spoken_language: lastSpokenLanguage || 'hi-IN',
        audio_transcript: text,
        lat: lat,
        lon: lon,
        citizen_name: citizenName,
        citizen_phone: citizenPhone
      };
    }

    const res = await fetch(endpoint, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(reqBody)
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

      const janBadge = data.jan_sunwai_eligible
        ? `<span class="badge badge-jan-sunwai">⚖️ Eligible for Jan Sunwai Review</span>`
        : '';

      resultContainer.innerHTML = `
        <div style="font-weight: bold; color: #34d399; margin-bottom: 6px;">
          ✓ Grievance Processed Successfully!
        </div>
        <div><strong>Assigned Ticket:</strong> ${data.master_ticket_id}</div>
        <div><strong>Department:</strong> ${data.department} (${data.issue_type})</div>
        <div><strong>National Mission:</strong> ${data.national_mission || 'Swachh Bharat / AMRUT'}</div>
        <div><strong>Ward & Corporator:</strong> ${data.ward_extracted} (${data.corporator_name || 'Ward Parshad'})</div>
        <div><strong>Urgency:</strong> ${data.urgency} | <strong>Language:</strong> ${data.language_detected}</div>
        <div style="margin-top: 6px; display: flex; gap: 6px; flex-wrap: wrap;">
          ${isDup
            ? '<span class="badge badge-high">Duplicate Merged: Linked to existing neighborhood master ticket</span>'
            : '<span class="badge badge-low">Unique Incident: New Master Ticket Created</span>'
          }
          ${visionBadge}
          ${janBadge}
        </div>
      `;

      loadMasterTickets();
      loadKPIStats();
      loadWardGovernanceData();
    } else {
      resultContainer.innerHTML = '<div style="color: #ef4444;">Failed to submit grievance. Please try again.</div>';
    }
  } catch (err) {
    resultContainer.innerHTML = `<div style="color: #ef4444;">Network error: ${err.message}</div>`;
  }
}

function detectLocation() {
  const coords = [
    { lat: 28.6514, lon: 77.1907 }, // Karol Bagh
    { lat: 28.7166, lon: 77.1189 }, // Rohini
    { lat: 28.6814, lon: 77.2228 }, // Civil Lines
    { lat: 28.6506, lon: 77.2303 }, // City-SP
    { lat: 28.5494, lon: 77.2001 }, // South
    { lat: 28.6415, lon: 77.1209 }, // West
    { lat: 12.9352, lon: 77.6245 }, // Koramangala
    { lat: 12.9716, lon: 77.6412 }  // Indiranagar
  ];
  const chosen = coords[Math.floor(Math.random() * coords.length)];
  document.getElementById('form-lat').value = chosen.lat;
  document.getElementById('form-lon').value = chosen.lon;
}

function setLocationCoords(lat, lon) {
  const latEl = document.getElementById('form-lat');
  const lonEl = document.getElementById('form-lon');
  if (latEl && lonEl) {
    latEl.value = lat;
    lonEl.value = lon;
  }
}

// 12 MCD Zones Selector Change
function onZoneSelectChange(zone) {
  const zoneDropdown = document.getElementById('mcd-zone-dropdown');
  if (zoneDropdown && zone !== zoneDropdown.value) {
    zoneDropdown.value = zone;
  }

  const zoneFilterSelect = document.getElementById('zone-filter-select');
  if (zoneFilterSelect) {
    zoneFilterSelect.value = (zone === 'ALL' ? '' : zone);
  }

  // Reload tickets filtered by zone
  loadMasterTickets();

  // Highlight or center map if coordinates exist
  const zoneCoords = {
    'City-SP': [28.6506, 77.2303],
    'Karol Bagh': [28.6514, 77.1907],
    'Civil Lines': [28.6814, 77.2228],
    'Keshav Puram': [28.6942, 77.1642],
    'Rohini': [28.7166, 77.1189],
    'Narela': [28.8527, 77.0924],
    'Najafgarh': [28.5921, 77.0460],
    'West': [28.6415, 77.1209],
    'South': [28.5494, 77.2001],
    'Central': [28.5700, 77.2400],
    'Shahdara South': [28.6300, 77.2770],
    'Shahdara North': [28.6750, 77.2750]
  };

  if (zone in zoneCoords && typeof map !== 'undefined' && map) {
    const [cLat, cLon] = zoneCoords[zone];
    map.setView([cLat, cLon], 13);
  }
}

// Fast Application / Grievance Tracker
async function trackApplication(customId) {
  const inputEl = document.getElementById('track-id-input');
  const trackId = (customId || (inputEl ? inputEl.value.trim() : '')).trim();

  if (!trackId) {
    alert('Please enter a valid Tracking ID (e.g. CMP-xxxx or MST-xxxx).');
    return;
  }

  const resultContainer = document.getElementById('quick-track-result');
  if (resultContainer) {
    resultContainer.style.display = 'block';
    resultContainer.innerHTML = '<span style="color: #60a5fa;">Searching MCD databases & multi-agent records...</span>';
  }

  try {
    const res = await fetch(`/api/v1/tracking/${encodeURIComponent(trackId)}`);
    if (!res.ok) {
      if (resultContainer) {
        resultContainer.innerHTML = `<span style="color: #ef4444;">❌ No record found for Tracking ID '${trackId}'. Please verify the ID.</span>`;
      }
      return;
    }

    const data = await res.json();

    if (resultContainer) {
      resultContainer.innerHTML = `
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
          <strong style="color: #fef08a;">${data.tracking_id}</strong>
          <span class="badge ${data.status === 'RESOLVED' ? 'badge-low' : 'badge-high'}">${data.status}</span>
        </div>
        <div style="color: #cbd5e1; margin-bottom: 4px;"><strong>${data.title}</strong></div>
        <div style="font-size: 0.75rem; color: #94a3b8; margin-bottom: 6px;">
          📍 ${data.mcd_zone || 'Delhi Zone'} &bull; Ward: ${data.ward_name} &bull; Engineer: ${data.assigned_engineer}
        </div>
        <div style="display: flex; justify-content: space-between; align-items: center;">
          <span style="font-size: 0.72rem; color: #60a5fa;">⏱️ SLA Remaining: <strong>${data.sla_hours_remaining} Hours</strong></span>
          <button class="btn-primary" style="padding: 3px 8px; font-size: 0.72rem;" onclick="openTrackingModalDirectly('${data.tracking_id}')">View Full Dossier</button>
        </div>
      `;
    }

    openTrackingModalWithData(data);
  } catch (err) {
    if (resultContainer) {
      resultContainer.innerHTML = `<span style="color: #ef4444;">Network error: ${err.message}</span>`;
    }
  }
}

function quickTrackDemo(id) {
  const inputEl = document.getElementById('track-id-input');
  if (inputEl) inputEl.value = id;
  trackApplication(id);
}

function openTrackingModalWithData(data) {
  const modal = document.getElementById('tracking-modal');
  if (!modal) return;

  document.getElementById('track-modal-id').innerText = `${data.tracking_id} (${data.type.toUpperCase()})`;

  const modalBody = document.getElementById('track-modal-body');
  
  let agentStepsHtml = '';
  if (data.agent_trace && data.agent_trace.length > 0) {
    agentStepsHtml = data.agent_trace.map((step, idx) => `
      <div style="background: rgba(15, 23, 42, 0.7); border-left: 3px solid #38bdf8; padding: 6px 10px; margin-bottom: 6px; border-radius: 0 4px 4px 0; font-size: 0.76rem;">
        <div style="display: flex; justify-content: space-between; color: #60a5fa; font-weight: bold;">
          <span>${step.agent_name}</span>
          <span style="color: #34d399;">${step.status}</span>
        </div>
        <div style="color: #e2e8f0; margin-top: 2px;">${step.thought_log}</div>
        <div style="color: #94a3b8; font-size: 0.7rem; margin-top: 2px;">Action: ${step.action_taken}</div>
      </div>
    `).join('');
  } else {
    agentStepsHtml = '<div style="color: var(--text-muted); font-style: italic;">Standard pipeline routing active.</div>';
  }

  const corpName = data.corporator && data.corporator.name ? data.corporator.name : 'Ward Parshad';

  modalBody.innerHTML = `
    <div style="background: #0f172a; border: 1px solid var(--border); border-radius: 6px; padding: 1rem; margin-bottom: 1rem; font-size: 0.82rem;">
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
        <h4 style="margin: 0; color: #ffffff; font-size: 1rem;">${data.title}</h4>
        <span class="badge ${data.status === 'RESOLVED' ? 'badge-low' : 'badge-high'}">${data.status}</span>
      </div>
      <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px; color: #cbd5e1;">
        <div><strong>Department:</strong> ${data.department}</div>
        <div><strong>Urgency:</strong> ${data.urgency}</div>
        <div><strong>MCD Zone:</strong> ${data.mcd_zone || 'MCD Zone'}</div>
        <div><strong>Ward:</strong> ${data.ward_name}</div>
        <div><strong>Assigned Officer:</strong> ${data.assigned_engineer}</div>
        <div><strong>Parshad / Corporator:</strong> ${corpName}</div>
        <div><strong>Jan Sunwai Status:</strong> ${data.jan_sunwai_status}</div>
        <div><strong>Citizen Charter SLA:</strong> ${data.sla_hours_remaining}h remaining</div>
      </div>
    </div>

    <h4 style="margin-bottom: 0.5rem; font-size: 0.9rem; color: #38bdf8;">Autonomous AI Agent Deliberation Trail:</h4>
    <div style="max-height: 240px; overflow-y: auto; padding-right: 4px;">
      ${agentStepsHtml}
    </div>

    <div style="margin-top: 1rem; text-align: right;">
      <button class="btn-primary" onclick="closeTrackingModal()">Close Dossier</button>
    </div>
  `;

  modal.classList.add('active');
}

async function openTrackingModalDirectly(trackingId) {
  try {
    const res = await fetch(`/api/v1/tracking/${encodeURIComponent(trackingId)}`);
    if (res.ok) {
      const data = await res.json();
      openTrackingModalWithData(data);
    }
  } catch (e) {
    console.error(e);
  }
}

function closeTrackingModal(e) {
  if (e && e.target !== e.currentTarget && e.target.tagName !== 'BUTTON') return;
  const modal = document.getElementById('tracking-modal');
  if (modal) modal.classList.remove('active');
}

// Multi-Agent Scenario Simulator
async function simulateAgentScenario(scenarioName) {
  switchTab('agent-view');
  const consoleEl = document.getElementById('deliberation-console');
  const statusEl = document.getElementById('sim-status-indicator');

  if (statusEl) {
    statusEl.innerText = `Orchestrating scenario '${scenarioName}'...`;
    statusEl.style.color = '#f59e0b';
  }

  if (consoleEl) {
    consoleEl.innerHTML = `
      <div style="color: #60a5fa; font-weight: bold; margin-bottom: 8px;">
        &gt; INITIATING 6-AGENT COGNITIVE ORCHESTRATION PIPELINE [SCENARIO: ${scenarioName.toUpperCase()}]...
      </div>
    `;
  }

  try {
    const res = await fetch('/api/v1/agents/simulate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ scenario: scenarioName })
    });

    if (!res.ok) {
      if (consoleEl) consoleEl.innerHTML += '<div style="color: #ef4444;">Failed to run scenario simulation.</div>';
      return;
    }

    const data = await res.json();

    if (consoleEl && data.agent_trace) {
      // Step-by-step animated rendering
      let delay = 0;
      data.agent_trace.forEach((step, idx) => {
        setTimeout(() => {
          const stepDiv = document.createElement('div');
          const isAlert = step.status.includes('FLAGGED') || step.status.includes('ALERT') || step.status.includes('ESCALATED');
          const isVerified = step.status.includes('VERIFIED') || step.status.includes('SUCCESS');
          stepDiv.className = `deliberation-step ${isAlert ? 'alert' : (isVerified ? 'verified' : '')}`;

          stepDiv.innerHTML = `
            <div class="step-header">
              <span>Step ${idx + 1}: ${step.agent_name}</span>
              <span class="badge ${isAlert ? 'badge-critical' : 'badge-low'}">${step.status}</span>
            </div>
            <div class="step-thought">&gt; ${step.thought_log}</div>
            <div class="step-action">Action: ${step.action_taken} &bull; Confidence: ${(step.confidence * 100).toFixed(1)}%</div>
          `;
          consoleEl.appendChild(stepDiv);
          consoleEl.scrollTop = consoleEl.scrollHeight;

          // If last step completed
          if (idx === data.agent_trace.length - 1) {
            const summaryDiv = document.createElement('div');
            summaryDiv.style.marginTop = '10px';
            summaryDiv.style.padding = '10px';
            summaryDiv.style.background = 'rgba(56, 189, 248, 0.1)';
            summaryDiv.style.border = '1px solid #38bdf8';
            summaryDiv.style.borderRadius = '6px';
            summaryDiv.innerHTML = `
              <div style="font-weight: bold; color: #fef08a; margin-bottom: 4px;">Executive Multi-Agent Summary:</div>
              <div style="color: #f8fafc; font-size: 0.8rem; line-height: 1.4;">${data.narrative_summary}</div>
            `;
            consoleEl.appendChild(summaryDiv);
            consoleEl.scrollTop = consoleEl.scrollHeight;

            if (statusEl) {
              statusEl.innerText = 'Orchestration Completed Successfully';
              statusEl.style.color = '#34d399';
            }
          }
        }, delay);
        delay += 350;
      });
    }
  } catch (err) {
    if (consoleEl) {
      consoleEl.innerHTML += `<div style="color: #ef4444;">Error: ${err.message}</div>`;
    }
  }
}

// Refresh Agent Manifest
async function loadAgentStatus() {
  try {
    const res = await fetch('/api/v1/agents/status');
    if (!res.ok) return;
    const agents = await res.json();
    console.log('Operational Agents Manifest:', agents);
  } catch (e) {
    console.warn('Failed to load agent status:', e);
  }
}

// Official MCD Services Information Modal / Prompt
function openServiceInfo(serviceKey) {
  const serviceDetails = {
    birth_death: {
      title: "Civil Registration System (CRS Delhi) - Birth & Death Registration",
      body: "Institutional and home births/deaths within the jurisdiction of the 12 MCD zones can be registered online within 21 days with no government fee. Digitize existing paper records, download verifiable QR certificates, or apply for corrections through the Delhi CRS gateway."
    },
    property_tax: {
      title: "MCD Online Property Tax (PTR) & Mutation Gateway",
      body: "Compute property tax under Unit Area Method with geo-tagging validation. Access the 2026 Amnesty Rebate Scheme, view UPIC ownership dossiers, generate tax receipts, or apply for official property mutation."
    },
    trade_license: {
      title: "MCD Single Window Factory & Trade Licensing",
      body: "Issue and auto-renew General Trade, Health, Factory, and Veterinary trade licenses under the Ease of Doing Business framework with statutory e-SLA turnaround."
    },
    building_plan: {
      title: "Online Building Plan Sanction (OBPS Delhi)",
      body: "Submit architectural drawings, obtain structural stability scrutiny, and track sanction orders online with zero physical contact."
    },
    community_hall: {
      title: "MCD Barat Ghar & Community Hall Online Booking",
      body: "Reserve air-conditioned Barat Ghars, community centers, and municipal parks across all 12 zones with real-time slot availability."
    }
  };

  const s = serviceDetails[serviceKey];
  if (s) {
    alert(`${s.title}\n\n${s.body}\n\n(Official link enabled for citizens of NCT of Delhi)`);
  }
}

// Accessibility Controls: Font Resizer
let currentFontSizeMultiplier = 1.0;
function changeFontSize(delta) {
  if (delta === 0) {
    currentFontSizeMultiplier = 1.0;
  } else {
    currentFontSizeMultiplier = Math.max(0.85, Math.min(1.25, currentFontSizeMultiplier + (delta * 0.08)));
  }
  document.documentElement.style.fontSize = `${currentFontSizeMultiplier * 100}%`;
}

// Accessibility Controls: High Contrast Mode
function toggleHighContrast() {
  document.body.classList.toggle('sunlight-mode');
  const isHighContrast = document.body.classList.contains('sunlight-mode');
  localStorage.setItem('civicsense_sunlight', isHighContrast ? 'true' : 'false');
}
