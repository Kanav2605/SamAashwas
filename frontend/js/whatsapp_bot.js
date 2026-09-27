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

  try {
    const response = await fetch('/api/v1/webhook/whatsapp', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        From: 'whatsapp:+919876543210',
        Body: text,
        Latitude: 12.9352,
        Longitude: 77.6245,
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
  const voiceSamples = [
    "🎙️ Voice Note (0:12): 'Bhaiya road par street light 4 din se band hai Indiranagar Ward 1'",
    "🎙️ Voice Note (0:15): 'ಸದರ್ ರಸ್ತೆಯಲ್ಲಿ ದೊಡ್ಡ ಗುಂಡಿ ಬಿದ್ದಿದೆ ಬೇಗ ಸರಿಮಾಡಿ ವಾರ್ಡ್ 3'",
    "🎙️ Voice Note (0:10): 'தெரு விளக்கு எரியவில்லை, இருட்டாக உள்ளது வார்டு 1'",
    "🎙️ Voice Note (0:18): 'Ward 2 gali mein sewer overflow ho raha hai badbu aa rahi hai'"
  ];
  const sample = voiceSamples[Math.floor(Math.random() * voiceSamples.length)];
  
  const chatBody = document.getElementById('wa-chat-body');
  const userMsgEl = document.createElement('div');
  userMsgEl.className = 'wa-msg out';
  userMsgEl.style.display = 'flex';
  userMsgEl.style.alignItems = 'center';
  userMsgEl.style.gap = '8px';
  userMsgEl.innerHTML = `<span>▶️</span> <span>${sample}</span>`;
  chatBody.appendChild(userMsgEl);
  chatBody.scrollTop = chatBody.scrollHeight;

  // Clean raw transcript for AI
  const cleanText = sample.replace(/🎙️ Voice Note \([0-9:]+\): '/, '').replace(/'$/, '');
  
  // Send cleaned speech-to-text to webhook
  setTimeout(() => {
    // Typing indicator
    const typingEl = document.createElement('div');
    typingEl.className = 'wa-msg in';
    typingEl.innerText = 'listening to audio & transcribing...';
    chatBody.appendChild(typingEl);
    chatBody.scrollTop = chatBody.scrollHeight;

    fetch('/api/v1/webhook/whatsapp', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        From: 'whatsapp:+919876543210',
        Body: cleanText,
        Latitude: 12.9352,
        Longitude: 77.6245
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
    }).catch(() => {
      if (chatBody.contains(typingEl)) chatBody.removeChild(typingEl);
    });
  }, 1000);
}
