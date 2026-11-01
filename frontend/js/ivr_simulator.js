// Jan Sunwai 1913 Toll-Free Vernacular IVR Phone Gateway Simulator
// Dial 1913 telephone simulation, DTMF keypad audio, and Bhashini speech-to-text ticket intake

let ivrDialBuffer = '';
let isIVRCallActive = false;

function openIVRModal() {
  const modal = document.getElementById('ivr-phone-modal');
  if (!modal) return;
  modal.classList.add('active');
  ivrDialBuffer = '1913';
  updateIVRDisplay();

  if (window.civicAudio && typeof window.civicAudio.playRisingTone === 'function') {
    window.civicAudio.playRisingTone();
  }
}

function closeIVRModal() {
  const modal = document.getElementById('ivr-phone-modal');
  if (modal) modal.classList.remove('active');
  hangupIVRCall();
  if (window.civicAudio && typeof window.civicAudio.playClick === 'function') {
    window.civicAudio.playClick();
  }
}

function pressKeypad(digit) {
  if (ivrDialBuffer.length < 12) {
    ivrDialBuffer += digit;
    updateIVRDisplay();
  }

  // Synthesize DTMF touch-tone frequency
  if (window.civicAudio && window.civicAudio.ctx) {
    playDTMFTone(digit);
  }
}

function clearKeypad() {
  ivrDialBuffer = '';
  updateIVRDisplay();
}

function updateIVRDisplay() {
  const disp = document.getElementById('ivr-number-display');
  if (disp) disp.innerText = ivrDialBuffer || 'Enter Number...';
}

function playDTMFTone(digit) {
  try {
    const ctx = window.civicAudio.ctx;
    if (ctx.state === 'suspended') ctx.resume();

    const dtmfFreqs = {
      '1': [697, 1209], '2': [697, 1336], '3': [697, 1477],
      '4': [770, 1209], '5': [770, 1336], '6': [770, 1477],
      '7': [852, 1209], '8': [852, 1336], '9': [852, 1477],
      '*': [941, 1209], '0': [941, 1336], '#': [941, 1477]
    };

    const freqs = dtmfFreqs[digit] || [770, 1336];
    const now = ctx.currentTime;

    const osc1 = ctx.createOscillator();
    const osc2 = ctx.createOscillator();
    const gain = ctx.createGain();

    osc1.frequency.setValueAtTime(freqs[0], now);
    osc2.frequency.setValueAtTime(freqs[1], now);

    gain.gain.setValueAtTime(0.08, now);
    gain.gain.exponentialRampToValueAtTime(0.0001, now + 0.14);

    osc1.connect(gain);
    osc2.connect(gain);
    gain.connect(ctx.destination);

    osc1.start(now);
    osc2.start(now);
    osc1.stop(now + 0.15);
    osc2.stop(now + 0.15);
  } catch (e) {
    // Audio fallback
  }
}

function startIVRCall() {
  isIVRCallActive = true;
  const statusEl = document.getElementById('ivr-call-status');
  const actionPanel = document.getElementById('ivr-active-call-panel');
  const keypad = document.getElementById('ivr-keypad-grid');

  if (statusEl) {
    statusEl.innerHTML = `<span style="color: #059669; font-weight: 900;">🟢 Connected to Municipal Toll-Free 1913</span><br><span style="font-size: 0.72rem; color: var(--text-muted);">"Namaste! SamAashwas Jan Sunwai mein aapka swagat hai. Apni bhasha mein samasya batayein."</span>`;
  }
  if (actionPanel) actionPanel.style.display = 'block';
  if (keypad) keypad.style.opacity = '0.6';

  if (window.civicAudio && typeof window.civicAudio.playRisingTone === 'function') {
    window.civicAudio.playRisingTone();
  }
}

function hangupIVRCall() {
  isIVRCallActive = false;
  const statusEl = document.getElementById('ivr-call-status');
  const actionPanel = document.getElementById('ivr-active-call-panel');
  const keypad = document.getElementById('ivr-keypad-grid');

  if (statusEl) statusEl.innerText = 'Call Ended • Dial 1913 for National Jan Sunwai';
  if (actionPanel) actionPanel.style.display = 'none';
  if (keypad) keypad.style.opacity = '1';
}

async function simulateIVRSpeechSubmission(dialect) {
  const samples = {
    'bhojpuri': "अरे भैया, हमार वार्ड में तीन दिन से बिजली के तार लटकल बा, कवनो भी समय अनहोनी हो जाई, जल्दी ठीक करवा दीं!",
    'awadhi': "सड़किया पे भारी गढ्ढा होइ गवा है पानी भरल बा, गाड़ी गिरत हई, तुरंत मरम्मत कराओ!",
    'kannada': "ನಮ್ಮ ಬಡಾವಣೆಯಲ್ಲಿ ಕಸದ ಗಾಡಿ ಬಂದಿಲ್ಲ, ರಸ್ತೆಯಲ್ಲಿ ಕಸ ತುಂಬಿದೆ ಬೇಗನೆ ತೆರವುಗೊಳಿಸಿ!",
    'marathi': "रस्त्यावर मोठा खड्डा पडला आहे आणि गटाराचे पाणी वाहत आहे, कृपया त्वरित लक्ष द्या!",
    'hindi': "वार्ड 12 में सीवर का ढक्कन खुला है, बदबू फैल रही है और बच्चे खेल रहे हैं, तुरंत बंद करवाएं!"
  };

  const text = samples[dialect] || samples['hindi'];
  const transcriptEl = document.getElementById('ivr-transcript-readout');
  if (transcriptEl) transcriptEl.innerText = `🎙️ [Bhashini Speech-to-Text (${dialect.toUpperCase()})]: "${text}"`;

  if (window.civicAudio && typeof window.civicAudio.playBubblePop === 'function') {
    window.civicAudio.playBubblePop();
  }

  // Submit via voice-note API
  try {
    const lat = 12.9716;
    const lon = 77.5946;
    const res = await fetch('/api/v1/complaints/voice-note', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        spoken_language: dialect === 'kannada' ? 'kn-IN' : (dialect === 'marathi' ? 'mr-IN' : 'hi-IN'),
        audio_transcript: text,
        lat: lat,
        lon: lon,
        citizen_name: "1913 Citizen Caller",
        citizen_phone: "9876543210"
      })
    });

    if (res.ok) {
      const data = await res.json();
      if (transcriptEl) {
        transcriptEl.innerHTML += `<br><span style="color: #059669; font-weight: 800;">✅ Master Ticket Generated: ${data.master_ticket_id} (Assigned: ${data.department})</span>`;
      }
      if (window.civicCelebration) window.civicCelebration.fireMarigoldPetals();
      if (window.civicAudio) window.civicAudio.playCelebrationFanfare();
      if (typeof loadMasterTickets === 'function') loadMasterTickets();
    }
  } catch (err) {
    console.error("IVR submission failed:", err);
  }
}

// Expose globals
window.openIVRModal = openIVRModal;
window.closeIVRModal = closeIVRModal;
window.pressKeypad = pressKeypad;
window.clearKeypad = clearKeypad;
window.startIVRCall = startIVRCall;
window.hangupIVRCall = hangupIVRCall;
window.simulateIVRSpeechSubmission = simulateIVRSpeechSubmission;
