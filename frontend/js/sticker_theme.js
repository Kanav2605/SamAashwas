/**
 * CampusHop / SamAashwas - Sticker Book Bus Stop Theme Engine
 * Features:
 * - Floating background SVG objects with parallax drift & density control (Chaos 22, Normal 14, Calm 7, Off 0)
 * - 4 Light Skins (Tomato Toast [default], Mint Gelato, Bubblegum Pop, Mustard Mayhem)
 * - Motion setting (Chaos, Normal, Calm, Off)
 * - Goofy Mascot ("Aashwas-Babu") with googly eyes & 4 expressions (happy, panicking, celebrating, confused)
 * - Squish Meter (<40% Roomy, 40-70% Cozy, 70-90% Snug, >90% Sardine Mode)
 * - Font Size Setting (S / M / L)
 */

// Mascot Goofy Sayings for Civic Awareness
const MASCOT_QUOTES = {
  happy: [
    "Hop on! Our 6 AI agents are sorting complaints faster than hot samosas!",
    "Road repaired in record time! Citizen smiles guaranteed! 🎉",
    "Everything running smoothly! Fresh paper, fresh resolutions!",
    "Look at that resolution rate! Swachh Bharat in high gear!"
  ],
  panicking: [
    "Aiyo! Pothole alert! Hold on tight to the bus handle!",
    "Transformer wire sparking! Alerting rapid ward engineer squad stat!",
    "Monsoon cloud spotted! Dewatering pumps rolling out!",
    "Sardine Mode activated! High grievance traffic incoming!"
  ],
  celebrating: [
    "Balle Balle! 100 Karma points unlocked for clean streets!",
    "Jan Sunwai docket resolved before the Commissioner!",
    "Sticker badge awarded! You're a certified Swachh Nagrik!",
    "Clean street verified! Slap a gold star on that ward!"
  ],
  confused: [
    "Arre, is that a pothole or a swimming pool? Checking vision AI...",
    "Wait, that's a selfie meme, not a sewer leak! Fraud shield blocked it!",
    "Searching the municipal docket... Where did that permit go?",
    "Need coordinates! Tap a city pin to guide the bus!"
  ]
};

// 11 Flat SVG Floating Objects (Section 7)
const SVG_OBJECTS = {
  'mini-bus': `
    <svg viewBox="0 0 48 36" width="100%" height="100%" fill="none" xmlns="http://www.w3.org/2000/svg">
      <rect x="3" y="6" width="42" height="22" rx="6" fill="#FFC93C" stroke="#231F20" stroke-width="2.5"/>
      <rect x="7" y="10" width="8" height="8" rx="2" fill="#FFFDF7" stroke="#231F20" stroke-width="2"/>
      <rect x="18" y="10" width="8" height="8" rx="2" fill="#FFFDF7" stroke="#231F20" stroke-width="2"/>
      <rect x="29" y="10" width="12" height="8" rx="2" fill="#7BDCB5" stroke="#231F20" stroke-width="2"/>
      <circle cx="12" cy="28" r="4.5" fill="#231F20"/>
      <circle cx="12" cy="28" r="2" fill="#FFFDF7"/>
      <circle cx="36" cy="28" r="4.5" fill="#231F20"/>
      <circle cx="36" cy="28" r="2" fill="#FFFDF7"/>
      <rect x="42" y="18" width="3" height="4" rx="1" fill="#FF5A4E" stroke="#231F20" stroke-width="1.5"/>
    </svg>`,
  
  'cone': `
    <svg viewBox="0 0 36 36" width="100%" height="100%" fill="none" xmlns="http://www.w3.org/2000/svg">
      <ellipse cx="18" cy="30" rx="13" ry="3.5" fill="#FF5A4E" stroke="#231F20" stroke-width="2.5"/>
      <polygon points="18,4 8,29 28,29" fill="#FF5A4E" stroke="#231F20" stroke-width="2.5"/>
      <polygon points="18,12 12,23 24,23" fill="#FFFDF7" stroke="#231F20" stroke-width="2"/>
    </svg>`,

  'road-sign': `
    <svg viewBox="0 0 36 40" width="100%" height="100%" fill="none" xmlns="http://www.w3.org/2000/svg">
      <line x1="18" y1="20" x2="18" y2="38" stroke="#231F20" stroke-width="3"/>
      <rect x="5" y="4" width="26" height="22" rx="4" fill="#FFC93C" stroke="#231F20" stroke-width="2.5"/>
      <path d="M12 17 L18 10 L24 17" stroke="#231F20" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
      <line x1="18" y1="13" x2="18" y2="21" stroke="#231F20" stroke-width="2.5" stroke-linecap="round"/>
    </svg>`,

  'pothole-marker': `
    <svg viewBox="0 0 36 36" width="100%" height="100%" fill="none" xmlns="http://www.w3.org/2000/svg">
      <ellipse cx="18" cy="22" rx="14" ry="7" fill="#231F20"/>
      <ellipse cx="18" cy="20" rx="12" ry="5.5" fill="#FFB88A" stroke="#231F20" stroke-width="2"/>
      <path d="M18 5 L18 16" stroke="#FF5A4E" stroke-width="3" stroke-linecap="round"/>
      <circle cx="18" cy="5" r="3" fill="#FF5A4E" stroke="#231F20" stroke-width="2"/>
    </svg>`,

  'tree': `
    <svg viewBox="0 0 36 42" width="100%" height="100%" fill="none" xmlns="http://www.w3.org/2000/svg">
      <rect x="15" y="24" width="6" height="15" fill="#FFB88A" stroke="#231F20" stroke-width="2.5" rx="2"/>
      <circle cx="18" cy="16" r="13" fill="#7BDCB5" stroke="#231F20" stroke-width="2.5"/>
      <circle cx="13" cy="13" r="2.5" fill="#FFFDF7"/>
    </svg>`,

  'coffee-cup': `
    <svg viewBox="0 0 36 36" width="100%" height="100%" fill="none" xmlns="http://www.w3.org/2000/svg">
      <rect x="7" y="11" width="18" height="18" rx="4" fill="#FFFDF7" stroke="#231F20" stroke-width="2.5"/>
      <path d="M25 15 C29 15 30 22 25 23" fill="none" stroke="#231F20" stroke-width="2.5" stroke-linecap="round"/>
      <path d="M11 7 C11 5 13 4 13 2" stroke="#FF5A4E" stroke-width="2" stroke-linecap="round"/>
      <path d="M16 7 C16 5 18 4 18 2" stroke="#FF5A4E" stroke-width="2" stroke-linecap="round"/>
      <rect x="9" y="16" width="14" height="6" rx="2" fill="#FFC93C" stroke="#231F20" stroke-width="1.5"/>
    </svg>`,

  'donut': `
    <svg viewBox="0 0 36 36" width="100%" height="100%" fill="none" xmlns="http://www.w3.org/2000/svg">
      <circle cx="18" cy="18" r="14" fill="#FF9EC4" stroke="#231F20" stroke-width="2.5"/>
      <circle cx="18" cy="18" r="5" fill="#FFF6E5" stroke="#231F20" stroke-width="2.5"/>
      <rect x="12" y="10" width="3" height="1.5" rx="0.75" fill="#FFC93C"/>
      <rect x="21" y="9" width="3" height="1.5" rx="0.75" fill="#7BDCB5"/>
      <rect x="23" y="19" width="3" height="1.5" rx="0.75" fill="#FFFDF7"/>
      <rect x="11" y="22" width="3" height="1.5" rx="0.75" fill="#B8A6FF"/>
    </svg>`,

  'star': `
    <svg viewBox="0 0 36 36" width="100%" height="100%" fill="none" xmlns="http://www.w3.org/2000/svg">
      <polygon points="18,3 22.5,12 32.5,13.5 25,20.8 26.8,30.8 18,26 9.2,30.8 11,20.8 3.5,13.5 13.5,12" 
               fill="#FFC93C" stroke="#231F20" stroke-width="2.5" stroke-linejoin="round"/>
      <circle cx="15" cy="17" r="1.5" fill="#231F20"/>
      <circle cx="21" cy="17" r="1.5" fill="#231F20"/>
      <path d="M16 21 Q18 23 20 21" stroke="#231F20" stroke-width="1.5" stroke-linecap="round"/>
    </svg>`,

  'cloud': `
    <svg viewBox="0 0 42 30" width="100%" height="100%" fill="none" xmlns="http://www.w3.org/2000/svg">
      <path d="M10 24 C5 24 3 20 5 16 C4 11 9 8 14 9 C17 4 25 4 28 8 C33 7 38 11 37 16 C40 19 39 24 33 24 Z" 
            fill="#FFFDF7" stroke="#231F20" stroke-width="2.5" stroke-linejoin="round"/>
      <circle cx="17" cy="17" r="1.5" fill="#231F20"/>
      <circle cx="25" cy="17" r="1.5" fill="#231F20"/>
      <path d="M19 20 Q21 22 23 20" stroke="#231F20" stroke-width="1.5" stroke-linecap="round"/>
    </svg>`,

  'sun': `
    <svg viewBox="0 0 36 36" width="100%" height="100%" fill="none" xmlns="http://www.w3.org/2000/svg">
      <circle cx="18" cy="18" r="9" fill="#FFC93C" stroke="#231F20" stroke-width="2.5"/>
      <line x1="18" y1="3" x2="18" y2="6" stroke="#231F20" stroke-width="2.5" stroke-linecap="round"/>
      <line x1="18" y1="30" x2="18" y2="33" stroke="#231F20" stroke-width="2.5" stroke-linecap="round"/>
      <line x1="3" y1="18" x2="6" y2="18" stroke="#231F20" stroke-width="2.5" stroke-linecap="round"/>
      <line x1="30" y1="18" x2="33" y2="18" stroke="#231F20" stroke-width="2.5" stroke-linecap="round"/>
      <line x1="7.4" y1="7.4" x2="9.5" y2="9.5" stroke="#231F20" stroke-width="2.5" stroke-linecap="round"/>
      <line x1="26.5" y1="26.5" x2="28.6" y2="28.6" stroke="#231F20" stroke-width="2.5" stroke-linecap="round"/>
      <line x1="7.4" y1="28.6" x2="9.5" y2="26.5" stroke="#231F20" stroke-width="2.5" stroke-linecap="round"/>
      <line x1="26.5" y1="9.5" x2="28.6" y2="7.4" stroke="#231F20" stroke-width="2.5" stroke-linecap="round"/>
      <circle cx="15" cy="16" r="1.5" fill="#231F20"/>
      <circle cx="21" cy="16" r="1.5" fill="#231F20"/>
      <path d="M16 19 Q18 21 20 19" stroke="#231F20" stroke-width="1.5" stroke-linecap="round"/>
    </svg>`,

  'lightbulb': `
    <svg viewBox="0 0 36 40" width="100%" height="100%" fill="none" xmlns="http://www.w3.org/2000/svg">
      <path d="M11 16 C11 11 14 7 18 7 C22 7 25 11 25 16 C25 20 22 22 22 25 L14 25 C14 22 11 20 11 16 Z" 
            fill="#FFC93C" stroke="#231F20" stroke-width="2.5"/>
      <rect x="14" y="25" width="8" height="5" fill="#FFFDF7" stroke="#231F20" stroke-width="2"/>
      <path d="M15 30 L21 30 L19 33 L17 33 Z" fill="#231F20"/>
      <line x1="16" y1="14" x2="16" y2="18" stroke="#231F20" stroke-width="1.5"/>
      <line x1="20" y1="14" x2="20" y2="18" stroke="#231F20" stroke-width="1.5"/>
      <line x1="16" y1="18" x2="20" y2="18" stroke="#231F20" stroke-width="1.5"/>
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
let currentMotion = localStorage.getItem('sticker_motion') || 'normal';
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
  bgEl.innerHTML = '';

  const count = DENSITY_MAP[currentMotion] || 0;
  if (count === 0) return;

  // Distribute objects across screen
  for (let i = 0; i < count; i++) {
    const objType = OBJECT_KEYS[i % OBJECT_KEYS.length];
    const wrapper = document.createElement('div');
    wrapper.className = 'floating-sticker-item';
    
    // Spread evenly with slight randomness
    const leftPct = (i * (100 / count) + (Math.random() * 5)) % 96 + 2;
    const topPct = (Math.sin(i * 1.3) * 40 + 48 + (Math.random() * 8)) % 92 + 3;
    const size = Math.floor(Math.random() * 18 + 36); // 36px to 54px
    const duration = Math.floor(Math.random() * 10 + 12); // 12s - 22s drift
    const delay = -(Math.random() * 15).toFixed(1);
    const tilt = ((Math.random() * 24) - 12).toFixed(1); // -12 to +12 deg tilt

    wrapper.style.left = `${leftPct}%`;
    wrapper.style.top = `${topPct}%`;
    wrapper.style.width = `${size}px`;
    wrapper.style.height = `${size}px`;
    wrapper.style.animationDuration = `${duration}s`;
    wrapper.style.animationDelay = `${delay}s`;
    wrapper.style.setProperty('--rot-tilt', `${tilt}deg`);
    
    wrapper.innerHTML = SVG_OBJECTS[objType];
    bgEl.appendChild(wrapper);
  }
}

// 4. Mascot Goofy Avatar Generator
function getMascotSVG(expression = 'happy', size = 64) {
  // Googly Eyes & Expression Paths
  let mouthHtml = `<path d="M19 28 Q24 33 29 28" stroke="#231F20" stroke-width="2.5" stroke-linecap="round" fill="#FF5A4E"/>`;
  let leftEyePupil = `<circle cx="16" cy="18" r="3" fill="#231F20"/>`;
  let rightEyePupil = `<circle cx="32" cy="18" r="3" fill="#231F20"/>`;
  let extraAccessories = ``;

  if (expression === 'panicking') {
    mouthHtml = `
      <path d="M17 30 Q21 26 24 30 Q27 34 31 30" stroke="#231F20" stroke-width="2.5" fill="none" stroke-linecap="round"/>
      <ellipse cx="24" cy="31" rx="2" ry="1.5" fill="#FFFDF7"/>
    `;
    leftEyePupil = `<circle cx="17.5" cy="17" r="1.8" fill="#231F20"/>`;
    rightEyePupil = `<circle cx="30.5" cy="17" r="1.8" fill="#231F20"/>`;
    extraAccessories = `
      <!-- Sweat drops -->
      <path d="M38 12 Q39 8 41 12 Q42 15 39 15 Q37 15 38 12 Z" fill="#7BDCB5" stroke="#231F20" stroke-width="1.5"/>
    `;
  } else if (expression === 'celebrating') {
    mouthHtml = `
      <path d="M17 26 Q24 36 31 26 Z" stroke="#231F20" stroke-width="2.5" fill="#FF5A4E"/>
      <path d="M21 31 Q24 34 27 31" stroke="#FFFDF7" stroke-width="2" stroke-linecap="round"/>
    `;
    leftEyePupil = `
      <polygon points="16,15 17.5,18 20.5,18 18,20 19,23 16,21.5 13,23 14,20 11.5,18 14.5,18" fill="#FFC93C" stroke="#231F20" stroke-width="1"/>
    `;
    rightEyePupil = `
      <polygon points="32,15 33.5,18 36.5,18 34,20 35,23 32,21.5 29,23 30,20 27.5,18 30.5,18" fill="#FFC93C" stroke="#231F20" stroke-width="1"/>
    `;
    extraAccessories = `
      <!-- Party Conductor Hat -->
      <polygon points="18,4 30,4 24,-5" fill="#FF9EC4" stroke="#231F20" stroke-width="2"/>
      <circle cx="24" cy="-5" r="2.5" fill="#FFC93C" stroke="#231F20" stroke-width="1.5"/>
      <circle cx="41" cy="5" r="2" fill="#B8A6FF"/>
      <circle cx="7" cy="6" r="2" fill="#FFC93C"/>
    `;
  } else if (expression === 'confused') {
    mouthHtml = `
      <path d="M19 30 L29 27" stroke="#231F20" stroke-width="2.5" stroke-linecap="round"/>
    `;
    leftEyePupil = `<circle cx="14" cy="16" r="3.5" fill="#231F20"/>`;
    rightEyePupil = `<circle cx="34" cy="20" r="2" fill="#231F20"/>`;
    extraAccessories = `
      <!-- Raised Eyebrow & Question Mark -->
      <path d="M11 12 Q16 9 20 13" stroke="#231F20" stroke-width="2.5" stroke-linecap="round" fill="none"/>
      <text x="36" y="8" font-family="'Fredoka', sans-serif" font-weight="800" font-size="14" fill="#FF5A4E">?</text>
    `;
  }

  return `
    <svg viewBox="-5 -8 58 58" width="${size}" height="${size}" fill="none" xmlns="http://www.w3.org/2000/svg" class="mascot-svg mascot-${expression}">
      <!-- Bus Body / Face -->
      <rect x="4" y="6" width="40" height="34" rx="12" fill="#FFC93C" stroke="#231F20" stroke-width="3"/>
      <!-- Roof Visor / Cap -->
      <path d="M8 6 Q24 2 40 6" stroke="#231F20" stroke-width="3" fill="#FF5A4E"/>
      <rect x="10" y="2" width="28" height="5" rx="2" fill="#FF5A4E" stroke="#231F20" stroke-width="2.5"/>
      <!-- Headlights / Cheeks -->
      <circle cx="10" cy="30" r="4" fill="#FF9EC4" stroke="#231F20" stroke-width="2"/>
      <circle cx="38" cy="30" r="4" fill="#FF9EC4" stroke="#231F20" stroke-width="2"/>
      
      <!-- Googly Eye Sockets -->
      <circle cx="16" cy="18" r="8" fill="#FFFDF7" stroke="#231F20" stroke-width="2.5"/>
      <circle cx="32" cy="18" r="8" fill="#FFFDF7" stroke="#231F20" stroke-width="2.5"/>
      
      <!-- Pupils -->
      ${leftEyePupil}
      ${rightEyePupil}
      
      <!-- Mouth -->
      ${mouthHtml}

      <!-- Tiny Bus Wheels on bottom -->
      <rect x="8" y="38" width="8" height="6" rx="3" fill="#231F20"/>
      <rect x="32" y="38" width="8" height="6" rx="3" fill="#231F20"/>
      
      <!-- Goofy Accessories -->
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
      <div class="mascot-speech-hint">Click me to change mood! 🚌</div>
    </div>
    <div class="mascot-avatar-wrapper" title="Aashwas-Babu, Your Civic Transit Guide">
      ${getMascotSVG(currentMascotMood, 72)}
      <div class="mascot-name-badge">Aashwas-Babu</div>
    </div>
  `;
}

function setMascotMood(mood) {
  if (['happy', 'panicking', 'celebrating', 'confused'].includes(mood)) {
    currentMascotMood = mood;
    updateMascotDisplay();
  }
}

function cycleMascotMood() {
  const moods = ['happy', 'celebrating', 'confused', 'panicking'];
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

// 6. Squish Meter Engine (<40% Roomy, 40-70% Cozy, 70-90% Snug, >90% Sardine Mode)
function updateSquishMeter(pct) {
  const meterVal = Math.min(100, Math.max(5, pct));
  let state = 'cozy';
  let label = 'Cozy';
  let badgeColor = 'var(--mustard)';
  let commentary = 'Comfortable capacity. Wards running on schedule!';

  if (meterVal < 40) {
    state = 'roomy';
    label = 'Roomy';
    badgeColor = 'var(--mint)';
    commentary = 'Hop on! Plenty of free capacity across all wards.';
  } else if (meterVal <= 70) {
    state = 'cozy';
    label = 'Cozy';
    badgeColor = 'var(--mustard)';
    commentary = 'Healthy urban pulse. Engineers resolving tickets in time!';
  } else if (meterVal <= 90) {
    state = 'snug';
    label = 'Snug';
    badgeColor = 'var(--peach)';
    commentary = 'Heavy traffic! Multi-agent spatial clustering active.';
  } else {
    state = 'sardine';
    label = 'Sardine Mode';
    badgeColor = 'var(--tomato)';
    commentary = 'Packed to the gills! Friday Jan Sunwai docket escalations triggered!';
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

  // React mascot if high
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

// 8. Sticker Toast Notification System (Section 6.5)
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
  else if (type === 'info') icon = '🚌';

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

// 9. Sticker Empty State Helper (Section 6.5)
function getStickerEmptyStateHTML(title = 'All Quiet on the Bus Stop!', desc = 'No incidents currently match your filter. Grab a cup of chai ☕ and enjoy the ride!', actionText = null, actionJs = null) {
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
