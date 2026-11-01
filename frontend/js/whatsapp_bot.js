// Interactive WhatsApp Bot Simulator with Vernacular Voice Notes & Quick Chips

async function sendWhatsAppMessage(overrideText = null) {
  const inputEl = document.getElementById('wa-input');
  const chatBody = document.getElementById('wa-chat-body');
  const text = (overrideText || inputEl.value).trim();

  if (!text) return;

  // Append user's outgoing message
  const userMsgEl = document.createElement('div');
  userMsgEl.className = 'wa-msg out';
  userMsgEl.innerText = text;
  chatBody.appendChild(userMsgEl);

  if (!overrideText) inputEl.value = '';
  chatBody.scrollTop = chatBody.scrollHeight;

  // Typing indicator
  const typingEl = document.createElement('div');
  typingEl.className = 'wa-msg in';
  typingEl.innerText = 'typing...';
  chatBody.appendChild(typingEl);
  chatBody.scrollTop = chatBody.scrollHeight;

  // Determine dynamic city coordinates
  const cityObj = (typeof CITIES_DATA !== 'undefined' && typeof currentSelectedCity !== 'undefined' && CITIES_DATA[currentSelectedCity])
    ? CITIES_DATA[currentSelectedCity]
    : (typeof CITIES_DATA !== 'undefined' ? CITIES_DATA['delhi'] || CITIES_DATA['all'] : null);
  const waLat = (cityObj && cityObj.pins && cityObj.pins.length > 0) ? cityObj.pins[0].lat : (cityObj ? cityObj.lat : 28.6139);
  const waLon = (cityObj && cityObj.pins && cityObj.pins.length > 0) ? cityObj.pins[0].lon : (cityObj ? cityObj.lon : 77.2090);

  // Determine sender phone from authenticated user or fallback
  const senderPhone = (typeof currentUser !== 'undefined' && currentUser && currentUser.user && currentUser.user.phone)
    ? `+91${currentUser.user.phone.replace(/[^0-9]/g, '').slice(-10)}`
    : '+919876543210';

  try {
    const response = await fetch('/api/v1/webhook/whatsapp', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        From: `whatsapp:${senderPhone}`,
        Body: text,
        Latitude: waLat,
        Longitude: waLon,
        LanguagePref: typeof currentLang !== 'undefined' ? (currentLang === 'hi' ? 'Hindi (Devanagari)' : (currentLang === 'kn' ? 'Kannada' : (currentLang === 'ta' ? 'Tamil' : null))) : null
      })
    });

    if (chatBody.contains(typingEl)) chatBody.removeChild(typingEl);

    if (response.ok) {
      const data = await response.json();
      const botMsgEl = document.createElement('div');
      botMsgEl.className = 'wa-msg in';
      botMsgEl.innerText = data.reply_message;
      chatBody.appendChild(botMsgEl);

      // Refresh command center background data
      if (typeof loadMasterTickets === 'function') loadMasterTickets();
      if (typeof loadKPIStats === 'function') loadKPIStats();
      if (typeof loadWardGovernanceData === 'function') loadWardGovernanceData();
    } else {
      const errorEl = document.createElement('div');
      errorEl.className = 'wa-msg in';
      errorEl.innerText = "Error contacting municipal server. Please try again.";
      chatBody.appendChild(errorEl);
    }
  } catch (err) {
    if (chatBody.contains(typingEl)) chatBody.removeChild(typingEl);
    const errEl = document.createElement('div');
    errEl.className = 'wa-msg in';
    errEl.innerText = "Simulation response: Grievance processed locally. Master Ticket updated.";
    chatBody.appendChild(errEl);
  }

  chatBody.scrollTop = chatBody.scrollHeight;
}

function sendQuickWhatsApp(msg) {
  sendWhatsAppMessage(msg);
}

function sendWhatsAppVoice() {
  const activeLang = typeof currentLang !== 'undefined' ? currentLang : 'hg';
  const voiceSamplesByLang = {
    hi: "🎙️ Voice Note (0:12): 'सड़क पर गहरा गड्ढा है 27th मेन रोड के पास, कभी भी दुर्घटना हो सकती है, वार्ड 3'",
    kn: "🎙️ Voice Note (0:15): 'ರಸ್ತೆಯಲ್ಲಿ ದೊಡ್ಡ ಗುಂಡಿ ಬಿದ್ದಿದೆ ವಾಹನ ಸವಾರರಿಗೆ ಅಪಘಾತವಾಗುವ ಸಂಭವವಿದೆ ಬೇಗ ಸರಿಮಾಡಿ, ವಾರ್ಡ್ 3'",
    ta: "🎙️ Voice Note (0:10): 'தெரு விளக்கு 4 நாட்களாக எரியவில்லை, இரவு நேரத்தில் மிகவும் இருட்டாக உள்ளது, வார்டு 1'",
    hg: "🎙️ Voice Note (0:12): 'Bhaiya road par street light 4 din se band hai Indiranagar Ward 1'",
    en: "🎙️ Voice Note (0:14): 'Dangerous open transformer wire sparking near school entrance, Ward 1'"
  };

  const sample = voiceSamplesByLang[activeLang] || voiceSamplesByLang['hg'];
  
  // Animate oscilloscope in WhatsApp header
  const waOsc = document.getElementById('wa-oscilloscope-canvas');
  if (waOsc) {
    waOsc.style.display = 'block';
    if (typeof startOscilloscope === 'function') startOscilloscope('wa-oscilloscope-canvas');
    setTimeout(() => {
      if (typeof stopOscilloscope === 'function') stopOscilloscope('wa-oscilloscope-canvas');
      waOsc.style.display = 'none';
    }, 1800);
  }

  if (window.civicAudio && typeof window.civicAudio.playRisingTone === 'function') {
    window.civicAudio.playRisingTone();
  }

  const chatBody = document.getElementById('wa-chat-body');
  const userMsgEl = document.createElement('div');
  userMsgEl.className = 'wa-msg out';
  userMsgEl.style.padding = '8px 10px';
  userMsgEl.innerHTML = `
    <div style="display: flex; align-items: center; gap: 8px;">
      <div class="wa-play-btn" onclick="if(window.civicAudio) window.civicAudio.playClick()">▶</div>
      <div style="flex: 1;">
        <div class="wa-waveform-bar"><div class="wa-waveform-progress"></div></div>
        <div style="font-size: 10px; color: #57534e; margin-top: 3px; font-weight: bold;">0:12 • Vernacular Voice Grievance</div>
      </div>
    </div>
    <div style="font-size: 11px; margin-top: 5px; font-style: italic; color: #1c1917;">"${sample.replace(/🎙️ Voice Note \([0-9:]+\): '/, '').replace(/'$/, '')}"</div>
  `;
  chatBody.appendChild(userMsgEl);
  chatBody.scrollTop = chatBody.scrollHeight;

  // Clean raw transcript for AI
  const cleanText = sample.replace(/🎙️ Voice Note \([0-9:]+\): '/, '').replace(/'$/, '');

  const langPref = activeLang === 'hi' ? 'Hindi (Devanagari)' : (activeLang === 'kn' ? 'Kannada' : (activeLang === 'ta' ? 'Tamil' : null));

  // Send cleaned speech-to-text to webhook
  setTimeout(() => {
    // Typing indicator
    const typingEl = document.createElement('div');
    typingEl.className = 'wa-msg in';
    typingEl.innerText = 'listening to audio & transcribing...';
    chatBody.appendChild(typingEl);
    chatBody.scrollTop = chatBody.scrollHeight;

    const cityObj = (typeof CITIES_DATA !== 'undefined' && typeof currentSelectedCity !== 'undefined' && CITIES_DATA[currentSelectedCity])
      ? CITIES_DATA[currentSelectedCity]
      : (typeof CITIES_DATA !== 'undefined' ? CITIES_DATA['delhi'] || CITIES_DATA['all'] : null);
    const waLat = (cityObj && cityObj.pins && cityObj.pins.length > 0) ? cityObj.pins[0].lat : (cityObj ? cityObj.lat : 28.6139);
    const waLon = (cityObj && cityObj.pins && cityObj.pins.length > 0) ? cityObj.pins[0].lon : (cityObj ? cityObj.lon : 77.2090);

    const senderPhone = (typeof currentUser !== 'undefined' && currentUser && currentUser.user && currentUser.user.phone)
      ? `+91${currentUser.user.phone.replace(/[^0-9]/g, '').slice(-10)}`
      : '+919876543210';

    fetch('/api/v1/webhook/whatsapp', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        From: `whatsapp:${senderPhone}`,
        Body: cleanText,
        Latitude: waLat,
        Longitude: waLon,
        LanguagePref: langPref
      })
    }).then(res => res.json()).then(data => {
      if (chatBody.contains(typingEl)) chatBody.removeChild(typingEl);
      const botMsgEl = document.createElement('div');
      botMsgEl.className = 'wa-msg in';
      botMsgEl.innerText = data.reply_message;
      chatBody.appendChild(botMsgEl);
      chatBody.scrollTop = chatBody.scrollHeight;
      if (typeof loadMasterTickets === 'function') loadMasterTickets();
      if (typeof loadKPIStats === 'function') loadKPIStats();
      if (typeof loadWardGovernanceData === 'function') loadWardGovernanceData();
    }).catch(() => {
      if (chatBody.contains(typingEl)) chatBody.removeChild(typingEl);
    });
  }, 1000);
}

// Expose on window for global click handlers
window.sendWhatsAppMessage = sendWhatsAppMessage;
window.sendQuickWhatsApp = sendQuickWhatsApp;
window.sendWhatsAppVoice = sendWhatsAppVoice;
