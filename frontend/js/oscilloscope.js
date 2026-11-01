// Real-time Audio Waveform Oscilloscope Visualizer
// Pure Canvas sine-wave synthesizer engine for speech recording and voice note feedback

const oscilloscopeState = {};

function initOscilloscope(canvasId) {
  const canvas = document.getElementById(canvasId);
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  drawFlatLine(ctx, canvas.width, canvas.height);
}

function drawFlatLine(ctx, w, h) {
  ctx.clearRect(0, 0, w, h);
  ctx.fillStyle = '#231F20';
  ctx.fillRect(0, 0, w, h);

  ctx.strokeStyle = '#10B981';
  ctx.lineWidth = 2;
  ctx.beginPath();
  ctx.moveTo(0, h / 2);
  ctx.lineTo(w, h / 2);
  ctx.stroke();
}

function startOscilloscope(canvasId) {
  const canvas = document.getElementById(canvasId);
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  const w = canvas.width;
  const h = canvas.height;

  oscilloscopeState[canvasId] = {
    active: true,
    phase: 0
  };

  function renderWave() {
    if (!oscilloscopeState[canvasId] || !oscilloscopeState[canvasId].active) {
      drawFlatLine(ctx, w, h);
      return;
    }

    const st = oscilloscopeState[canvasId];
    st.phase += 0.08;

    ctx.clearRect(0, 0, w, h);
    ctx.fillStyle = '#231F20';
    ctx.fillRect(0, 0, w, h);

    // Center guideline
    ctx.strokeStyle = '#374151';
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.moveTo(0, h / 2);
    ctx.lineTo(w, h / 2);
    ctx.stroke();

    // Primary oscillating green wave
    ctx.strokeStyle = '#10B981';
    ctx.lineWidth = 2.5;
    ctx.beginPath();

    for (let x = 0; x < w; x++) {
      const freq1 = Math.sin((x * 0.05) + st.phase) * (h * 0.35);
      const freq2 = Math.sin((x * 0.02) - st.phase * 1.5) * (h * 0.15);
      const envelope = Math.sin((x / w) * Math.PI); // taper ends
      const y = (h / 2) + (freq1 + freq2) * envelope;

      if (x === 0) ctx.moveTo(x, y);
      else ctx.lineTo(x, y);
    }
    ctx.stroke();

    // Secondary subtle gold harmonic wave
    ctx.strokeStyle = 'rgba(255, 201, 60, 0.7)';
    ctx.lineWidth = 1.5;
    ctx.beginPath();

    for (let x = 0; x < w; x += 2) {
      const freq = Math.cos((x * 0.07) + st.phase * 0.8) * (h * 0.22);
      const envelope = Math.sin((x / w) * Math.PI);
      const y = (h / 2) + freq * envelope;

      if (x === 0) ctx.moveTo(x, y);
      else ctx.lineTo(x, y);
    }
    ctx.stroke();

    requestAnimationFrame(renderWave);
  }

  requestAnimationFrame(renderWave);
}

function stopOscilloscope(canvasId) {
  if (oscilloscopeState[canvasId]) {
    oscilloscopeState[canvasId].active = false;
  }
}

// Expose globals
window.initOscilloscope = initOscilloscope;
window.startOscilloscope = startOscilloscope;
window.stopOscilloscope = stopOscilloscope;
