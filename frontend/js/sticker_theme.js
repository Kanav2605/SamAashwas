/**
 * SamAashwas - Sticker Book Civic Theme Engine
 * Features:
 * - Floating background SVG objects with parallax drift & density control (Chaos 22, Normal 14, Calm 7, Off 0)
 * - 24 Pure Civic Floating SVG Objects (cones, potholes, streetlamps, taps, bins, brooms, hard-hats, etc.)
 * - 4 Light Skins (Tomato Toast [default], Mint Gelato, Bubblegum Pop, Mustard Mayhem)
 * - Motion setting (Chaos, Normal, Calm, Off) with reduced-motion support
 * - Goofy Municipal Mascot ("Aashwas-Babu") with hard hat, clipboard, googly eyes & 8 expressions
 * - Civic Capacity Squish Meter (<40% Roomy, 40-70% Cozy, 70-90% Snug, >90% High Surge)
 * - Font Size Setting (S / M / L)
 */

// 8 Mascot Moods & Civic Inspector Sayings
const MASCOT_QUOTES = {
  happy: [
    "Streets looking spick and span! Autonomous engines resolving tickets in record time!",
    "Ward 4 drain desilted before the clouds arrived! Citizen smiles guaranteed! 🎉",
    "Everything running smoothly! Fresh paper, verified civic resolutions!",
    "Civic trust index at an all-time high! Swachh Bharat squads in full swing!"
  ],
  inspecting: [
    "Inspecting road surface with precision... JE repair squad dispatched!",
    "Comparing before and after photos... Geo-coordinates match within 15 meters!",
    "Checking UPIC property tax ledger... Zero dues certificate verified!",
    "Scanning asset QR code... Pole maintenance history logged cleanly!"
  ],
  panicking: [
    "Aiyo! Pothole crater alert! Dispatching ward rapid-response squad stat!",
    "Live wire sparking hazard! Fast-lane emergency protocol triggered!",
    "Monsoon squall alert! Mobilizing dewatering pump teams to low-lying sectors!",
    "Surge Mode activated! High grievance volume incoming from Sector 12!"
  ],
  celebrating: [
    "Balle Balle! 100 Citizen Karma points unlocked for reporting that dark spot!",
    "Jan Sunwai docket resolved by the Zonal Commissioner before Friday!",
    "Swachh Nagrik badge awarded! You are a certified civic guardian!",
    "Clean lane verified! Slap an inspector gold star on that ward!"
  ],
  confused: [
    "Arre, is that a pothole or a swimming pool? Checking multimodal vision AI...",
    "Wait, that's a random meme selfie, not a broken drain! Spam shield flagged it!",
    "Searching the zonal records... Which department owns this boundary road?",
    "Need coordinates! Drop a map pin so our field team knows where to roll!"
  ],
  soaked: [
    "Rain pouring buckets! Check the Monsoon Risk Shield for pump status!",
    "My hard hat is dripping! Primary storm drains desilted just in time!",
    "Monsoon preparedness check: high-risk wards alerted 48 hours early!",
    "Paper boats on the street? That means a blocked culvert needs jetting!"
  ],
  sweating: [
    "Whew, 42 degrees in the shade! Field squads repairing transformer links!",
    "High complaint velocity in Ward 7! Spatial deduplication merging 40 tickets into 1!",
    "SLA countdown ticking: 3 hours remaining before ombudsman escalation!",
    "Hot pavement patch work underway! Hats off to the junior engineers!"
  ],
  sleepy: [
    "Night patrol active. Smart LED streetlight sensors monitoring dark spots.",
    "Quiet night across the wards. Background outbox syncing citizen dockets.",
    "Recharging clipboards for the morning Ward Sabha inspection walk.",
    "All clear for now. Babu is taking a small chai break!"
  ]
};

// 24 Pure Civic Flat SVG Objects (Section 7) - Municipal Grievance Theme
const SVG_OBJECTS = {
  'cone': `
    <svg viewBox="0 0 36 36" width="100%" height="100%" fill="none" xmlns="http://www.w3.org/2000/svg">
      <ellipse cx="18" cy="30" rx="13" ry="3.5" fill="#FF5A4E" stroke="#231F20" stroke-width="2.5"/>
      <polygon points="18,4 8,29 28,29" fill="#FF5A4E" stroke="#231F20" stroke-width="2.5"/>
      <polygon points="18,12 12,23 24,23" fill="#FFFDF7" stroke="#231F20" stroke-width="2"/>
    </svg>`,

  'pothole': `
    <svg viewBox="0 0 36 36" width="100%" height="100%" fill="none" xmlns="http://www.w3.org/2000/svg">
      <ellipse cx="18" cy="22" rx="14" ry="7" fill="#231F20"/>
      <ellipse cx="18" cy="20" rx="12" ry="5.5" fill="#FFB88A" stroke="#231F20" stroke-width="2"/>
      <circle cx="14" cy="19" r="2.5" fill="#FFFDF7" stroke="#231F20" stroke-width="1"/>
      <circle cx="15" cy="19" r="1" fill="#231F20"/>
      <circle cx="22" cy="19" r="2.5" fill="#FFFDF7" stroke="#231F20" stroke-width="1"/>
      <circle cx="21" cy="19" r="1" fill="#231F20"/>
    </svg>`,

  'streetlamp': `
    <svg viewBox="0 0 36 40" width="100%" height="100%" fill="none" xmlns="http://www.w3.org/2000/svg">
      <line x1="18" y1="14" x2="18" y2="38" stroke="#231F20" stroke-width="3"/>
      <path d="M12 14 L24 14 L21 4 L15 4 Z" fill="#FFC93C" stroke="#231F20" stroke-width="2.5"/>
      <polygon points="18,14 8,36 28,36" fill="#FFF6E5" opacity="0.6"/>
      <circle cx="18" cy="10" r="2" fill="#FF5A4E"/>
    </svg>`,

  'tap': `
    <svg viewBox="0 0 36 36" width="100%" height="100%" fill="none" xmlns="http://www.w3.org/2000/svg">
      <rect x="4" y="10" width="14" height="6" rx="2" fill="#7BDCB5" stroke="#231F20" stroke-width="2"/>
      <path d="M14 10 L14 6 L18 6 L18 10" stroke="#231F20" stroke-width="2.5"/>
      <rect x="13" y="3" width="6" height="3" rx="1" fill="#FF5A4E" stroke="#231F20" stroke-width="1.5"/>
      <path d="M14 16 L14 20 L10 20 L10 16" fill="#7BDCB5" stroke="#231F20" stroke-width="2"/>
      <ellipse cx="12" cy="27" rx="2" ry="3" fill="#B8A6FF" stroke="#231F20" stroke-width="1.5"/>
    </svg>`,

  'garbage-bin': `
    <svg viewBox="0 0 36 40" width="100%" height="100%" fill="none" xmlns="http://www.w3.org/2000/svg">
      <rect x="8" y="10" width="20" height="24" rx="3" fill="#7BDCB5" stroke="#231F20" stroke-width="2.5"/>
      <line x1="6" y1="10" x2="30" y2="10" stroke="#231F20" stroke-width="3" stroke-linecap="round"/>
      <rect x="14" y="6" width="8" height="4" rx="1" fill="#FFC93C" stroke="#231F20" stroke-width="2"/>
      <line x1="14" y1="15" x2="14" y2="28" stroke="#231F20" stroke-width="2" stroke-linecap="round"/>
      <line x1="22" y1="15" x2="22" y2="28" stroke="#231F20" stroke-width="2" stroke-linecap="round"/>
      <circle cx="10" cy="34" r="2.5" fill="#231F20"/>
      <circle cx="26" cy="34" r="2.5" fill="#231F20"/>
    </svg>`,

  'broom': `
    <svg viewBox="0 0 36 40" width="100%" height="100%" fill="none" xmlns="http://www.w3.org/2000/svg">
      <line x1="26" y1="4" x2="14" y2="24" stroke="#231F20" stroke-width="3" stroke-linecap="round"/>
      <polygon points="14,24 6,36 18,36" fill="#FFC93C" stroke="#231F20" stroke-width="2.5"/>
      <line x1="9" y1="36" x2="13" y2="27" stroke="#231F20" stroke-width="1.5"/>
      <line x1="15" y1="36" x2="15" y2="27" stroke="#231F20" stroke-width="1.5"/>
      <line x1="11" y1="28" x2="17" y2="26" stroke="#FF5A4E" stroke-width="2"/>
    </svg>`,

  'manhole': `
    <svg viewBox="0 0 36 36" width="100%" height="100%" fill="none" xmlns="http://www.w3.org/2000/svg">
      <circle cx="18" cy="18" r="14" fill="#FFB88A" stroke="#231F20" stroke-width="2.5"/>
      <circle cx="18" cy="18" r="9" stroke="#231F20" stroke-width="2" stroke-dasharray="3 3"/>
      <circle cx="18" cy="18" r="3" fill="#231F20"/>
      <line x1="4" y1="18" x2="9" y2="18" stroke="#231F20" stroke-width="2"/>
      <line x1="27" y1="18" x2="32" y2="18" stroke="#231F20" stroke-width="2"/>
      <line x1="18" y1="4" x2="18" y2="9" stroke="#231F20" stroke-width="2"/>
      <line x1="18" y1="27" x2="18" y2="32" stroke="#231F20" stroke-width="2"/>
    </svg>`,

  'paper-boat': `
    <svg viewBox="0 0 40 32" width="100%" height="100%" fill="none" xmlns="http://www.w3.org/2000/svg">
      <polygon points="6,20 34,20 28,28 12,28" fill="#FFFDF7" stroke="#231F20" stroke-width="2.5"/>
      <polygon points="6,20 20,6 20,20" fill="#FFC93C" stroke="#231F20" stroke-width="2"/>
      <polygon points="20,8 34,20 20,20" fill="#FF5A4E" stroke="#231F20" stroke-width="2"/>
      <path d="M4 30 Q12 32 20 30 Q28 28 36 30" stroke="#B8A6FF" stroke-width="2" stroke-linecap="round"/>
    </svg>`,

  'umbrella': `
    <svg viewBox="0 0 36 38" width="100%" height="100%" fill="none" xmlns="http://www.w3.org/2000/svg">
      <path d="M5 20 C5 9 11 4 18 4 C25 4 31 9 31 20 Z" fill="#FFC93C" stroke="#231F20" stroke-width="2.5"/>
      <path d="M12 20 C12 9 18 4 18 4 C18 4 24 9 24 20" stroke="#231F20" stroke-width="2" fill="#FF5A4E"/>
      <line x1="18" y1="4" x2="18" y2="30" stroke="#231F20" stroke-width="2.5"/>
      <path d="M18 30 C18 34 14 34 14 31" stroke="#231F20" stroke-width="2.5" fill="none" stroke-linecap="round"/>
    </svg>`,

  'rain-cloud': `
    <svg viewBox="0 0 42 34" width="100%" height="100%" fill="none" xmlns="http://www.w3.org/2000/svg">
      <path d="M10 18 C5 18 3 14 5 10 C4 6 9 3 14 4 C17 0 25 0 28 4 C33 3 38 7 37 11 C40 14 39 18 33 18 Z" 
            fill="#FFFDF7" stroke="#231F20" stroke-width="2.5" stroke-linejoin="round"/>
      <line x1="12" y1="22" x2="9" y2="29" stroke="#7BDCB5" stroke-width="2.5" stroke-linecap="round"/>
      <line x1="20" y1="22" x2="17" y2="29" stroke="#7BDCB5" stroke-width="2.5" stroke-linecap="round"/>
      <line x1="28" y1="22" x2="25" y2="29" stroke="#7BDCB5" stroke-width="2.5" stroke-linecap="round"/>
    </svg>`,

  'kulhad-chai': `
    <svg viewBox="0 0 36 38" width="100%" height="100%" fill="none" xmlns="http://www.w3.org/2000/svg">
      <polygon points="8,12 28,12 24,32 12,32" fill="#FFB88A" stroke="#231F20" stroke-width="2.5"/>
      <ellipse cx="18" cy="12" rx="10" ry="2.5" fill="#FF5A4E" stroke="#231F20" stroke-width="2"/>
      <path d="M14 8 C14 5 16 4 16 2" stroke="#231F20" stroke-width="2" stroke-linecap="round"/>
      <path d="M20 8 C20 5 22 4 22 2" stroke="#231F20" stroke-width="2" stroke-linecap="round"/>
      <line x1="11" y1="22" x2="25" y2="22" stroke="#231F20" stroke-width="1.5" stroke-dasharray="2 2"/>
    </svg>`,

  'auto-rickshaw': `
    <svg viewBox="0 0 44 34" width="100%" height="100%" fill="none" xmlns="http://www.w3.org/2000/svg">
      <path d="M6 22 L10 10 L26 8 L36 16 L36 24 L6 24 Z" fill="#7BDCB5" stroke="#231F20" stroke-width="2.5"/>
      <path d="M10 10 L26 8 L24 4 L8 6 Z" fill="#FFC93C" stroke="#231F20" stroke-width="2"/>
      <rect x="22" y="12" width="10" height="7" rx="1" fill="#FFFDF7" stroke="#231F20" stroke-width="1.5"/>
      <circle cx="12" cy="25" r="4.5" fill="#231F20"/>
      <circle cx="12" cy="25" r="1.5" fill="#FFFDF7"/>
      <circle cx="32" cy="25" r="4.5" fill="#231F20"/>
      <circle cx="32" cy="25" r="1.5" fill="#FFFDF7"/>
      <circle cx="38" cy="18" r="2" fill="#FF5A4E" stroke="#231F20" stroke-width="1"/>
    </svg>`,

  'hard-hat': `
    <svg viewBox="0 0 38 32" width="100%" height="100%" fill="none" xmlns="http://www.w3.org/2000/svg">
      <path d="M7 19 C7 9 13 4 19 4 C25 4 31 9 31 19 Z" fill="#FFC93C" stroke="#231F20" stroke-width="2.5"/>
      <rect x="4" y="19" width="30" height="5" rx="2.5" fill="#FFC93C" stroke="#231F20" stroke-width="2.5"/>
      <line x1="19" y1="4" x2="19" y2="18" stroke="#231F20" stroke-width="2"/>
      <circle cx="19" cy="12" r="2.5" fill="#FF5A4E"/>
    </svg>`,

  'wrench': `
    <svg viewBox="0 0 36 36" width="100%" height="100%" fill="none" xmlns="http://www.w3.org/2000/svg">
      <line x1="10" y1="26" x2="24" y2="12" stroke="#231F20" stroke-width="5" stroke-linecap="round"/>
      <line x1="10" y1="26" x2="24" y2="12" stroke="#7BDCB5" stroke-width="2.5" stroke-linecap="round"/>
      <circle cx="26" cy="10" r="6" fill="#7BDCB5" stroke="#231F20" stroke-width="2.5"/>
      <polygon points="26,10 32,7 29,4" fill="#FFF6E5"/>
    </svg>`,

  'clipboard': `
    <svg viewBox="0 0 34 40" width="100%" height="100%" fill="none" xmlns="http://www.w3.org/2000/svg">
      <rect x="6" y="8" width="22" height="28" rx="3" fill="#FFFDF7" stroke="#231F20" stroke-width="2.5"/>
      <rect x="11" y="4" width="12" height="6" rx="2" fill="#FF5A4E" stroke="#231F20" stroke-width="2"/>
      <path d="M11 16 L14 19 L21 13" stroke="#16a34a" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
      <line x1="11" y1="24" x2="23" y2="24" stroke="#231F20" stroke-width="2" stroke-linecap="round"/>
      <line x1="11" y1="30" x2="19" y2="30" stroke="#231F20" stroke-width="2" stroke-linecap="round"/>
    </svg>`,

  'megaphone': `
    <svg viewBox="0 0 40 34" width="100%" height="100%" fill="none" xmlns="http://www.w3.org/2000/svg">
      <polygon points="12,14 26,6 26,24 12,18" fill="#FF5A4E" stroke="#231F20" stroke-width="2.5"/>
      <rect x="6" y="13" width="7" height="6" rx="1.5" fill="#FFC93C" stroke="#231F20" stroke-width="2"/>
      <line x1="14" y1="18" x2="16" y2="28" stroke="#231F20" stroke-width="3" stroke-linecap="round"/>
      <ellipse cx="26" cy="15" rx="3" ry="9" fill="#FFC93C" stroke="#231F20" stroke-width="2"/>
    </svg>`,

  'speech-bubble': `
    <svg viewBox="0 0 40 34" width="100%" height="100%" fill="none" xmlns="http://www.w3.org/2000/svg">
      <path d="M6 8 C6 4 10 3 18 3 C26 3 34 4 34 8 C34 16 30 18 22 18 L16 26 L16 18 C8 18 6 15 6 8 Z" 
            fill="#B8A6FF" stroke="#231F20" stroke-width="2.5"/>
      <circle cx="14" cy="11" r="1.5" fill="#231F20"/>
      <circle cx="20" cy="11" r="1.5" fill="#231F20"/>
      <circle cx="26" cy="11" r="1.5" fill="#231F20"/>
    </svg>`,

  'tiffin-box': `
    <svg viewBox="0 0 32 38" width="100%" height="100%" fill="none" xmlns="http://www.w3.org/2000/svg">
      <rect x="6" y="12" width="20" height="7" rx="2" fill="#FFFDF7" stroke="#231F20" stroke-width="2"/>
      <rect x="6" y="19" width="20" height="7" rx="2" fill="#FFFDF7" stroke="#231F20" stroke-width="2"/>
      <rect x="6" y="26" width="20" height="7" rx="2" fill="#FFFDF7" stroke="#231F20" stroke-width="2"/>
      <path d="M6 16 L3 16 L3 30 L6 30" stroke="#FF5A4E" stroke-width="2"/>
      <path d="M26 16 L29 16 L29 30 L26 30" stroke="#FF5A4E" stroke-width="2"/>
      <path d="M10 12 L10 6 C10 4 22 4 22 6 L22 12" stroke="#FF5A4E" stroke-width="2.5" fill="none"/>
    </svg>`,

  'kite': `
    <svg viewBox="0 0 36 42" width="100%" height="100%" fill="none" xmlns="http://www.w3.org/2000/svg">
      <polygon points="18,3 32,18 18,33 4,18" fill="#FF9EC4" stroke="#231F20" stroke-width="2.5"/>
      <line x1="18" y1="3" x2="18" y2="33" stroke="#231F20" stroke-width="1.5"/>
      <path d="M4 18 Q18 24 32 18" stroke="#231F20" stroke-width="1.5" fill="none"/>
      <polygon points="18,33 14,39 22,39" fill="#FFC93C" stroke="#231F20" stroke-width="2"/>
    </svg>`,

  'balloon': `
    <svg viewBox="0 0 32 42" width="100%" height="100%" fill="none" xmlns="http://www.w3.org/2000/svg">
      <ellipse cx="16" cy="16" rx="12" ry="14" fill="#FF5A4E" stroke="#231F20" stroke-width="2.5"/>
      <polygon points="16,30 13,34 19,34" fill="#FF5A4E" stroke="#231F20" stroke-width="1.5"/>
      <path d="M16 34 Q12 38 18 42" stroke="#231F20" stroke-width="2" fill="none"/>
    </svg>`,

  'marigold': `
    <svg viewBox="0 0 36 36" width="100%" height="100%" fill="none" xmlns="http://www.w3.org/2000/svg">
      <circle cx="18" cy="18" r="13" fill="#FFC93C" stroke="#231F20" stroke-width="2.5"/>
      <circle cx="18" cy="18" r="8" fill="#FF5A4E" stroke="#231F20" stroke-width="2"/>
      <circle cx="18" cy="18" r="3.5" fill="#FFFDF7"/>
    </svg>`,

  'crow': `
    <svg viewBox="0 0 38 34" width="100%" height="100%" fill="none" xmlns="http://www.w3.org/2000/svg">
      <path d="M8 20 Q12 12 22 14 Q28 8 32 12 Q36 14 38 13 L34 17 Q32 26 22 26 Q12 26 8 20 Z" 
            fill="#231F20" stroke="#231F20" stroke-width="2"/>
      <circle cx="30" cy="13" r="1.5" fill="#FFFDF7"/>
      <line x1="16" y1="26" x2="14" y2="32" stroke="#231F20" stroke-width="2"/>
      <line x1="22" y1="26" x2="22" y2="32" stroke="#231F20" stroke-width="2"/>
    </svg>`,

  'smiling-sun': `
    <svg viewBox="0 0 36 36" width="100%" height="100%" fill="none" xmlns="http://www.w3.org/2000/svg">
      <circle cx="18" cy="18" r="9" fill="#FFC93C" stroke="#231F20" stroke-width="2.5"/>
      <line x1="18" y1="3" x2="18" y2="6" stroke="#231F20" stroke-width="2.5" stroke-linecap="round"/>
      <line x1="18" y1="30" x2="18" y2="33" stroke="#231F20" stroke-width="2.5" stroke-linecap="round"/>
      <line x1="3" y1="18" x2="6" y2="18" stroke="#231F20" stroke-width="2.5" stroke-linecap="round"/>
      <line x1="30" y1="18" x2="33" y2="18" stroke="#231F20" stroke-width="2.5" stroke-linecap="round"/>
      <circle cx="15" cy="16" r="1.5" fill="#231F20"/>
      <circle cx="21" cy="16" r="1.5" fill="#231F20"/>
      <path d="M15 19 Q18 22 21 19" stroke="#231F20" stroke-width="2" stroke-linecap="round"/>
    </svg>`,

  'mango': `
    <svg viewBox="0 0 36 38" width="100%" height="100%" fill="none" xmlns="http://www.w3.org/2000/svg">
      <path d="M12 14 C10 6 22 4 24 12 C26 20 22 32 14 30 C8 28 8 20 12 14 Z" 
            fill="#FFC93C" stroke="#231F20" stroke-width="2.5"/>
      <path d="M22 6 Q28 4 30 8 Q24 10 22 6" fill="#7BDCB5" stroke="#231F20" stroke-width="1.5"/>
      <ellipse cx="14" cy="22" rx="2" ry="4" fill="#FF5A4E" opacity="0.6"/>
    </svg>`
};

const OBJECT_KEYS = Object.keys(SVG_OBJECTS);

// Density Map (Section 7)
const DENSITY_MAP = {
  chaos: 22,
  normal: 14,
  calm: 7,
  off: 0
};

// State
let currentSkin = localStorage.getItem('sticker_skin') || 'tomato-toast';
let currentMotion = localStorage.getItem('sticker_motion') || 'off';
let currentMascotMood = 'happy';

// Initialize Theme Systems
document.addEventListener('DOMContentLoaded', () => {
  applySkin(currentSkin);
  applyMotion(currentMotion);
  initFloatingBackground();
  initMascotBuddy();
  updateSquishMeter(62); // Initial cozy state
  initFontSizePreference();
});

// 1. Skin Switcher (4 Light Skins)
function applySkin(skinName) {
  currentSkin = skinName;
  localStorage.setItem('sticker_skin', skinName);

  document.body.classList.remove(
    'skin-tomato-toast',
    'skin-mint-gelato',
    'skin-bubblegum-pop',
    'skin-mustard-mayhem'
  );
  document.body.classList.add(`skin-${skinName}`);

  document.querySelectorAll('.skin-btn').forEach(btn => {
    btn.classList.toggle('active', btn.getAttribute('data-skin') === skinName);
  });
}

// 2. Motion Setting (Chaos, Normal, Calm, Off)
function applyMotion(motionLevel) {
  currentMotion = motionLevel;
  localStorage.setItem('sticker_motion', motionLevel);
  document.body.setAttribute('data-motion', motionLevel);

  document.querySelectorAll('.motion-btn').forEach(btn => {
    btn.classList.toggle('active', btn.getAttribute('data-motion') === motionLevel);
  });

  renderFloatingObjects();
}

// 3. Floating Background Objects (Section 7)
function initFloatingBackground() {
  let bgEl = document.getElementById('floating-background');
  if (!bgEl) {
    bgEl = document.createElement('div');
    bgEl.id = 'floating-background';
    bgEl.className = 'floating-background-layer';
    document.body.insertBefore(bgEl, document.body.firstChild);
  }
  renderFloatingObjects();
}

function renderFloatingObjects() {
  const bgEl = document.getElementById('floating-background');
  if (!bgEl) return;

  // Clear existing
  bgEl.innerHTML = '';

  // Check display modes and reduced motion
  const isReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const isSunlight = document.body.classList.contains('sunlight-mode');
  const isLite = document.body.classList.contains('lite-data-mode');

  if (currentMotion === 'off' || isReducedMotion || isSunlight || isLite) {
    return;
  }

  const count = DENSITY_MAP[currentMotion] || 14;
  const screenWidth = window.innerWidth;
  const screenHeight = window.innerHeight;

  // Seeded coordinate distribution
  for (let i = 0; i < count; i++) {
    const key = OBJECT_KEYS[i % OBJECT_KEYS.length];
    const objSvg = SVG_OBJECTS[key];
    if (!objSvg) continue;

    const el = document.createElement('div');
    el.className = 'floating-sticker-item';

    // Determinate layout grid with pseudo-random jitter
    const col = i % 5;
    const row = Math.floor(i / 5);
    const posX = (col * 20) + ((i * 17) % 15);
    const posY = (row * 22) + ((i * 19) % 15);
    const tilt = ((i * 13) % 40) - 20; // -20deg to +20deg
    const scale = 0.85 + ((i % 4) * 0.1);
    const duration = 16 + (i % 8) * 3; // 16s - 37s drift

    el.style.left = `${posX}%`;
    el.style.top = `${posY}%`;
    el.style.transform = `rotate(${tilt}deg) scale(${scale})`;
    el.style.animationDuration = `${duration}s`;
    el.style.animationDelay = `-${(i * 3) % duration}s`;

    el.innerHTML = objSvg;
    bgEl.appendChild(el);
  }
}

// 4. Mascot SVG Generator (Municipal Inspector Aashwas-Babu)
function getMascotSVG(expression = 'happy', size = 68) {
  let mouthHtml = '';
  let leftEyePupil = `<circle cx="16" cy="20" r="3" fill="#231F20"/>`;
  let rightEyePupil = `<circle cx="32" cy="20" r="3" fill="#231F20"/>`;
  let extraAccessories = '';

  if (expression === 'happy') {
    mouthHtml = `
      <path d="M19 28 Q24 35 29 28 Z" stroke="#231F20" stroke-width="2.5" fill="#FF5A4E"/>
      <path d="M21 28 Q24 31 27 28" stroke="#FFFDF7" stroke-width="2" stroke-linecap="round"/>
    `;
    leftEyePupil = `<circle cx="17" cy="19" r="3" fill="#231F20"/>`;
    rightEyePupil = `<circle cx="31" cy="19" r="3" fill="#231F20"/>`;
  } else if (expression === 'inspecting') {
    mouthHtml = `<path d="M20 28 L28 28" stroke="#231F20" stroke-width="2.5" stroke-linecap="round"/>`;
    leftEyePupil = `<circle cx="16" cy="20" r="4" fill="#231F20"/>`;
    rightEyePupil = `<circle cx="32" cy="20" r="2.5" fill="#231F20"/>`;
    extraAccessories = `
      <!-- Magnifying Glass -->
      <circle cx="38" cy="22" r="7" stroke="#231F20" stroke-width="2.5" fill="#FFF6E5" fill-opacity="0.5"/>
      <line x1="43" y1="27" x2="48" y2="34" stroke="#231F20" stroke-width="3" stroke-linecap="round"/>
    `;
  } else if (expression === 'panicking') {
    mouthHtml = `<ellipse cx="24" cy="30" rx="4.5" ry="5.5" fill="#231F20"/>`;
    leftEyePupil = `<circle cx="16" cy="18" r="4.5" fill="#FF5A4E"/>`;
    rightEyePupil = `<circle cx="32" cy="18" r="4.5" fill="#FF5A4E"/>`;
    extraAccessories = `
      <!-- Sweat Drops -->
      <path d="M8 12 Q7 8 9 12 Q10 15 7 15 Q5 15 8 12 Z" fill="#7BDCB5" stroke="#231F20" stroke-width="1.5"/>
      <path d="M40 12 Q39 8 41 12 Q42 15 39 15 Q37 15 40 12 Z" fill="#7BDCB5" stroke="#231F20" stroke-width="1.5"/>
    `;
  } else if (expression === 'celebrating') {
    mouthHtml = `
      <path d="M18 27 Q24 36 30 27 Z" stroke="#231F20" stroke-width="2.5" fill="#FF5A4E"/>
    `;
    leftEyePupil = `<polygon points="16,16 18,19 21,19 19,21 20,24 16,22 13,24 14,21 12,19 15,19" fill="#FFC93C" stroke="#231F20" stroke-width="1"/>`;
    rightEyePupil = `<polygon points="32,16 34,19 37,19 35,21 36,24 32,22 29,24 30,21 28,19 31,19" fill="#FFC93C" stroke="#231F20" stroke-width="1"/>`;
    extraAccessories = `
      <!-- Confetti Stars -->
      <circle cx="6" cy="4" r="2.5" fill="#FF5A4E"/>
      <circle cx="42" cy="6" r="2" fill="#7BDCB5"/>
      <circle cx="38" cy="-2" r="2.5" fill="#B8A6FF"/>
    `;
  } else if (expression === 'confused') {
    mouthHtml = `<path d="M19 30 L29 27" stroke="#231F20" stroke-width="2.5" stroke-linecap="round"/>`;
    leftEyePupil = `<circle cx="15" cy="18" r="4" fill="#231F20"/>`;
    rightEyePupil = `<circle cx="33" cy="22" r="2" fill="#231F20"/>`;
    extraAccessories = `
      <text x="36" y="8" font-family="'Fredoka', sans-serif" font-weight="900" font-size="16" fill="#FF5A4E">?</text>
    `;
  } else if (expression === 'soaked') {
    mouthHtml = `<path d="M20 30 Q24 26 28 30" stroke="#231F20" stroke-width="2.5" stroke-linecap="round" fill="none"/>`;
    extraAccessories = `
      <!-- Water Droplets dripping from hard hat -->
      <path d="M12 12 Q11 8 13 12 Q14 15 11 15 Z" fill="#B8A6FF" stroke="#231F20" stroke-width="1.5"/>
      <path d="M36 12 Q35 8 37 12 Q38 15 35 15 Z" fill="#B8A6FF" stroke="#231F20" stroke-width="1.5"/>
      <ellipse cx="24" cy="42" rx="14" ry="3" fill="#B8A6FF" stroke="#231F20" stroke-width="1.5"/>
    `;
  } else if (expression === 'sweating') {
    mouthHtml = `<path d="M20 29 Q24 32 28 29" stroke="#231F20" stroke-width="2" stroke-linecap="round"/>`;
    extraAccessories = `
      <!-- Sun Wipe -->
      <path d="M38 14 Q37 10 39 14 Q40 17 37 17 Z" fill="#FFB88A" stroke="#231F20" stroke-width="1.5"/>
    `;
  } else { // sleepy
    mouthHtml = `<path d="M21 28 L27 28" stroke="#231F20" stroke-width="2" stroke-linecap="round"/>`;
    leftEyePupil = `<line x1="13" y1="20" x2="19" y2="20" stroke="#231F20" stroke-width="2.5"/>`;
    rightEyePupil = `<line x1="29" y1="20" x2="35" y2="20" stroke="#231F20" stroke-width="2.5"/>`;
    extraAccessories = `
      <text x="36" y="6" font-family="'Fredoka', sans-serif" font-weight="900" font-size="12" fill="#B8A6FF">zZ</text>
    `;
  }

  return `
    <svg viewBox="-4 -8 56 56" width="${size}" height="${size}" fill="none" xmlns="http://www.w3.org/2000/svg" class="mascot-svg mascot-${expression}">
      <!-- Inspector Head -->
      <rect x="6" y="10" width="36" height="30" rx="14" fill="#FFC93C" stroke="#231F20" stroke-width="2.5"/>

      <!-- Inspector Hard Hat -->
      <path d="M4 10 C4 2 12 -4 24 -4 C36 -4 44 2 44 10 Z" fill="#FF5A4E" stroke="#231F20" stroke-width="2.5"/>
      <rect x="2" y="9" width="44" height="4" rx="2" fill="#FFC93C" stroke="#231F20" stroke-width="2"/>
      <circle cx="24" cy="2" r="3" fill="#FFFDF7" stroke="#231F20" stroke-width="1.5"/>
      <circle cx="24" cy="2" r="1.2" fill="#FF5A4E"/>

      <!-- Cheeks -->
      <circle cx="10" cy="28" r="3.5" fill="#FF9EC4" stroke="#231F20" stroke-width="1.5"/>
      <circle cx="38" cy="28" r="3.5" fill="#FF9EC4" stroke="#231F20" stroke-width="1.5"/>

      <!-- Googly Eye Sockets -->
      <circle cx="16" cy="20" r="7" fill="#FFFDF7" stroke="#231F20" stroke-width="2.5"/>
      <circle cx="32" cy="20" r="7" fill="#FFFDF7" stroke="#231F20" stroke-width="2.5"/>

      <!-- Pupils -->
      ${leftEyePupil}
      ${rightEyePupil}

      <!-- Glorious Inspector Moustache -->
      <path d="M12 26 C16 23 21 26 24 25 C27 26 32 23 36 26 C33 30 26 31 24 27 C22 31 15 30 12 26 Z" 
            fill="#231F20" stroke="#231F20" stroke-width="1.5"/>

      <!-- Mouth -->
      ${mouthHtml}

      <!-- Inspector Clipboard Badge on shoulder -->
      <rect x="36" y="32" width="10" height="13" rx="2" fill="#FFFDF7" stroke="#231F20" stroke-width="2"/>
      <rect x="39" y="30" width="4" height="3" rx="1" fill="#FF5A4E" stroke="#231F20" stroke-width="1.5"/>
      <line x1="38" y1="36" x2="43" y2="36" stroke="#231F20" stroke-width="1.2"/>
      <line x1="38" y1="40" x2="42" y2="40" stroke="#231F20" stroke-width="1.2"/>

      <!-- Extra Mood Accessories -->
      ${extraAccessories}
    </svg>
  `;
}

// 5. Interactive Mascot Buddy Widget ("Aashwas-Babu")
function initMascotBuddy() {
  let mascotContainer = document.getElementById('mascot-buddy-widget');
  if (!mascotContainer) {
    mascotContainer = document.createElement('div');
    mascotContainer.id = 'mascot-buddy-widget';
    mascotContainer.className = 'mascot-floating-buddy';
    document.body.appendChild(mascotContainer);
  }

  updateMascotDisplay();

  mascotContainer.addEventListener('click', () => {
    cycleMascotMood();
    squishMascotElement();
  });
}

function updateMascotDisplay() {
  const container = document.getElementById('mascot-buddy-widget');
  if (!container) return;

  const quotes = MASCOT_QUOTES[currentMascotMood] || MASCOT_QUOTES.happy;
  const quote = quotes[Math.floor(Math.random() * quotes.length)];

  container.innerHTML = `
    <div class="mascot-speech-bubble" id="mascot-speech">
      <span class="mascot-speech-mood">${currentMascotMood.toUpperCase()}</span>
      <div class="mascot-speech-text">"${quote}"</div>
      <div class="mascot-actions-bar">
        <button type="button" class="mascot-action-mini-btn" onclick="event.stopPropagation(); triggerMascotChaiBreak()">☕ Chai</button>
        <button type="button" class="mascot-action-mini-btn" onclick="event.stopPropagation(); speakMascotQuote('${encodeURIComponent(quote)}')">🔊 Speak</button>
        <button type="button" class="mascot-action-mini-btn" onclick="event.stopPropagation(); blowMascotWhistle()">🚨 Whistle</button>
      </div>
    </div>
    <div class="mascot-avatar-wrapper" title="Aashwas-Babu, Municipal Chief Civic Inspector">
      ${getMascotSVG(currentMascotMood, 72)}
      <div class="mascot-name-badge">Aashwas-Babu</div>
    </div>
  `;
}

function triggerMascotChaiBreak() {
  setMascotMood('happy');
  if (window.civicAudio && typeof window.civicAudio.playClick === 'function') {
    window.civicAudio.playClick();
  }
  const speechText = document.querySelector('.mascot-speech-text');
  if (speechText) {
    speechText.innerHTML = '"Aah, mast cutting chai! ☕ 10-minute break while our 6 autonomous agents keep the city sparkling!"';
  }
  if (typeof showStickerToast === 'function') {
    showStickerToast('☕ Aashwas-Babu is enjoying hot cutting chai with biscuits!', 'info', 2500);
  }
}

function speakMascotQuote(encodedQuote) {
  try {
    const text = decodeURIComponent(encodedQuote);
    if ('speechSynthesis' in window) {
      window.speechSynthesis.cancel();
      const utterance = new SpeechSynthesisUtterance(text);
      utterance.rate = 1.0;
      utterance.lang = 'en-IN';
      window.speechSynthesis.speak(utterance);
    }
  } catch (e) {}
}

function blowMascotWhistle() {
  setMascotMood('inspecting');
  if (window.civicAudio && typeof window.civicAudio.playInspectorWhistle === 'function') {
    window.civicAudio.playInspectorWhistle();
  }
  if (typeof showStickerToast === 'function') {
    showStickerToast('🚨 *FWEEEET!* Municipal Chief Inspector on site! Checking road levels.', 'warning', 2500);
  }
}

function setMascotMood(mood) {
  if (['happy', 'inspecting', 'panicking', 'celebrating', 'confused', 'soaked', 'sweating', 'sleepy'].includes(mood)) {
    currentMascotMood = mood;
    updateMascotDisplay();
  }
}

function cycleMascotMood() {

  const moods = ['happy', 'inspecting', 'celebrating', 'confused', 'soaked', 'panicking'];
  const nextIdx = (moods.indexOf(currentMascotMood) + 1) % moods.length;
  setMascotMood(moods[nextIdx]);
}

function squishMascotElement() {
  const wrapper = document.querySelector('.mascot-avatar-wrapper');
  if (!wrapper) return;
  wrapper.classList.remove('squished');
  void wrapper.offsetWidth; // trigger reflow
  wrapper.classList.add('squished');
}

// 6. Civic Capacity Squish Meter (<40% Roomy, 40-70% Cozy, 70-90% Snug, >90% High Surge)
function updateSquishMeter(pct) {
  const meterVal = Math.min(100, Math.max(5, pct));
  let state = 'cozy';
  let label = 'Cozy';
  let badgeColor = 'var(--mustard)';
  let commentary = 'Comfortable maintenance capacity. Field squads running on schedule!';

  if (meterVal < 40) {
    state = 'roomy';
    label = 'Roomy';
    badgeColor = 'var(--mint)';
    commentary = 'Plentiful maintenance crew capacity across all municipal zones.';
  } else if (meterVal <= 70) {
    state = 'cozy';
    label = 'Cozy';
    badgeColor = 'var(--mustard)';
    commentary = 'Healthy urban pulse. Engineers resolving tickets well within SLA guarantees!';
  } else if (meterVal <= 90) {
    state = 'snug';
    label = 'Snug';
    badgeColor = 'var(--peach)';
    commentary = 'High grievance volume! Multi-agent spatial clustering and crew routing active.';
  } else {
    state = 'sardine';
    label = 'High Surge';
    badgeColor = 'var(--tomato)';
    commentary = 'Surge load! Friday Jan Sunwai automatic escalation thresholds active!';
  }

  const barEl = document.getElementById('squish-meter-bar');
  const labelEl = document.getElementById('squish-meter-label');
  const valEl = document.getElementById('squish-meter-val');
  const commentEl = document.getElementById('squish-meter-comment');

  if (barEl) {
    barEl.style.width = `${meterVal}%`;
    barEl.style.backgroundColor = badgeColor;
  }
  if (labelEl) {
    labelEl.innerText = label;
    labelEl.style.backgroundColor = badgeColor;
  }
  if (valEl) valEl.innerText = `${meterVal}%`;
  if (commentEl) commentEl.innerText = commentary;

  // React mascot if surge
  if (state === 'sardine') {
    setMascotMood('panicking');
  } else if (state === 'roomy') {
    setMascotMood('happy');
  }
}

// 7. Font Size Preference (S / M / L)
function initFontSizePreference() {
  const savedSize = localStorage.getItem('sticker_font_size') || 'M';
  setFontSizeChoice(savedSize);
}

function setFontSizeChoice(size) {
  localStorage.setItem('sticker_font_size', size);
  document.querySelectorAll('.font-choice-btn').forEach(btn => {
    btn.classList.toggle('active', btn.getAttribute('data-size') === size);
  });

  if (size === 'S') {
    document.documentElement.style.fontSize = '13px';
  } else if (size === 'L') {
    document.documentElement.style.fontSize = '16.5px';
  } else {
    document.documentElement.style.fontSize = '14.5px';
  }
}

// 8. Sticker Toast Notification System
function showStickerToast(message, type = 'info', duration = 3500) {
  let container = document.getElementById('sticker-toast-container');
  if (!container) {
    container = document.createElement('div');
    container.id = 'sticker-toast-container';
    container.className = 'sticker-toast-container';
    document.body.appendChild(container);
  }

  const toast = document.createElement('div');
  const typeClass = type === 'success' ? 'toast-success' : (type === 'error' ? 'toast-error' : 'toast-info');
  toast.className = `sticker-toast ${typeClass}`;
  
  let icon = '📌';
  if (type === 'success') icon = '🎉';
  else if (type === 'error') icon = '⚠️';
  else if (type === 'info') icon = '🏛️';

  toast.innerHTML = `
    <span style="font-size: 1.2rem;">${icon}</span>
    <span style="flex: 1; line-height: 1.35;">${message}</span>
  `;

  container.appendChild(toast);

  setTimeout(() => {
    toast.style.transition = 'all 0.25s ease';
    toast.style.opacity = '0';
    toast.style.transform = 'translateY(-10px) scale(0.9)';
    setTimeout(() => {
      if (container.contains(toast)) container.removeChild(toast);
    }, 260);
  }, duration);
}

// 9. Sticker Empty State Helper
function getStickerEmptyStateHTML(title = 'All Quiet Across the Wards!', desc = 'No incidents currently match your filter. Grab a cup of chai ☕ — streets are clear!', actionText = null, actionJs = null) {
  const actionButton = actionText && actionJs
    ? `<button class="btn-primary" onclick="${actionJs}" style="margin-top: 10px; font-size: 0.82rem; padding: 6px 16px;">${actionText}</button>`
    : '';

  return `
    <div class="sticker-empty-state">
      <div class="sticker-empty-mascot">
        ${getMascotSVG('happy', 68)}
      </div>
      <div class="sticker-empty-title">${title}</div>
      <div class="sticker-empty-desc">${desc}</div>
      ${actionButton}
    </div>
  `;
}

// Expose on window for global access
window.applySkin = applySkin;
window.applyMotion = applyMotion;
window.setMascotMood = setMascotMood;
window.cycleMascotMood = cycleMascotMood;
window.updateSquishMeter = updateSquishMeter;
window.setFontSizeChoice = setFontSizeChoice;
window.getMascotSVG = getMascotSVG;
window.showStickerToast = showStickerToast;
window.showToast = showStickerToast;
window.getStickerEmptyStateHTML = getStickerEmptyStateHTML;
window.triggerMascotChaiBreak = triggerMascotChaiBreak;
window.speakMascotQuote = speakMascotQuote;
window.blowMascotWhistle = blowMascotWhistle;

