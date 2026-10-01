// SamAashwas (समाश्वास) - National Municipal Grievance Intelligence & Urban Care Platform
// Main Application Controller powered by CivicSense AI

let currentTickets = [];
let selectedTicketId = null;
let isRecording = false;
let speechRecognizer = null;
let allWardsData = [];
let currentSelectedCity = 'all';
let currentUser = null;
let pendingPostLoginAction = null;
let currentGalleryCategory = 'all';
let currentJanSunwaiFilter = 'ALL';
let showSpatialClusters = true;

// Supported Metros & Corporations Metadata
const CITIES_DATA = {
  all: {
    id: "all",
    name: "Pan-India",
    local_name: "अखिल भारतीय नगर सेवा",
    corporation: "PAN-INDIA",
    corporation_full: "National Municipal Care & Citizen Redressal Platform",
    emblem: "🏛️",
    lat: 20.5937,
    lon: 78.9629,
    zoom: 5,
    helplines: {
      control_room: "112 / 1916",
      water: "1916",
      sanitation: "1913 / 1533",
      power: "1912",
      medical: "108"
    },
    advisory: "24x7 Monsoon & Disaster Control Rooms operational across BBMP Bengaluru, MCD Delhi, BMC Mumbai, PMC Pune, GCC Chennai, GHMC Hyderabad, LMC Lucknow & KMC Kolkata • Primary storm drain desilting achieved 86.4% readiness • Friday Jan Sunwai active at all Zonal Offices.",
    pins: [
      { name: "Bengaluru (Indiranagar)", lat: 12.9716, lon: 77.6412 },
      { name: "Delhi (Karol Bagh)", lat: 28.6514, lon: 77.1907 },
      { name: "Mumbai (Bandra West)", lat: 19.0596, lon: 72.8295 },
      { name: "Pune (Shivajinagar)", lat: 18.5314, lon: 73.8446 }
    ]
  },
  bengaluru: {
    id: "bengaluru",
    name: "Bengaluru",
    local_name: "ಬೃಹತ್ ಬೆಂಗಳೂರು ಮಹಾನಗರ ಪಾಲಿಕೆ",
    corporation: "BBMP",
    corporation_full: "Bruhat Bengaluru Mahanagara Palike",
    emblem: "🏛️",
    lat: 12.9716,
    lon: 77.5946,
    zoom: 12,
    helplines: {
      control_room: "1533 / 080-22660000",
      water: "1916 (BWSSB)",
      sanitation: "1533 (SBM)",
      power: "1912 (BESCOM)",
      medical: "108"
    },
    advisory: "BBMP High Alert: Rajakaluve SWD desilting 88% completed in Koramangala & Bellandur corridors • Rapid Pothole Squads tarring Outer Ring Road • Friday Jan Sunwai 11:00 AM @ BBMP Head Office.",
    pins: [
      { name: "Indiranagar", lat: 12.9716, lon: 77.6412 },
      { name: "Koramangala", lat: 12.9352, lon: 77.6245 },
      { name: "HSR Layout", lat: 12.9121, lon: 77.6446 },
      { name: "Malleshwaram", lat: 13.0067, lon: 77.5694 }
    ]
  },
  delhi: {
    id: "delhi",
    name: "Delhi",
    local_name: "दिल्ली नगर निगम",
    corporation: "MCD",
    corporation_full: "Municipal Corporation of Delhi",
    emblem: "🏛️",
    lat: 28.6139,
    lon: 77.2090,
    zoom: 12,
    helplines: {
      control_room: "155305 / 1800-11-8700",
      water: "1916 (Delhi Jal Board)",
      sanitation: "155305 (MCD Sanitation)",
      power: "19123 (BSES / TPDDL)",
      medical: "108"
    },
    advisory: "MCD Flood Control Alert: 24x7 Control Rooms Activated across all 12 Administrative Zones • Minto Bridge & Pul Prahladpur heavy sumps tested • Anti-Dengue door-to-door fogging active.",
    pins: [
      { name: "Karol Bagh", lat: 28.6514, lon: 77.1907 },
      { name: "Rohini", lat: 28.7166, lon: 77.1189 },
      { name: "Civil Lines", lat: 28.6814, lon: 77.2228 },
      { name: "Chandni Chowk", lat: 28.6506, lon: 77.2303 }
    ]
  },
  mumbai: {
    id: "mumbai",
    name: "Mumbai",
    local_name: "बृहन्मुंबई महानगरपालिका",
    corporation: "BMC",
    corporation_full: "Brihanmumbai Municipal Corporation",
    emblem: "🌊",
    lat: 19.0760,
    lon: 72.8777,
    zoom: 12,
    helplines: {
      control_room: "1916 / 022-22694725",
      water: "1916 (BMC Hydraulic)",
      sanitation: "1916 (Solid Waste)",
      power: "19122 (BEST / Adani)",
      medical: "108"
    },
    advisory: "BMC High-Tide Readiness: 480 dewatering pumps positioned at Hindmata, Milan Subway & Gandhi Market • Mithi River desilting 91% complete • Ward disaster teams on standby.",
    pins: [
      { name: "Bandra West", lat: 19.0596, lon: 72.8295 },
      { name: "Andheri East", lat: 19.1136, lon: 72.8697 },
      { name: "Dadar West", lat: 19.0178, lon: 72.8478 },
      { name: "Colaba / Fort", lat: 18.9067, lon: 72.8147 }
    ]
  },
  pune: {
    id: "pune",
    name: "Pune",
    local_name: "पुणे महानगरपालिका",
    corporation: "PMC",
    corporation_full: "Pune Municipal Corporation",
    emblem: "🏰",
    lat: 18.5204,
    lon: 73.8567,
    zoom: 12,
    helplines: {
      control_room: "1800-1030-222 / 020-25501000",
      water: "020-25501100 (PMC Water)",
      sanitation: "1800-1030-222",
      power: "1912 (MSEDCL)",
      medical: "108"
    },
    advisory: "PMC Smart Care Drive: Mutha Riverfront cleaning & nullah desilting ahead of schedule • Smart LED streetlight dark spot audit in Kothrud & Viman Nagar • Friday Jan Sunwai active.",
    pins: [
      { name: "Shivajinagar", lat: 18.5314, lon: 73.8446 },
      { name: "Kothrud", lat: 18.5074, lon: 73.8077 },
      { name: "Viman Nagar", lat: 18.5679, lon: 73.9143 },
      { name: "Hadapsar", lat: 18.5089, lon: 73.9259 }
    ]
  },
  chennai: {
    id: "chennai",
    name: "Chennai",
    local_name: "பெருநகர சென்னை மாநகராட்சி",
    corporation: "GCC",
    corporation_full: "Greater Chennai Corporation",
    emblem: "🌴",
    lat: 13.0827,
    lon: 80.2707,
    zoom: 12,
    helplines: {
      control_room: "1913 / 044-25619206",
      water: "044-45674567 (CMWSSB)",
      sanitation: "1913 (Namma Chennai)",
      power: "94987-94987 (TANGEDCO)",
      medical: "108"
    },
    advisory: "Singara Chennai 2.0 Mission: Kosasthalaiyar & Kovalam basin storm drain works under continuous sensor telemetry • Namma Chennai Ward grievance response under 12 hours.",
    pins: [
      { name: "T. Nagar", lat: 13.0418, lon: 80.2341 },
      { name: "Mylapore", lat: 13.0339, lon: 80.2676 },
      { name: "Adyar", lat: 13.0012, lon: 80.2565 },
      { name: "Anna Nagar", lat: 13.0850, lon: 80.2101 }
    ]
  },
  hyderabad: {
    id: "hyderabad",
    name: "Hyderabad",
    local_name: "గ్రేటర్ హైదరాబాద్ మున్సిపల్ కార్పొరేషన్",
    corporation: "GHMC",
    corporation_full: "Greater Hyderabad Municipal Corporation",
    emblem: "🕌",
    lat: 17.3850,
    lon: 78.4867,
    zoom: 12,
    helplines: {
      control_room: "040-21111111 / 1800-599-0099",
      water: "155313 (HMWSSB)",
      sanitation: "040-21111111",
      power: "1912 (TSSPDCL)",
      medical: "108"
    },
    advisory: "GHMC Monsoon Emergency Action: Strategic Nala Development Program (SNDP) phase 2 channels cleared • Rapid Action Teams deployed across Jubilee Hills & Hitec Corridor.",
    pins: [
      { name: "Jubilee Hills", lat: 17.4319, lon: 78.4073 },
      { name: "Hitec City", lat: 17.4474, lon: 78.3762 },
      { name: "Charminar", lat: 17.3616, lon: 78.4747 },
      { name: "Secunderabad", lat: 17.4399, lon: 78.4983 }
    ]
  },
  lucknow: {
    id: "lucknow",
    name: "Lucknow",
    local_name: "लखनऊ नगर निगम",
    corporation: "LMC",
    corporation_full: "Lucknow Municipal Corporation",
    emblem: "🛕",
    lat: 26.8467,
    lon: 80.9462,
    zoom: 12,
    helplines: {
      control_room: "1533 / 0522-2622080",
      water: "0522-2623040 (Jal Sansthan)",
      sanitation: "1533 (Swachh Desk)",
      power: "1912 (MVVNL)",
      medical: "108"
    },
    advisory: "Swachh Lucknow Clean City Mission: Gomti Riverfront ecological cleanup • Door-to-door waste segregation 94% verified • Sambhav Diwas / Jan Sunwai hearings every Tuesday & Friday.",
    pins: [
      { name: "Hazratganj", lat: 26.8536, lon: 80.9452 },
      { name: "Gomti Nagar", lat: 26.8568, lon: 81.0028 },
      { name: "Alambagh", lat: 26.8184, lon: 80.9082 },
      { name: "Chowk", lat: 26.8667, lon: 80.9083 }
    ]
  },
  kolkata: {
    id: "kolkata",
    name: "Kolkata",
    local_name: "কলকাতা পৌরসংস্থা",
    corporation: "KMC",
    corporation_full: "Kolkata Municipal Corporation",
    emblem: "🌉",
    lat: 22.5726,
    lon: 88.3639,
    zoom: 12,
    helplines: {
      control_room: "155359 / 033-22861000",
      water: "033-22861212",
      sanitation: "155359",
      power: "1912 (CESC)",
      medical: "108"
    },
    advisory: "KMC Drainage & Health Alert: KEIIP dewatering sumps fully operational • Anti-dengue drone spraying active across Borough VII & VIII • Talk to Mayor Jan Sunwai active.",
    pins: [
      { name: "Park Street", lat: 22.5513, lon: 88.3526 },
      { name: "Salt Lake", lat: 22.5867, lon: 88.4178 },
      { name: "Burrabazar", lat: 22.5847, lon: 88.3582 },
      { name: "Ballygunge", lat: 22.5280, lon: 88.3659 }
    ]
  }
};

// ==========================================================================
// CITIZEN AUTHENTICATION & MERI PEHCHAN CONTROLLER
// ==========================================================================

function initAuth() {
  try {
    const saved = localStorage.getItem('civicsense_auth');
    if (saved) {
      const parsed = JSON.parse(saved);
      if (parsed && parsed.user && parsed.token) {
        currentUser = parsed;
      }
    }
  } catch (e) {
    console.warn('Error reading saved session:', e);
  }
  renderAuthHeader();
  syncFormWithUser();
  updateRewardsProfile();
}

function renderAuthHeader() {
  const container = document.getElementById('citizen-auth-widget');
  if (!container) return;

  if (currentUser && currentUser.user) {
    const u = currentUser.user;
    container.innerHTML = `
      <div class="citizen-logged-pill" title="Logged in as ${u.name} (${u.role || 'Citizen'})">
        <div class="citizen-avatar-icon">${u.avatar || '👤'}</div>
        <div>
          <div class="citizen-name-text">${u.name}</div>
          <div style="font-size: 0.65rem; color: var(--text-muted); font-weight: 700;">${u.ward || u.city || 'Citizen'}</div>
        </div>
        <span class="citizen-karma-pill">🪙 ${u.karma_points || 850}</span>
        <button class="btn-citizen-logout" onclick="logoutCitizen()" title="Log out of Citizen Session">🚪 Logout</button>
      </div>
    `;
  } else {
    container.innerHTML = `
      <button class="btn-citizen-login" onclick="openLoginModal()">
        <span>🔑</span> <span>Citizen Login</span> <span style="opacity: 0.6;">|</span> <span>मेरी पहचान</span>
      </button>
    `;
  }
}

function openLoginModal(actionCallback = null) {
  pendingPostLoginAction = actionCallback;
  const modal = document.getElementById('citizen-login-modal');
  if (modal) {
    modal.style.display = 'flex';
    const phoneStep = document.getElementById('login-phone-step');
    const otpStep = document.getElementById('login-otp-step');
    if (phoneStep) phoneStep.style.display = 'block';
    if (otpStep) otpStep.style.display = 'none';
  }
}

function closeLoginModal(event = null) {
  if (event && event.target !== document.getElementById('citizen-login-modal')) return;
  const modal = document.getElementById('citizen-login-modal');
  if (modal) modal.style.display = 'none';
  pendingPostLoginAction = null;
}

async function loginWithPreset(presetId) {
  try {
    const res = await fetch('/api/v1/auth/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ preset_id: presetId })
    });
    if (!res.ok) throw new Error('Preset login failed');
    const data = await res.json();
    setAuthenticatedUser(data.access_token, data.user);
    if (typeof showStickerToast === 'function') {
      showStickerToast(`Namaste, ${data.user.name}! Citizen profile verified.`, 'success');
    }
    const modal = document.getElementById('citizen-login-modal');
    if (modal) modal.style.display = 'none';
    executePendingAction();
  } catch (err) {
    if (typeof showStickerToast === 'function') {
      showStickerToast('Login failed: ' + err.message, 'error');
    }
  }
}

async function sendMobileOTP() {
  const phoneInput = document.getElementById('login-phone-input');
  if (!phoneInput) return;
  const phone = phoneInput.value.trim();
  if (phone.length < 10) {
    if (typeof showStickerToast === 'function') {
      showStickerToast('Please enter a valid 10-digit mobile number', 'error');
    }
    return;
  }

  try {
    const res = await fetch('/api/v1/auth/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ phone: phone })
    });
    if (!res.ok) throw new Error('Failed to send OTP');
    const data = await res.json();

    document.getElementById('login-phone-step').style.display = 'none';
    document.getElementById('login-otp-step').style.display = 'block';
    const otpInput = document.getElementById('login-otp-input');
    if (otpInput) otpInput.focus();

    if (typeof showStickerToast === 'function') {
      showStickerToast(`OTP sent to +91-${phone}! Demo code: ${data.demo_otp}`, 'info');
    }
  } catch (err) {
    if (typeof showStickerToast === 'function') {
      showStickerToast('Error sending OTP: ' + err.message, 'error');
    }
  }
}

function autoFillDemoOTP() {
  const otpInput = document.getElementById('login-otp-input');
  if (otpInput) {
    otpInput.value = '123456';
    verifyMobileOTP();
  }
}

async function verifyMobileOTP() {
  const phoneInput = document.getElementById('login-phone-input');
  const otpInput = document.getElementById('login-otp-input');
  if (!phoneInput || !otpInput) return;

  const phone = phoneInput.value.trim();
  const otp = otpInput.value.trim();

  if (otp.length !== 6) {
    if (typeof showStickerToast === 'function') {
      showStickerToast('Please enter the 6-digit OTP (use 123456)', 'error');
    }
    return;
  }

  try {
    const res = await fetch('/api/v1/auth/verify-otp', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ phone: phone, otp: otp })
    });
    if (!res.ok) {
      const errData = await res.json().catch(() => ({}));
      throw new Error(errData.detail || 'OTP verification failed');
    }
    const data = await res.json();
    setAuthenticatedUser(data.access_token, data.user);
    if (typeof showStickerToast === 'function') {
      showStickerToast(`Welcome, ${data.user.name}! Citizen account verified.`, 'success');
    }
    const modal = document.getElementById('citizen-login-modal');
    if (modal) modal.style.display = 'none';
    executePendingAction();
  } catch (err) {
    if (typeof showStickerToast === 'function') {
      showStickerToast(err.message, 'error');
    }
  }
}

function setAuthenticatedUser(token, user) {
  currentUser = { token: token, user: user };
  localStorage.setItem('civicsense_auth', JSON.stringify(currentUser));
  renderAuthHeader();
  syncFormWithUser();
  updateRewardsProfile();
}

function executePendingAction() {
  if (typeof pendingPostLoginAction === 'function') {
    const cb = pendingPostLoginAction;
    pendingPostLoginAction = null;
    cb();
  }
}

function syncFormWithUser() {
  if (currentUser && currentUser.user) {
    const nameInput = document.getElementById('citizen-name');
    const phoneInput = document.getElementById('citizen-phone');
    if (nameInput) nameInput.value = currentUser.user.name;
    if (phoneInput) phoneInput.value = currentUser.user.phone;
  }
}

function updateRewardsProfile() {
  if (currentUser && currentUser.user) {
    const u = currentUser.user;
    const nameEl = document.getElementById('reward-user-name');
    const rankEl = document.getElementById('reward-user-rank');
    const karmaEl = document.getElementById('reward-karma-points');
    if (nameEl) nameEl.innerText = u.name;
    if (rankEl) rankEl.innerText = `${u.role_title || u.role} • ${u.badge || 'Active Citizen'}`;
    if (karmaEl) karmaEl.innerText = u.karma_points || 850;
  }
}

async function logoutCitizen() {
  if (currentUser && currentUser.token) {
    try {
      await fetch('/api/v1/auth/logout', {
        method: 'POST',
        headers: { 'Authorization': `Bearer ${currentUser.token}` }
      });
    } catch (e) {
      console.warn('Logout request notice:', e);
    }
  }
  currentUser = null;
  localStorage.removeItem('civicsense_auth');
  renderAuthHeader();

  const nameInput = document.getElementById('citizen-name');
  const phoneInput = document.getElementById('citizen-phone');
  if (nameInput) nameInput.value = 'Citizen';
  if (phoneInput) phoneInput.value = '9876543210';

  if (typeof showStickerToast === 'function') {
    showStickerToast('Logged out successfully. Login anytime to file grievances.', 'info');
  }
}

function requireLogin(callback) {
  if (currentUser && currentUser.user) {
    callback();
  } else {
    openLoginModal(callback);
  }
}

function handleReportIssueClick() {
  requireLogin(() => {
    switchTab('citizen-portal');
    const txtArea = document.getElementById('complaint-text');
    if (txtArea) txtArea.focus();
  });
}

function handleGrievanceTabClick() {
  requireLogin(() => {
    switchTab('citizen-portal');
  });
}

document.addEventListener('DOMContentLoaded', () => {
  // Restore language preference
  const savedLang = localStorage.getItem('civicsense_lang') || 'en';
  if (typeof setLanguage === 'function') setLanguage(savedLang);

  // Restore sunlight mode preference
  if (localStorage.getItem('civicsense_sunlight') === 'true') {
    document.body.classList.add('sunlight-mode');
  }

  // Restore lite mode preference
  if (localStorage.getItem('civicsense_lite') === 'true') {
    document.body.classList.add('lite-data-mode');
  }

  initAuth();
  initMap();
  animateHeroCounters();
  loadKPIStats();
  loadMasterTickets();
  loadTransformations();
  loadRewards();
  loadPredictiveData();
  loadWardGovernanceData();
});

// Animate Dynamic Hero Impact Metrics Counters
function animateHeroCounters() {
  animateValue('impact-resolved-count', 17000, 18450, 1500, '+');
  animateValue('impact-active-squads', 100, 142, 1200, '');
}

function animateValue(id, start, end, duration, suffix = '') {
  const el = document.getElementById(id);
  if (!el) return;
  const range = end - start;
  const startTime = new Date().getTime();
  const timer = setInterval(() => {
    const now = new Date().getTime();
    const progress = Math.min((now - startTime) / duration, 1);
    const current = Math.floor(progress * range + start);
    el.innerText = `${current.toLocaleString('en-IN')}${suffix}`;
    if (progress >= 1) clearInterval(timer);
  }, 30);
}

// City Switcher Handler
function selectCity(cityId) {
  currentSelectedCity = cityId;
  const city = CITIES_DATA[cityId] || CITIES_DATA['all'];

  // Update active pill UI
  document.querySelectorAll('.city-pill').forEach(btn => {
    btn.classList.toggle('active', btn.getAttribute('onclick').includes(`'${cityId}'`));
  });

  // Update Header titles & emblem
  const emblemEl = document.getElementById('header-emblem-icon');
  const titleLocalEl = document.getElementById('header-corp-title-local');
  const titleEnEl = document.getElementById('header-corp-title-en');
  const subEl = document.getElementById('header-corp-subtitle');
  const tickerEl = document.getElementById('public-ticker-text');
  const badgeLiveEl = document.getElementById('hero-live-badge-text');

  if (emblemEl) emblemEl.innerText = city.emblem || "🏛️";
  if (titleLocalEl) titleLocalEl.innerText = city.local_name;
  if (titleEnEl) titleEnEl.innerText = `SamAashwas - ${city.corporation_full}`;
  if (subEl) subEl.innerText = `Powered by CivicSense AI • Autonomous Multi-Agent Deduplication, Statutory SLAs & Jan Sunwai (${city.corporation})`;
  if (tickerEl) tickerEl.innerHTML = `🚨 <strong>${city.corporation} CIVIC ADVISORY:</strong> ${city.advisory}`;
  if (badgeLiveEl) badgeLiveEl.innerText = `${city.name} Civic Grid Active • ${city.corporation} Intelligent Redressal Shield`;

  // Update Map Position
  if (typeof flyToCity === 'function') {
    flyToCity(city.lat, city.lon, city.zoom);
  }

  // Update Form Quick Pins for this city
  updateFormPins(city);

  // Update Helplines Grid
  updateHelplinesGrid(city);

  // Reload filtered tickets and data
  const cityQuery = city.id === 'all' ? '' : city.name;
  const commandCityFilter = document.getElementById('command-city-filter');
  if (commandCityFilter) {
    commandCityFilter.value = city.id === 'all' ? '' : city.name;
  }
  loadKPIStats(cityQuery);
  loadMasterTickets(cityQuery);
  loadPredictiveData(cityQuery);
  loadWardGovernanceData(cityQuery);
}

function updateFormPins(city) {
  const container = document.getElementById('form-quick-pins');
  if (!container) return;

  const pins = city.pins || CITIES_DATA['all'].pins;
  let html = `
    <button type="button" class="btn-primary" style="background: #334155; font-size: 0.8rem;" onclick="detectLocation()" data-i18n="btn_gps">
      📍 Auto-Detect GPS Location
    </button>
  `;

  pins.forEach(p => {
    html += `
      <button type="button" class="btn-secondary" style="font-size: 0.8rem;" onclick="setLocationCoords(${p.lat}, ${p.lon})">
        📍 ${p.name}
      </button>
    `;
  });

  container.innerHTML = html;

  // Set default form coordinates to first pin
  if (pins.length > 0) {
    setLocationCoords(pins[0].lat, pins[0].lon);
  }
}

function updateHelplinesGrid(city) {
  const container = document.getElementById('helpline-grid-container');
  if (!container) return;

  const h = city.helplines;
  container.innerHTML = `
    <a href="tel:112" class="helpline-card emergency">
      <div class="helpline-icon-wrap">🚨</div>
      <div>
        <div class="helpline-num">112</div>
        <div class="helpline-name">National Emergency & Police</div>
        <div class="helpline-action">Tap to Call &bull; Toll-Free</div>
      </div>
    </a>

    <a href="tel:${h.water.split(' ')[0]}" class="helpline-card water">
      <div class="helpline-icon-wrap">💧</div>
      <div>
        <div class="helpline-num">${h.water}</div>
        <div class="helpline-name">Water Supply & Pipeline Burst</div>
        <div class="helpline-action">${city.name} Water Desk</div>
      </div>
    </a>

    <a href="tel:${h.sanitation.split(' ')[0]}" class="helpline-card sanitation">
      <div class="helpline-icon-wrap">🧹</div>
      <div>
        <div class="helpline-num">${h.sanitation}</div>
        <div class="helpline-name">Municipal Sanitation & Waste</div>
        <div class="helpline-action">${city.corporation} SBM Desk</div>
      </div>
    </a>

    <a href="tel:${h.power.split(' ')[0]}" class="helpline-card power">
      <div class="helpline-icon-wrap">⚡</div>
      <div>
        <div class="helpline-num">${h.power}</div>
        <div class="helpline-name">Power Grid & Live Wire Sparks</div>
        <div class="helpline-action">Discom Control Room</div>
      </div>
    </a>

    <a href="tel:${h.medical}" class="helpline-card medical">
      <div class="helpline-icon-wrap">🚑</div>
      <div>
        <div class="helpline-num">108</div>
        <div class="helpline-name">Ambulance & Medical Emergency</div>
        <div class="helpline-action">Emergency Medical Response</div>
      </div>
    </a>
  `;
}

function onCommandCityChange(cityVal) {
  const cityKey = Object.keys(CITIES_DATA).find(k => CITIES_DATA[k].name.toLowerCase() === (cityVal || '').toLowerCase()) || 'all';
  selectCity(cityKey);
}

// Tab Switcher for Desktop & Mobile
function switchTab(tabId) {
  document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
  document.querySelectorAll('.mobile-nav-item').forEach(btn => btn.classList.remove('active'));
  document.querySelectorAll('.view-container').forEach(view => view.classList.remove('active'));

  const targetView = document.getElementById(tabId);
  if (targetView) targetView.classList.add('active');

  const desktopBtn = document.querySelector(`.tab-btn[data-tab="${tabId}"]`);
  if (desktopBtn) desktopBtn.classList.add('active');

  const mobileBtn = document.querySelector(`.mobile-nav-item[data-tab="${tabId}"]`);
  if (mobileBtn) mobileBtn.classList.add('active');

  if (tabId === 'command-center' && typeof map !== 'undefined' && map) {
    setTimeout(() => { map.invalidateSize(); }, 200);
  }

  if (tabId === 'gallery-view') loadTransformations();
  if (tabId === 'rewards-view') loadRewards();
  if (tabId === 'jan-sunwai-view') loadWardGovernanceData();
  if (tabId === 'predictive-view') loadPredictiveData();
}

// Fetch Real-time KPI Stats
async function loadKPIStats(cityFilter = '') {
  try {
    const activeCity = cityFilter || (currentSelectedCity !== 'all' ? CITIES_DATA[currentSelectedCity].name : '');
    const url = activeCity ? `/api/v1/analytics/stats?city=${encodeURIComponent(activeCity)}` : '/api/v1/analytics/stats';
    const res = await fetch(url);
    if (!res.ok) return;
    const stats = await res.json();

    const repEl = document.getElementById('kpi-total-reports');
    const masEl = document.getElementById('kpi-master-tickets');
    const dedEl = document.getElementById('kpi-dedup-rate');
    const wrkEl = document.getElementById('kpi-high-risk-wards');
    const janEl = document.getElementById('kpi-jan-sunwai-count');

    if (repEl) repEl.innerText = stats.total_complaints;
    if (masEl) masEl.innerText = stats.total_master_tickets;
    if (dedEl) dedEl.innerText = `${stats.deduplication_rate_pct}%`;
    if (wrkEl) wrkEl.innerText = stats.high_risk_wards_count;
    if (janEl) janEl.innerText = stats.jan_sunwai_escalated_count || 0;

    // Update CampusHop Squish Meter (Section 6.10)
    if (typeof updateSquishMeter === 'function' && stats.total_master_tickets !== undefined) {
      const loadPct = Math.min(95, Math.max(25, Math.round((stats.total_master_tickets / 16) * 100)));
      updateSquishMeter(loadPct);
    }
  } catch (e) {
    console.warn('Could not fetch stats:', e);
  }
}

// Load Master Tickets with Filters & City Selection
async function loadMasterTickets(cityFilter = '') {
  const statusFilterEl = document.getElementById('status-filter');
  const statusFilter = statusFilterEl ? statusFilterEl.value : '';

  let url = '/api/v1/master-tickets?';
  const params = [];
  if (statusFilter === 'JAN_SUNWAI') {
    params.push('jan_sunwai_only=true');
  } else if (statusFilter) {
    params.push(`status=${encodeURIComponent(statusFilter)}`);
  }

  const activeCity = cityFilter || (currentSelectedCity !== 'all' ? CITIES_DATA[currentSelectedCity].name : '');
  if (activeCity) {
    params.push(`city=${encodeURIComponent(activeCity)}`);
  }

  url += params.join('&');

  try {
    const res = await fetch(url);
    if (!res.ok) return;
    currentTickets = await res.json();

    renderTicketList(currentTickets);
    renderMapIncidents(currentTickets);
    renderLiteWardGrid(currentTickets);
  } catch (e) {
    console.error('Error fetching tickets:', e);
  }
}

function renderTicketList(tickets) {
  const listEl = document.getElementById('ticket-list');
  if (!listEl) return;
  listEl.innerHTML = '';

  if (tickets.length === 0) {
    listEl.innerHTML = typeof getStickerEmptyStateHTML === 'function'
      ? getStickerEmptyStateHTML('No Incidents in Queue!', 'All reported civic issues in this filter have been resolved or routed. Hop on to another ward!', 'Refresh Queue', 'loadMasterTickets()')
      : '<div style="padding: 1.5rem; text-align: center; color: var(--text-muted); font-weight: 700;">No incidents found for this filter.</div>';
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
      ? `<span class="badge badge-jan-sunwai">⚖️ Jan Sunwai</span>`
      : '';

    const missionTag = t.national_mission
      ? `<span class="badge badge-mission">${t.national_mission.split('/')[0].trim()}</span>`
      : '';

    const corporatorName = t.corporator && t.corporator.name ? t.corporator.name : 'Ward Councillor';
    const cityLabel = t.city ? `${t.city} &bull; ` : '';

    card.innerHTML = `
      <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 6px; gap: 6px; flex-wrap: wrap;">
        <div style="display: flex; gap: 4px; flex-wrap: wrap; align-items: center;">
          <span class="badge ${badgeClass}">${t.urgency}</span>
          ${janSunwaiTag}
          ${missionTag}
        </div>
        <span class="badge-count">${t.report_count} reports</span>
      </div>
      <div style="font-weight: 700; font-size: 0.9rem; margin-bottom: 4px; color: var(--text-main);">${t.title}</div>
      <div style="font-size: 0.75rem; color: var(--text-muted); margin-bottom: 6px;">
        📍 ${cityLabel}${t.ward_name} &bull; 🏛️ ${corporatorName}
      </div>
      <div style="display: flex; justify-content: space-between; font-size: 0.75rem; color: var(--ink); font-weight: 700;">
        <span>Status: <strong>${t.status}</strong></span>
        ${t.is_sla_breached || t.sla_hours_remaining <= 0
          ? `<span style="color: var(--tomato); font-weight: 900;">⚠️ SLA: Overdue</span>`
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
  document.getElementById('modal-ward').innerText = `${ticket.city || ''} - ${ticket.ward_name}`;
  document.getElementById('modal-urgency').innerText = ticket.urgency;
  document.getElementById('modal-status').innerText = ticket.status;
  document.getElementById('modal-engineer').innerText = ticket.assigned_engineer;
  document.getElementById('modal-sla').innerText = ticket.is_sla_breached
    ? `⚠️ Overdue / Breached! (${ticket.sla_hours_remaining}h remaining of ${ticket.citizen_charter_sla_hours || 48}h Citizen Charter)`
    : `${ticket.sla_hours_remaining} hours remaining (${ticket.citizen_charter_sla_hours || 48}h Citizen Charter)`;
  document.getElementById('modal-report-count').innerText = ticket.report_count;

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

  const corp = ticket.corporator || {};
  const mla = ticket.mla || {};
  document.getElementById('modal-corporator').innerText = corp.name ? `${corp.name} (${corp.phone || 'N/A'})` : 'Ward Councillor';
  document.getElementById('modal-mla').innerText = mla.name ? `${mla.name} (${mla.constituency || 'Constituency'})` : 'Constituency MLA';

  const reportsList = document.getElementById('modal-reports-list');
  reportsList.innerHTML = '';

  (ticket.citizen_reports || []).forEach((r, idx) => {
    const reportItem = document.createElement('div');
    reportItem.style.background = '#FFFDF7';
    reportItem.style.padding = '10px 14px';
    reportItem.style.borderRadius = '14px';
    reportItem.style.border = '2px solid #231F20';
    reportItem.style.boxShadow = '2px 2px 0 #231F20';
    reportItem.style.fontSize = '0.82rem';
    reportItem.style.color = '#231F20';

    reportItem.innerHTML = `
      <div style="display: flex; justify-content: space-between; color: #57534e; font-weight: 800; margin-bottom: 4px;">
        <strong>#${idx + 1} ${r.citizen_name} (${r.citizen_phone})</strong>
        <span>Channel: <strong style="color: #231F20;">${r.channel}</strong></span>
      </div>
      <div style="color: #231F20; font-style: italic; font-weight: 600;">"${r.raw_text}"</div>
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
      if (typeof showStickerToast === 'function') {
        showStickerToast(`Ticket status updated to ${newStatus}!`, 'success');
      }
      closeModal();
      loadMasterTickets();
      loadKPIStats();
      loadWardGovernanceData();
    }
  } catch (e) {
    if (typeof showStickerToast === 'function') {
      showStickerToast('Failed to update ticket status', 'error');
    }
  }
}

async function escalateModalToJanSunwai() {
  if (!selectedTicketId) return;
  try {
    const res = await fetch(`/api/v1/master-tickets/${selectedTicketId}/escalate-jan-sunwai`, {
      method: 'POST'
    });
    if (res.ok) {
      if (typeof showStickerToast === 'function') {
        showStickerToast('Incident docketed for upcoming Friday Jan Sunwai before the Municipal Commissioner.', 'success');
      }
      closeModal();
      loadMasterTickets();
      loadKPIStats();
      loadWardGovernanceData();
    }
  } catch (e) {
    if (typeof showStickerToast === 'function') {
      showStickerToast('Failed to escalate to Jan Sunwai', 'error');
    }
  }
}

// BEFORE & AFTER TRANSFORMATION GALLERY
async function loadTransformations(categoryFilter = null) {
  const container = document.getElementById('transformation-cards-container');
  if (!container) return;

  const cat = categoryFilter !== null ? categoryFilter : currentGalleryCategory;
  const url = (cat && cat !== 'all')
    ? `/api/v1/transformations?category=${encodeURIComponent(cat)}`
    : '/api/v1/transformations';

  try {
    const res = await fetch(url);
    if (!res.ok) return;
    const items = await res.json();

    container.innerHTML = '';
    if (items.length === 0) {
      container.innerHTML = '<div style="grid-column: 1/-1; text-align: center; padding: 2rem; color: var(--text-muted); font-weight: 700;">No verified transformations in this category.</div>';
      return;
    }

    items.forEach(t => {
      const card = document.createElement('div');
      card.className = 'transformation-card';
      card.innerHTML = `
        <div class="transformation-header">
          <div>
            <div class="transformation-title">${t.title}</div>
            <div class="transformation-location">📍 ${t.location} &bull; ${t.city}</div>
          </div>
          <span class="transformation-tag">${t.badge}</span>
        </div>

        <div class="before-after-container">
          <div class="ba-box before">
            <div class="ba-label">⚠️ Before Report</div>
            <div class="ba-icon">${t.before_icon}</div>
            <div class="ba-desc">${t.before_desc}</div>
          </div>
          <div class="ba-box after">
            <div class="ba-label">✅ After Redressal</div>
            <div class="ba-icon">${t.after_icon}</div>
            <div class="ba-desc">${t.after_desc}</div>
          </div>
        </div>

        <div class="transformation-footer">
          <div>
            <span>Turnaround: </span>
            <span class="turnaround-pill">⏱️ ${t.sla_turnaround_hours} Hours</span>
          </div>
          <button class="endorse-btn" onclick="endorseTransformation('${t.id}', this)">
            👍 Verified (${t.endorsements})
          </button>
        </div>
      `;
      container.appendChild(card);
    });
  } catch (e) {
    console.warn('Failed to load transformations:', e);
  }
}

function filterGallery(category) {
  currentGalleryCategory = category;
  document.querySelectorAll('.gallery-filter-btn').forEach(btn => {
    btn.classList.toggle('active', btn.getAttribute('data-cat') === category);
  });
  loadTransformations(category);
}

function endorseTransformation(id, btnEl) {
  btnEl.style.background = 'var(--mint)';
  btnEl.style.borderColor = 'var(--ink)';
  btnEl.style.color = 'var(--ink)';
  btnEl.innerText = '✅ Endorsed by You';
  btnEl.disabled = true;
  if (typeof showStickerToast === 'function') {
    showStickerToast('Thank you for verifying civic transformation!', 'success');
  }
}

// SWACHH NAGRIK COMMUNITY REWARDS & BADGES
async function loadRewards() {
  const badgesContainer = document.getElementById('rewards-badges-container');
  const perksContainer = document.getElementById('rewards-perks-container');
  if (!badgesContainer || !perksContainer) return;

  try {
    const res = await fetch('/api/v1/rewards');
    if (!res.ok) return;
    const data = await res.json();

    // Badges
    badgesContainer.innerHTML = '';
    data.badges.forEach(b => {
      const isUnlocked = b.status === 'UNLOCKED';
      const badgeCard = document.createElement('div');
      badgeCard.className = 'reward-badge-card';
      badgeCard.innerHTML = `
        <div class="badge-icon-box" style="${isUnlocked ? 'background: #E8F9F2; border-color: var(--ink);' : 'opacity: 0.5;'}">
          ${b.icon}
        </div>
        <div>
          <div style="display: flex; align-items: center; gap: 8px;">
            <div style="font-weight: 800; font-size: 0.95rem; color: var(--ink); font-family: var(--font-display);">${b.name}</div>
            <span class="badge ${isUnlocked ? 'badge-low' : 'badge-medium'}">${isUnlocked ? 'UNLOCKED' : 'IN PROGRESS'}</span>
          </div>
          <div style="font-size: 0.78rem; color: var(--text-muted); font-weight: 600; margin-top: 4px;">${b.description}</div>
          <div style="font-size: 0.72rem; color: var(--ink); font-weight: 700; margin-top: 6px;">Points Required: <strong>${b.points_req} Karma</strong></div>
        </div>
      `;
      badgesContainer.appendChild(badgeCard);
    });

    // Perks
    perksContainer.innerHTML = '';
    data.perks.forEach(p => {
      const perkCard = document.createElement('div');
      perkCard.className = 'perk-card';
      perkCard.innerHTML = `
        <div>
          <div style="font-weight: 800; font-size: 0.95rem; color: var(--ink); font-family: var(--font-display); margin-bottom: 6px;">${p.title}</div>
          <div style="font-size: 0.78rem; color: var(--text-muted); font-weight: 600; line-height: 1.45; margin-bottom: 12px;">${p.desc}</div>
        </div>
        <div style="display: flex; justify-content: space-between; align-items: center; padding-top: 10px; border-top: 1.5px dashed var(--ink);">
          <span style="font-size: 0.8rem; color: var(--ink); font-weight: 800;">🪙 ${p.points_cost} Karma Points</span>
          <button class="btn-primary" style="font-size: 0.75rem; padding: 5px 12px;" onclick="claimPerk('${p.title}', '${p.code}', '${p.desc}')">Claim Perk</button>
        </div>
      `;
      perksContainer.appendChild(perkCard);
    });
  } catch (e) {
    console.warn('Failed to load rewards:', e);
  }
}

function claimPerk(title, code, desc) {
  document.getElementById('perk-modal-title').innerText = title;
  document.getElementById('perk-modal-desc').innerText = desc;
  document.getElementById('perk-modal-code').innerText = code;
  document.getElementById('perk-modal').style.display = 'flex';
}

function closePerkModal(event) {
  if (event && event.target !== document.getElementById('perk-modal')) return;
  document.getElementById('perk-modal').style.display = 'none';
}

// PREDICTIVE RISK DATA
async function loadPredictiveData(cityFilter = '') {
  const cardsContainer = document.getElementById('ward-risk-cards');
  const tableBody = document.getElementById('assets-table-body');
  if (!cardsContainer || !tableBody) return;

  const activeCity = cityFilter || (currentSelectedCity !== 'all' ? CITIES_DATA[currentSelectedCity].name : '');
  const riskUrl = activeCity ? `/api/v1/predictive-maintenance/ward-risk?city=${encodeURIComponent(activeCity)}` : '/api/v1/predictive-maintenance/ward-risk';
  const assetsUrl = activeCity ? `/api/v1/predictive-maintenance/assets?city=${encodeURIComponent(activeCity)}` : '/api/v1/predictive-maintenance/assets';

  try {
    const [resRisk, resAssets] = await Promise.all([
      fetch(riskUrl),
      fetch(assetsUrl)
    ]);

    if (resRisk.ok) {
      const wards = await resRisk.json();
      allWardsData = wards;
      cardsContainer.innerHTML = '';
      wards.slice(0, 8).forEach(w => {
        let badgeClass = 'low';
        if (w.risk_level === 'CRITICAL') badgeClass = 'critical';
        else if (w.risk_level === 'HIGH') badgeClass = 'high';
        else if (w.risk_level === 'MEDIUM') badgeClass = 'medium';

        const card = document.createElement('div');
        card.className = 'risk-card';
        card.innerHTML = `
          <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 8px;">
            <div>
              <div style="font-weight: 800; font-size: 0.95rem; color: var(--ink); font-family: var(--font-display);">${w.ward_name}</div>
              <div style="font-size: 0.72rem; color: var(--text-muted); font-weight: 700;">${w.ward_id}</div>
            </div>
            <div class="risk-score-badge ${badgeClass}">${w.risk_score}</div>
          </div>
          <div style="font-size: 0.78rem; color: var(--ink); font-weight: 600; margin-bottom: 8px;">
            🌧️ Rain 24h: <strong>${w.rainfall_forecast_24h_mm}mm</strong> &bull; Active Issues: <strong>${w.active_complaints_count}</strong>
          </div>
          <div style="font-size: 0.74rem; color: var(--ink); background: #FFE8E5; border: 1.5px solid var(--ink); padding: 6px; border-radius: 8px; margin-bottom: 6px; font-weight: 700;">
            ⚠️ ${w.recommendation}
          </div>
          <div style="font-size: 0.72rem; color: var(--text-muted); font-weight: 700;">
            Desilting Readiness: <strong>${w.desilting_readiness_pct}%</strong>
          </div>
        `;
        cardsContainer.appendChild(card);
      });
    }

    if (resAssets.ok) {
      const assets = await resAssets.json();
      tableBody.innerHTML = '';
      assets.forEach(a => {
        const row = document.createElement('tr');
        row.style.borderBottom = '1.5px solid var(--paper-2)';
        row.innerHTML = `
          <td style="padding: 10px; font-weight: 800; color: var(--ink); font-family: var(--font-display);">${a.asset_id}</td>
          <td style="padding: 10px; font-weight: 600;">${a.type}</td>
          <td style="padding: 10px; font-weight: 600;">${a.ward_id}</td>
          <td style="padding: 10px; font-weight: 700;">${a.structural_health_score}/100</td>
          <td style="padding: 10px; font-weight: 900; color: ${a.failure_probability > 0.4 ? 'var(--tomato)' : 'var(--mint)'};">
            ${(a.failure_probability * 100).toFixed(1)}%
          </td>
          <td style="padding: 10px; font-size: 0.75rem; color: var(--ink); font-weight: 600;">${a.recommended_action}</td>
        `;
        tableBody.appendChild(row);
      });
    }
  } catch (e) {
    console.warn('Error loading predictive data:', e);
  }
}

// JAN SUNWAI & WARD GOVERNANCE
function filterJanSunwai(filterType) {
  currentJanSunwaiFilter = filterType;
  document.querySelectorAll('#jan-sunwai-view .gallery-filter-btn').forEach(btn => {
    btn.classList.remove('active');
  });
  const activeBtn = document.getElementById(`jan-filter-${filterType.toLowerCase()}`);
  if (activeBtn) activeBtn.classList.add('active');
  loadWardGovernanceData();
}

async function loadWardGovernanceData(cityFilter = '') {
  const cardsContainer = document.getElementById('ward-governance-cards');
  const tableBody = document.getElementById('jan-sunwai-table-body');
  const badgeTotal = document.getElementById('jan-sunwai-badge-total');
  if (!cardsContainer || !tableBody) return;

  const activeCity = cityFilter || (currentSelectedCity !== 'all' ? CITIES_DATA[currentSelectedCity].name : '');
  const url = activeCity
    ? `/api/v1/master-tickets?jan_sunwai_only=true&city=${encodeURIComponent(activeCity)}`
    : '/api/v1/master-tickets?jan_sunwai_only=true';

  try {
    const res = await fetch(url);
    if (!res.ok) return;
    const tickets = await res.json();

    // Filter tickets according to currentJanSunwaiFilter
    let filteredTickets = tickets;
    if (currentJanSunwaiFilter === 'CRITICAL') {
      filteredTickets = tickets.filter(t => t.urgency === 'Critical');
    } else if (currentJanSunwaiFilter === 'BREACHED') {
      filteredTickets = tickets.filter(t => t.is_sla_breached || t.sla_hours_remaining <= 0);
    }

    if (badgeTotal) badgeTotal.innerText = `${filteredTickets.length} Docketed Cases`;

    tableBody.innerHTML = '';
    if (filteredTickets.length === 0) {
      tableBody.innerHTML = '<tr><td colspan="7" style="padding: 1.5rem; text-align: center; color: var(--text-muted); font-weight: 700;">No Jan Sunwai cases matching this filter.</td></tr>';
    } else {
      filteredTickets.forEach(t => {
        const row = document.createElement('tr');
        row.style.borderBottom = '1.5px solid var(--paper-2)';
        const corpName = t.corporator && t.corporator.name ? t.corporator.name : 'Parshad';

        row.innerHTML = `
          <td style="padding: 10px; font-weight: 800; color: var(--tomato); font-family: var(--font-display);">${t.master_ticket_id}</td>
          <td style="padding: 10px; font-weight: 700; color: var(--ink);">${t.title}</td>
          <td style="padding: 10px; color: var(--ink);">${t.ward_name}<br/><span style="font-size: 0.72rem; color: var(--text-muted); font-weight: 700;">${corpName}</span></td>
          <td style="padding: 10px;"><span class="badge badge-mission">${(t.national_mission || '').split('/')[0]}</span></td>
          <td style="padding: 10px; font-weight: 800; color: var(--ink);">${t.report_count} Citizens</td>
          <td style="padding: 10px; font-weight: 700;">
            ${t.is_sla_breached ? '<span style="color: var(--tomato); font-weight: 900;">⚠️ SLA Breached</span>' : `${t.sla_hours_remaining}h rem.`}
          </td>
          <td style="padding: 10px;">
            <button class="btn-primary" style="font-size: 0.72rem; padding: 4px 10px;" onclick="openTicketModal('${t.master_ticket_id}')">Inspect</button>
          </td>
        `;
        tableBody.appendChild(row);
      });
    }

    // Populate Ward Governance representative cards
    cardsContainer.innerHTML = '';
    const uniqueWards = {};
    currentTickets.forEach(t => {
      if (!uniqueWards[t.ward_id]) {
        uniqueWards[t.ward_id] = t;
      }
    });

    Object.values(uniqueWards).slice(0, 6).forEach(w => {
      const corp = w.corporator || {};
      const mla = w.mla || {};
      const card = document.createElement('div');
      card.className = 'ward-gov-card';
      card.innerHTML = `
        <div style="font-weight: 800; font-size: 1rem; color: var(--ink); font-family: var(--font-display); margin-bottom: 4px;">${w.ward_name}</div>
        <div style="font-size: 0.75rem; color: var(--tomato); font-weight: 800; margin-bottom: 8px;">Corporation: ${w.city || 'Municipal'} &bull; ${w.ward_id}</div>
        <div style="font-size: 0.8rem; color: var(--ink); margin-bottom: 4px;">
          🏛️ <strong>Parshad:</strong> ${corp.name || 'Elected Ward Councillor'} (${corp.phone || 'N/A'})
        </div>
        <div style="font-size: 0.8rem; color: var(--ink); margin-bottom: 8px;">
          🏛️ <strong>MLA:</strong> ${mla.name || 'Constituency MLA'} (${mla.constituency || 'Assembly'})
        </div>
        <div style="font-size: 0.74rem; color: var(--ink); background: var(--paper-2); border: 1.5px solid var(--ink); padding: 6px 10px; border-radius: 8px; font-weight: 700;">
          📅 <strong>Ward Sabha:</strong> ${w.ward_sabha_schedule || '1st Saturday of Month, 10:30 AM'}
        </div>
      `;
      cardsContainer.appendChild(card);
    });
  } catch (e) {
    console.warn('Error loading governance data:', e);
  }
}

// FAST APPLICATION / GRIEVANCE TRACKER
async function trackApplication() {
  const inputEl = document.getElementById('track-id-input');
  const resultEl = document.getElementById('quick-track-result');
  if (!inputEl || !resultEl) return;

  const trackingId = inputEl.value.trim();
  if (!trackingId) return;

  resultEl.style.display = 'block';
  resultEl.innerHTML = '<div style="color: var(--ink); font-weight: 700;">Searching municipal database...</div>';

  try {
    const res = await fetch(`/api/v1/tracking/${encodeURIComponent(trackingId)}`);
    if (!res.ok) {
      resultEl.innerHTML = `<div style="color: var(--tomato); font-weight: 800;">Tracking ID '${trackingId}' not found. Please verify.</div>`;
      return;
    }

    const data = await res.json();
    resultEl.innerHTML = `
      <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 6px;">
        <strong style="color: var(--tomato); font-size: 0.95rem; font-family: var(--font-display);">${data.tracking_id}</strong>
        <span class="badge ${data.urgency === 'Critical' ? 'badge-critical' : 'badge-low'}">${data.status}</span>
      </div>
      <div style="font-weight: 800; color: var(--ink); margin-bottom: 4px; font-size: 0.95rem;">${data.title}</div>
      <div style="color: var(--text-muted); font-size: 0.75rem; margin-bottom: 6px; font-weight: 700;">
        📍 Ward: ${data.ward_name} &bull; Officer: ${data.assigned_engineer}
      </div>
      <div style="display: flex; justify-content: space-between; font-size: 0.75rem; color: var(--ink); margin-bottom: 8px; font-weight: 700;">
        <span>SLA Remaining: <strong>${data.sla_hours_remaining} Hours</strong></span>
        <span>Citizens Endorsed: <strong>${data.report_count}</strong></span>
      </div>
      <button class="btn-primary" style="font-size: 0.75rem; padding: 6px 12px; width: 100%;" onclick="openTrackingModal('${data.tracking_id}')">
        Open Full Multi-Agent Dossier &rarr;
      </button>
    `;
  } catch (e) {
    resultEl.innerHTML = `<div style="color: var(--tomato); font-weight: 800;">Error tracking application.</div>`;
  }
}

function quickTrackDemo(demoId) {
  const inputEl = document.getElementById('track-id-input');
  if (inputEl) {
    inputEl.value = demoId;
    trackApplication();
  }
}

async function openTrackingModal(trackingId) {
  try {
    const res = await fetch(`/api/v1/tracking/${encodeURIComponent(trackingId)}`);
    if (!res.ok) return;
    const data = await res.json();

    document.getElementById('track-modal-id').innerText = data.tracking_id;
    const body = document.getElementById('track-modal-body');

    let traceHtml = '';
    (data.agent_trace || []).forEach((st, idx) => {
      traceHtml += `
        <div style="background: #FFFDF7; border: 2px solid #231F20; border-left: 5px solid #FF5A4E; border-radius: 10px; padding: 8px 12px; margin-bottom: 8px; font-size: 0.78rem; box-shadow: 1px 1px 0 #231F20;">
          <div style="color: #231F20; font-weight: 800; font-family: 'Fredoka', cursive;">Step ${idx + 1}: ${st.agent_name} <span class="badge" style="background: #FFC93C; font-size: 10px; margin-left: 6px;">${st.status}</span></div>
          <div style="color: #57534e; font-weight: 600; margin-top: 3px;">${st.thought_log}</div>
        </div>
      `;
    });

    body.innerHTML = `
      <div style="background: #FFEFD0; border: 2.5px solid #231F20; border-radius: 14px; padding: 12px; margin-bottom: 12px; font-size: 0.82rem; color: #231F20; box-shadow: 2px 2px 0 #231F20;">
        <div><strong>Title:</strong> ${data.title}</div>
        <div><strong>Department:</strong> ${data.department}</div>
        <div><strong>Ward & Zone:</strong> ${data.ward_name} (${data.mcd_zone || ''})</div>
        <div><strong>Assigned Officer:</strong> ${data.assigned_engineer}</div>
        <div><strong>Statutory SLA:</strong> ${data.sla_hours_remaining} Hours remaining</div>
        <div><strong>Jan Sunwai Status:</strong> ${data.jan_sunwai_status || 'NONE'}</div>
      </div>
      <h4 style="font-size: 0.95rem; font-family: 'Fredoka', cursive; color: #231F20; margin-bottom: 6px;">Autonomous 6-Agent Deliberation Trail</h4>
      <div style="max-height: 220px; overflow-y: auto; background: #FFF6E5; border: 2px solid #231F20; padding: 10px; border-radius: 14px; box-shadow: inset 1px 1px 0 #231F20;">
        ${traceHtml || '<div style="color: #57534e; font-style: italic;">Standard SLA intake processing.</div>'}
      </div>
    `;

    document.getElementById('tracking-modal').style.display = 'flex';
  } catch (e) {
    if (typeof showStickerToast === 'function') {
      showStickerToast('Failed to load tracking modal', 'error');
    }
  }
}

function closeTrackingModal(event) {
  if (event && event.target !== document.getElementById('tracking-modal')) return;
  document.getElementById('tracking-modal').style.display = 'none';
}

// CITIZEN FORM SUBMISSION
async function handleCitizenSubmit(event) {
  event.preventDefault();

  // Enforce Citizen Authentication before lodging complaint
  if (!currentUser || !currentUser.user) {
    if (typeof showStickerToast === 'function') {
      showStickerToast('Please log in with Meri Pehchan or 1-click citizen profile to lodge your complaint.', 'info');
    }
    openLoginModal(() => {
      handleCitizenSubmit(event);
    });
    return;
  }

  const rawText = document.getElementById('complaint-text').value;
  const lat = parseFloat(document.getElementById('form-lat').value);
  const lon = parseFloat(document.getElementById('form-lon').value);
  const name = document.getElementById('citizen-name').value || currentUser.user.name;
  const phone = document.getElementById('citizen-phone').value || currentUser.user.phone;
  const imageHint = document.getElementById('form-image-hint').value;
  const resultEl = document.getElementById('submission-result');

  resultEl.style.display = 'block';
  resultEl.innerHTML = '<div style="color: var(--ink); font-weight: 700;">Submitting and processing with 6 autonomous agents...</div>';

  try {
    const payload = {
      raw_text: rawText,
      lat: lat,
      lon: lon,
      citizen_name: name,
      citizen_phone: phone,
      channel: 'web_portal',
      image_category_hint: imageHint || null
    };

    const headers = { 'Content-Type': 'application/json' };
    if (currentUser && currentUser.token) {
      headers['Authorization'] = `Bearer ${currentUser.token}`;
    }

    const res = await fetch('/api/v1/complaints/submit', {
      method: 'POST',
      headers: headers,
      body: JSON.stringify(payload)
    });

    if (!res.ok) throw new Error('Submission failed');
    const data = await res.json();

    const isDup = data.is_duplicate;
    const dupNotice = isDup
      ? `<div style="color: var(--ink); background: #FFF3DA; border: 1.5px solid var(--ink); border-radius: 8px; padding: 8px; margin-top: 6px; font-weight: 700;">🤝 <strong>Merged into Existing Master Incident:</strong> 300m spatial clustering detected neighborhood duplicate. You are linked as an active endorsement.</div>`
      : `<div style="color: var(--ink); background: #E8F9F2; border: 1.5px solid var(--ink); border-radius: 8px; padding: 8px; margin-top: 6px; font-weight: 700;">✨ <strong>New Master Incident Created:</strong> Automatically routed to Ward Junior Engineer with statutory SLA.</div>`;

    resultEl.innerHTML = `
      <div style="font-weight: 900; font-size: 1.1rem; color: var(--ink); font-family: var(--font-display); margin-bottom: 6px;">
        🎉 Grievance Successfully Registered!
      </div>
      <div>Tracking ID: <strong style="color: var(--tomato); font-family: var(--font-display);">${data.complaint_id}</strong></div>
      <div>Master Incident ID: <strong style="color: var(--ink); font-family: var(--font-display);">${data.master_ticket_id}</strong></div>
      <div>Department: <strong>${data.department}</strong> &bull; Urgency: <strong>${data.urgency}</strong></div>
      <div>Assigned Ward: <strong>${data.ward_extracted}</strong> &bull; Corporator: <strong>${data.corporator_name}</strong></div>
      <div>Statutory SLA: <strong>${data.citizen_charter_sla_hours} Hours</strong></div>
      ${dupNotice}
    `;

    document.getElementById('citizen-form').reset();
    syncFormWithUser();
    if (typeof showStickerToast === 'function') {
      showStickerToast('Grievance registered and routed to Ward Engineer!', 'success');
    }
    loadKPIStats();
    loadMasterTickets();
  } catch (err) {
    resultEl.innerHTML = `<div style="color: var(--tomato); font-weight: 800;">Error: ${err.message}</div>`;
  }
}

// VERNACULAR VOICE RECORDING
function toggleVoiceRecording() {
  // Enforce Citizen Authentication before recording voice grievance
  if (!currentUser || !currentUser.user) {
    if (typeof showStickerToast === 'function') {
      showStickerToast('Please log in with Meri Pehchan before recording a vernacular voice grievance.', 'info');
    }
    openLoginModal(() => {
      toggleVoiceRecording();
    });
    return;
  }

  const btn = document.getElementById('voice-record-btn');
  const label = document.getElementById('voice-btn-label');
  const statusLabel = document.getElementById('voice-status-label');
  const langSelect = document.getElementById('voice-lang-select');

  if (isRecording) {
    if (speechRecognizer) speechRecognizer.stop();
    isRecording = false;
    btn.style.background = 'var(--theme-primary)';
    btn.style.color = 'var(--cream-white)';
    label.innerText = 'Start Speaking';
    statusLabel.innerText = 'Recording completed and transcribed';
    return;
  }

  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (!SpeechRecognition) {
    statusLabel.innerText = 'Speech recognition not supported in browser. Using simulated transcription.';
    fillSampleGrievance('hi');
    return;
  }

  try {
    speechRecognizer = new SpeechRecognition();
    speechRecognizer.lang = langSelect.value === 'hinglish' ? 'hi-IN' : langSelect.value;
    speechRecognizer.interimResults = false;

    speechRecognizer.onstart = () => {
      isRecording = true;
      btn.style.background = 'var(--tomato)';
      btn.style.color = 'var(--cream-white)';
      label.innerText = 'Listening... Tap to Stop';
      statusLabel.innerText = 'Listening in ' + langSelect.options[langSelect.selectedIndex].text;
    };

    speechRecognizer.onresult = (e) => {
      const transcript = e.results[0][0].transcript;
      document.getElementById('complaint-text').value = transcript;
      statusLabel.innerText = `Transcribed: "${transcript}"`;
    };

    speechRecognizer.onerror = (e) => {
      statusLabel.innerText = `Microphone notice: ${e.error}. Selected sample loaded.`;
      isRecording = false;
      btn.style.background = 'var(--theme-primary)';
      btn.style.color = 'var(--cream-white)';
      label.innerText = 'Start Speaking';
      fillSampleGrievance('hi');
    };

    speechRecognizer.onend = () => {
      isRecording = false;
      btn.style.background = 'var(--theme-primary)';
      btn.style.color = 'var(--cream-white)';
      label.innerText = 'Start Speaking';
    };

    speechRecognizer.start();
  } catch (e) {
    fillSampleGrievance('hi');
  }
}

// Interactive Map Controls
function resetMapView() {
  const city = (typeof CITIES_DATA !== 'undefined' && CITIES_DATA[currentSelectedCity])
    ? CITIES_DATA[currentSelectedCity]
    : CITIES_DATA['all'];
  if (typeof flyToCity === 'function') {
    flyToCity(city.lat, city.lon, city.zoom);
  }
  if (typeof showStickerToast === 'function') {
    showStickerToast(`Map view centered on ${city.name}`, 'info');
  }
}

function toggleSpatialClusters() {
  showSpatialClusters = !showSpatialClusters;
  const btn = document.getElementById('btn-toggle-clusters');
  if (typeof radiusLayer !== 'undefined' && radiusLayer && typeof map !== 'undefined' && map) {
    if (showSpatialClusters) {
      map.addLayer(radiusLayer);
      if (btn) btn.innerText = '🔵 Toggle 300m Rings';
      if (typeof showStickerToast === 'function') {
        showStickerToast('300m Spatial Clustering Perimeters visible', 'info');
      }
    } else {
      map.removeLayer(radiusLayer);
      if (btn) btn.innerText = '⚪ Show 300m Rings';
      if (typeof showStickerToast === 'function') {
        showStickerToast('300m Spatial Clustering Perimeters hidden', 'info');
      }
    }
  }
}

function fillSampleGrievance(lang) {
  const samples = {
    hi: "सड़क पर बड़ा गड्ढा है, दो-पहिया वाहन गिर रहे हैं, कृपया जल्द मरम्मत कराएं",
    kn: "ರಸ್ತೆಯಲ್ಲಿ ದೊಡ್ಡ ಗುಂಡಿ ಬಿದ್ದಿದೆ, ವಾಹನ ಸವಾರರಿಗೆ ಅಪಘಾತವಾಗುವ ಸಂಭವವಿದೆ ಬೇಗ ಸರಿಮಾಡಿ",
    ta: "தெரு விளக்கு எரியவில்லை, இரவு நேரத்தில் மிகவும் இருட்டாக உள்ளது, சரிசெய்யவும்",
    hg: "Bhaiya road par street light 4 din se band hai, near Sharma general store pura andhera hai",
    en: "Dangerous sewer water overflowing on main road near gate, terrible smell please clear"
  };
  const txt = samples[lang] || samples.en;
  document.getElementById('complaint-text').value = txt;
  const statusLabel = document.getElementById('voice-status-label');
  if (statusLabel) statusLabel.innerText = `Loaded sample: "${txt}"`;
}

function setLocationCoords(lat, lon) {
  document.getElementById('form-lat').value = lat;
  document.getElementById('form-lon').value = lon;
}

function detectLocation() {
  const city = (typeof CITIES_DATA !== 'undefined' && CITIES_DATA[currentSelectedCity]) ? CITIES_DATA[currentSelectedCity] : CITIES_DATA['all'];
  const fallbackLat = (city.pins && city.pins[0]) ? city.pins[0].lat : city.lat;
  const fallbackLon = (city.pins && city.pins[0]) ? city.pins[0].lon : city.lon;

  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(
      (pos) => {
        setLocationCoords(pos.coords.latitude.toFixed(6), pos.coords.longitude.toFixed(6));
        if (typeof showStickerToast === 'function') {
          showStickerToast(`Detected GPS: (${pos.coords.latitude.toFixed(4)}, ${pos.coords.longitude.toFixed(4)})`, 'info');
        }
      },
      () => {
        setLocationCoords(fallbackLat, fallbackLon);
        if (typeof showStickerToast === 'function') {
          showStickerToast(`Simulated GPS location set to ${city.name} Central.`, 'info');
        }
      }
    );
  } else {
    setLocationCoords(fallbackLat, fallbackLon);
  }
}

// 2G LITE DATA WARD GRID
function renderLiteWardGrid(tickets) {
  const container = document.getElementById('lite-wards-container');
  if (!container) return;
  container.innerHTML = '';

  const wardsMap = {};
  tickets.forEach(t => {
    if (!wardsMap[t.ward_name]) {
      wardsMap[t.ward_name] = { name: t.ward_name, count: 0, critical: 0 };
    }
    wardsMap[t.ward_name].count += t.report_count;
    if (t.urgency === 'Critical') wardsMap[t.ward_name].critical++;
  });

  Object.values(wardsMap).forEach(w => {
    const card = document.createElement('div');
    card.style.background = '#FFFDF7';
    card.style.padding = '10px 14px';
    card.style.borderRadius = '14px';
    card.style.border = '2.5px solid #231F20';
    card.style.boxShadow = '2px 2px 0 #231F20';
    card.innerHTML = `
      <div style="font-weight: 800; color: #231F20; font-family: 'Fredoka', cursive;">${w.name}</div>
      <div style="font-size: 0.75rem; color: #57534e; font-weight: 700;">Reports: ${w.count} &bull; Critical: ${w.critical}</div>
    `;
    container.appendChild(card);
  });
}

// SIMULATE MULTI-AGENT SCENARIO
async function simulateAgentScenario(scenarioType) {
  const consoleEl = document.getElementById('deliberation-console');
  const statusEl = document.getElementById('sim-status-indicator');
  if (!consoleEl) return;

  if (typeof setMascotMood === 'function') {
    setMascotMood(scenarioType === 'spam_selfie_meme' ? 'confused' : 'panicking');
  }

  if (statusEl) {
    statusEl.innerText = 'Deliberating across 6 Autonomous Civic Agents...';
    statusEl.style.color = '#231F20';
  }

  consoleEl.innerHTML = `
    <div style="color: #FF5A4E; font-weight: 800; font-family: 'Fredoka', cursive;">
      &gt; INITIATING MULTI-AGENT CIVIC DELIBERATION PIPELINE FOR [${scenarioType.toUpperCase()}]...
    </div>
  `;

  try {
    const res = await fetch('/api/v1/agents/simulate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ scenario: scenarioType })
    });

    if (!res.ok) throw new Error('Simulation failed');
    const data = await res.json();

    if (data.agent_trace && data.agent_trace.length > 0) {
      let delay = 250;
      data.agent_trace.forEach((step, idx) => {
        setTimeout(() => {
          const stepDiv = document.createElement('div');
          stepDiv.className = 'deliberation-step';
          const isAlert = step.status.includes('FLAGGED') || step.status === 'ALERT' || step.status === 'ESCALATED';

          stepDiv.innerHTML = `
            <div class="step-header">
              <span style="font-family: 'Fredoka', cursive;">Step ${idx + 1}: ${step.agent_name}</span>
              <span class="badge ${isAlert ? 'badge-critical' : 'badge-low'}">${step.status}</span>
            </div>
            <div class="step-thought">&gt; ${step.thought_log}</div>
            <div class="step-action">Action: ${step.action_taken} &bull; Confidence: ${(step.confidence * 100).toFixed(1)}%</div>
          `;
          consoleEl.appendChild(stepDiv);
          consoleEl.scrollTop = consoleEl.scrollHeight;

          if (idx === data.agent_trace.length - 1) {
            const summaryDiv = document.createElement('div');
            summaryDiv.style.marginTop = '12px';
            summaryDiv.style.padding = '12px';
            summaryDiv.style.background = '#FFEFD0';
            summaryDiv.style.border = '2.5px solid #231F20';
            summaryDiv.style.borderRadius = '14px';
            summaryDiv.style.boxShadow = '3px 3px 0 #231F20';
            summaryDiv.innerHTML = `
              <div style="font-weight: 800; font-family: 'Fredoka', cursive; color: #FF5A4E; margin-bottom: 4px;">Executive Multi-Agent Summary:</div>
              <div style="color: #231F20; font-size: 0.82rem; font-weight: 600; line-height: 1.45;">${data.narrative_summary}</div>
            `;
            consoleEl.appendChild(summaryDiv);
            consoleEl.scrollTop = consoleEl.scrollHeight;

            if (statusEl) {
              statusEl.innerText = 'Orchestration Completed Successfully';
              statusEl.style.color = '#7BDCB5';
            }

            if (typeof setMascotMood === 'function') {
              setMascotMood('celebrating');
            }
          }
        }, delay);
        delay += 350;
      });
    }
  } catch (err) {
    consoleEl.innerHTML += `<div style="color: #ef4444;">Error: ${err.message}</div>`;
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

// Official Municipal Online Services Modal / Prompt
function openServiceInfo(serviceKey) {
  const serviceDetails = {
    birth_death: {
      title: "Civil Registration System (CRS) - Birth & Death Registration",
      body: "Institutional and home births/deaths within municipal jurisdiction can be registered online within 21 days with zero government fee. Digitize existing paper records, download verifiable QR certificates, or apply for corrections through the digital CRS gateway."
    },
    property_tax: {
      title: "Municipal Online Property Tax (PTR) & Mutation Gateway",
      body: "Compute property tax under Self-Assessment System (SAS) with geo-tagging validation. Access the 2026 Amnesty Rebate Scheme, view UPIC ownership dossiers, generate digital receipts, or track property mutation."
    },
    trade_license: {
      title: "Single Window Factory & Trade Licensing Gateway",
      body: "Instant issuance and auto-renewal of General Trade, Health, Factory, and Veterinary trade operating permits under the Ease of Doing Business framework with statutory e-SLA turnaround."
    },
    building_plan: {
      title: "Online Building Plan Sanction (OBPS)",
      body: "Submit architectural drawings, obtain automated structural stability scrutiny, and track sanction orders online with zero physical contact."
    },
    community_hall: {
      title: "Community Hall & Park Online Booking",
      body: "Reserve air-conditioned community centers, Barat Ghars, and municipal parks across all zones with transparent digital tariff payment."
    }
  };

  const s = serviceDetails[serviceKey];
  if (s) {
    if (typeof showStickerToast === 'function') {
      showStickerToast(`${s.title}: ${s.body}`, 'info', 5500);
    }
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

function toggleSunlightMode() {
  toggleHighContrast();
}

function toggleLiteMode() {
  document.body.classList.toggle('lite-data-mode');
  const isLite = document.body.classList.contains('lite-data-mode');
  localStorage.setItem('civicsense_lite', isLite ? 'true' : 'false');
}

// Expose functions globally on window for inline event handlers
window.initAuth = initAuth;
window.renderAuthHeader = renderAuthHeader;
window.openLoginModal = openLoginModal;
window.closeLoginModal = closeLoginModal;
window.loginWithPreset = loginWithPreset;
window.sendMobileOTP = sendMobileOTP;
window.autoFillDemoOTP = autoFillDemoOTP;
window.verifyMobileOTP = verifyMobileOTP;
window.logoutCitizen = logoutCitizen;
window.handleReportIssueClick = handleReportIssueClick;
window.handleGrievanceTabClick = handleGrievanceTabClick;
window.filterGallery = filterGallery;
window.resetMapView = resetMapView;
window.toggleSpatialClusters = toggleSpatialClusters;
window.filterJanSunwai = filterJanSunwai;
window.trackApplication = trackApplication;
window.quickTrackDemo = quickTrackDemo;
window.openTrackingModal = openTrackingModal;
window.closeTrackingModal = closeTrackingModal;
window.openTicketModal = openTicketModal;
window.closeModal = closeModal;
window.updateTicketStatus = updateTicketStatus;
window.escalateModalToJanSunwai = escalateModalToJanSunwai;
window.selectCity = selectCity;
window.switchTab = switchTab;
window.loadMasterTickets = loadMasterTickets;
window.loadTransformations = loadTransformations;
window.endorseTransformation = endorseTransformation;
window.claimPerk = claimPerk;
window.closePerkModal = closePerkModal;
window.toggleVoiceRecording = toggleVoiceRecording;
window.fillSampleGrievance = fillSampleGrievance;
window.detectLocation = detectLocation;
window.setLocationCoords = setLocationCoords;
window.handleCitizenSubmit = handleCitizenSubmit;
window.simulateAgentScenario = simulateAgentScenario;
window.loadAgentStatus = loadAgentStatus;
window.openServiceInfo = openServiceInfo;
window.changeFontSize = changeFontSize;
window.toggleHighContrast = toggleHighContrast;
window.toggleSunlightMode = toggleSunlightMode;
window.toggleLiteMode = toggleLiteMode;
window.onCommandCityChange = onCommandCityChange;
