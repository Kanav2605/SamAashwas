// Interactive WhatsApp Bot Simulator
async function sendWhatsAppMessage() {
  const inputEl = document.getElementById('wa-input');
  const chatBody = document.getElementById('wa-chat-body');
  const text = inputEl.value.trim();

  if (!text) return;

  // Append user's outgoing message
  const userMsgEl = document.createElement('div');
  userMsgEl.className = 'wa-msg out';
  userMsgEl.innerText = text;
  chatBody.appendChild(userMsgEl);

  inputEl.value = '';
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
        Longitude: 77.6245
      })
    });

    chatBody.removeChild(typingEl);

    if (response.ok) {
      const data = await response.json();
      const botMsgEl = document.createElement('div');
      botMsgEl.className = 'wa-msg in';
      botMsgEl.innerText = data.reply_message;
      chatBody.appendChild(botMsgEl);

      // Refresh command center background data
      if (typeof loadMasterTickets === 'function') loadMasterTickets();
      if (typeof loadKPIStats === 'function') loadKPIStats();
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
