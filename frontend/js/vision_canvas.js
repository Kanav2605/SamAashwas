// Multimodal AI Vision Diagnostics Canvas Studio
// Real-time canvas rendering, animated laser scanning, bounding box overlays & spam shield diagnostics

let currentVisionSample = 'sample_pothole';
let visionScanAnimationId = null;
let currentDiagnosticsResult = null;

function initVisionCanvas() {
  const canvas = document.getElementById('vision-diagnostic-canvas');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  drawSimulatedCivicPhoto(ctx, currentVisionSample);
}

function loadVisionSample(sampleKey) {
  currentVisionSample = sampleKey;
  
  // Update button active states
  document.querySelectorAll('.vision-chip-btn').forEach(btn => {
    btn.classList.toggle('active', btn.getAttribute('data-sample') === sampleKey);
  });

  // Also sync form-image-hint select if present
  const selectEl = document.getElementById('form-image-hint');
  if (selectEl) {
    if (sampleKey === 'sample_pothole') selectEl.value = 'pothole';
    else if (sampleKey === 'sample_garbage') selectEl.value = 'garbage_dump';
    else if (sampleKey === 'sample_streetlight') selectEl.value = 'broken_streetlight';
    else if (sampleKey === 'sample_waterlog') selectEl.value = 'waterlogging';
    else if (sampleKey === 'sample_spam') selectEl.value = 'unrelated_or_spam';
  }

  const canvas = document.getElementById('vision-diagnostic-canvas');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  drawSimulatedCivicPhoto(ctx, sampleKey);

  // Play subtle feedback click
  if (window.civicAudio && typeof window.civicAudio.playClick === 'function') {
    window.civicAudio.playClick();
  }

  // Auto run scan
  runVisionScan();
}

function loadUserPhotoToCanvas(event) {
  const file = event.target.files && event.target.files[0];
  if (!file) return;

  const reader = new FileReader();
  reader.onload = function(e) {
    const img = new Image();
    img.onload = function() {
      const canvas = document.getElementById('vision-diagnostic-canvas');
      if (!canvas) return;
      const ctx = canvas.getContext('2d');
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
      runVisionScan(file.name);
    };
    img.src = e.target.result;
  };
  reader.readAsDataURL(file);
}

function drawSimulatedCivicPhoto(ctx, sampleKey) {
  const w = ctx.canvas.width;
  const h = ctx.canvas.height;
  ctx.clearRect(0, 0, w, h);

  if (sampleKey === 'sample_pothole') {
    // Road asphalt surface
    ctx.fillStyle = '#3a3a3c';
    ctx.fillRect(0, 0, w, h);

    // Road markings (yellow dashed line)
    ctx.strokeStyle = '#FFC93C';
    ctx.lineWidth = 6;
    ctx.setLineDash([20, 15]);
    ctx.beginPath();
    ctx.moveTo(w * 0.1, h * 0.2);
    ctx.lineTo(w * 0.9, h * 0.2);
    ctx.stroke();
    ctx.setLineDash([]);

    // Primary pothole crater
    ctx.fillStyle = '#1c1917';
    ctx.beginPath();
    ctx.ellipse(w * 0.5, h * 0.58, w * 0.28, h * 0.22, -0.05, 0, Math.PI * 2);
    ctx.fill();

    // Crater inner depth / exposed aggregate gravel
    ctx.fillStyle = '#44403c';
    ctx.beginPath();
    ctx.ellipse(w * 0.48, h * 0.60, w * 0.22, h * 0.16, 0.02, 0, Math.PI * 2);
    ctx.fill();

    // Gravel pebbles
    ctx.fillStyle = '#78716c';
    for (let i = 0; i < 18; i++) {
      const px = w * 0.35 + Math.random() * w * 0.3;
      const py = h * 0.48 + Math.random() * h * 0.22;
      ctx.beginPath();
      ctx.arc(px, py, 3 + Math.random() * 4, 0, Math.PI * 2);
      ctx.fill();
    }

    // Fatigue crack lines
    ctx.strokeStyle = '#292524';
    ctx.lineWidth = 2.5;
    ctx.beginPath();
    ctx.moveTo(w * 0.22, h * 0.55);
    ctx.lineTo(w * 0.12, h * 0.45);
    ctx.lineTo(w * 0.08, h * 0.6);
    ctx.moveTo(w * 0.78, h * 0.58);
    ctx.lineTo(w * 0.88, h * 0.7);
    ctx.stroke();

    // Field photo timestamp watermark
    ctx.fillStyle = '#FFC93C';
    ctx.font = 'bold 11px Courier New';
    ctx.fillText('CAM-01 • GPS: 12.9716 N, 77.5946 E • 2026-11-01 15:20:14', 12, h - 12);

  } else if (sampleKey === 'sample_garbage') {
    // Pavement & Wall background
    ctx.fillStyle = '#e7e5e4';
    ctx.fillRect(0, 0, w, h * 0.45);
    ctx.fillStyle = '#57534e';
    ctx.fillRect(0, h * 0.45, w, h * 0.55);

    // Green municipal dumpster bin
    ctx.fillStyle = '#15803d';
    ctx.strokeStyle = '#14532d';
    ctx.lineWidth = 3;
    ctx.fillRect(w * 0.58, h * 0.25, w * 0.32, h * 0.45);
    ctx.strokeRect(w * 0.58, h * 0.25, w * 0.32, h * 0.45);
    ctx.fillStyle = '#166534';
    ctx.fillRect(w * 0.55, h * 0.22, w * 0.38, 12);

    // Mixed waste heap overflowing
    ctx.fillStyle = '#78716c';
    ctx.beginPath();
    ctx.arc(w * 0.40, h * 0.65, w * 0.25, 0, Math.PI * 2);
    ctx.fill();

    // Colored plastic bags & debris
    const colors = ['#3b82f6', '#ef4444', '#eab308', '#ffffff', '#000000'];
    for (let i = 0; i < 24; i++) {
      ctx.fillStyle = colors[i % colors.length];
      const bx = w * 0.22 + Math.random() * w * 0.45;
      const by = h * 0.52 + Math.random() * h * 0.32;
      ctx.beginPath();
      ctx.ellipse(bx, by, 10 + Math.random() * 12, 6 + Math.random() * 8, Math.random(), 0, Math.PI * 2);
      ctx.fill();
    }

    ctx.fillStyle = '#FFC93C';
    ctx.font = 'bold 11px Courier New';
    ctx.fillText('SWACHH-INSPECTION • GPS: 12.9780 N, 77.6402 E • 1.8 TONS ESTIMATE', 12, h - 12);

  } else if (sampleKey === 'sample_streetlight') {
    // Dark night sky
    ctx.fillStyle = '#0f172a';
    ctx.fillRect(0, 0, w, h);

    // Steel pole
    ctx.fillStyle = '#64748b';
    ctx.fillRect(w * 0.48, h * 0.1, 16, h * 0.9);

    // Horizontal lamp arm
    ctx.fillStyle = '#64748b';
    ctx.fillRect(w * 0.38, h * 0.14, w * 0.2, 12);

    // Luminaire fixture (dark / unlit)
    ctx.fillStyle = '#1e293b';
    ctx.strokeStyle = '#FF5A4E';
    ctx.lineWidth = 2.5;
    ctx.fillRect(w * 0.35, h * 0.18, 55, 24);
    ctx.strokeRect(w * 0.35, h * 0.18, 55, 24);

    // Red X over dead lamp
    ctx.strokeStyle = '#FF5A4E';
    ctx.lineWidth = 3;
    ctx.beginPath();
    ctx.moveTo(w * 0.36, h * 0.19);
    ctx.lineTo(w * 0.36 + 50, h * 0.19 + 22);
    ctx.moveTo(w * 0.36 + 50, h * 0.19);
    ctx.lineTo(w * 0.36, h * 0.19 + 22);
    ctx.stroke();

    ctx.fillStyle = '#FF5A4E';
    ctx.font = 'bold 12px Fredoka, sans-serif';
    ctx.fillText('NO ILLUMINATION • MCB OPEN CIRCUIT', w * 0.42, h * 0.32);

    ctx.fillStyle = '#FFC93C';
    ctx.font = 'bold 11px Courier New';
    ctx.fillText('ELECTRICAL-AUDIT • POLE #BLR-4091 • FEEDER FAULT', 12, h - 12);

  } else if (sampleKey === 'sample_waterlog') {
    // Waterlogged road surface
    ctx.fillStyle = '#1e3a5f';
    ctx.fillRect(0, 0, w, h);

    // Submerged road curbs
    ctx.fillStyle = '#475569';
    ctx.fillRect(0, 0, w, h * 0.3);

    // Water ripple rings
    ctx.strokeStyle = '#60a5fa';
    ctx.lineWidth = 2;
    for (let r = 20; r <= 120; r += 25) {
      ctx.beginPath();
      ctx.ellipse(w * 0.45, h * 0.65, r * 1.6, r * 0.6, 0, 0, Math.PI * 2);
      ctx.stroke();
    }

    // Submerged drain grate
    ctx.strokeStyle = '#94a3b8';
    ctx.lineWidth = 3;
    ctx.strokeRect(w * 0.72, h * 0.6, 60, 40);
    for (let g = 0; g < 5; g++) {
      ctx.beginPath();
      ctx.moveTo(w * 0.72 + 10 + g * 10, h * 0.6);
      ctx.lineTo(w * 0.72 + 10 + g * 10, h * 0.6 + 40);
      ctx.stroke();
    }

    ctx.fillStyle = '#FFC93C';
    ctx.font = 'bold 11px Courier New';
    ctx.fillText('MONSOON-TELEMETRY • WATER DEPTH > 260MM • UNDERPASS HAZARD', 12, h - 12);

  } else if (sampleKey === 'sample_spam') {
    // Colorful viral meme graphic
    ctx.fillStyle = '#fef08a';
    ctx.fillRect(0, 0, w, h);

    // Funny cartoon cat face
    ctx.fillStyle = '#ea580c';
    ctx.beginPath();
    ctx.arc(w * 0.5, h * 0.45, 70, 0, Math.PI * 2);
    ctx.fill();

    // Cat ears
    ctx.beginPath();
    ctx.moveTo(w * 0.5 - 55, h * 0.45 - 35);
    ctx.lineTo(w * 0.5 - 35, h * 0.45 - 90);
    ctx.lineTo(w * 0.5 - 10, h * 0.45 - 55);
    ctx.fill();

    ctx.beginPath();
    ctx.moveTo(w * 0.5 + 55, h * 0.45 - 35);
    ctx.lineTo(w * 0.5 + 35, h * 0.45 - 90);
    ctx.lineTo(w * 0.5 + 10, h * 0.45 - 55);
    ctx.fill();

    // Cat eyes
    ctx.fillStyle = '#ffffff';
    ctx.beginPath();
    ctx.arc(w * 0.5 - 25, h * 0.45 - 10, 16, 0, Math.PI * 2);
    ctx.arc(w * 0.5 + 25, h * 0.45 - 10, 16, 0, Math.PI * 2);
    ctx.fill();
    ctx.fillStyle = '#000000';
    ctx.beginPath();
    ctx.arc(w * 0.5 - 25, h * 0.45 - 10, 8, 0, Math.PI * 2);
    ctx.arc(w * 0.5 + 25, h * 0.45 - 10, 8, 0, Math.PI * 2);
    ctx.fill();

    // Meme text
    ctx.fillStyle = '#000000';
    ctx.font = '900 20px Impact, sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText('WHEN THE ROAD IS BAD', w * 0.5, 36);
    ctx.fillText('BUT YOU POST CAT MEMES', w * 0.5, h - 25);
    ctx.textAlign = 'start';
  }
}

async function runVisionScan(customImageName = null) {
  const canvas = document.getElementById('vision-diagnostic-canvas');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  const w = canvas.width;
  const h = canvas.height;

  // Sound feedback: scanner pulse
  if (window.civicAudio && typeof window.civicAudio.playRisingTone === 'function') {
    window.civicAudio.playRisingTone();
  }

  // Laser scanner animation
  let scanY = 0;
  const startTime = Date.now();
  const scanDuration = 600; // ms

  function animateLaser() {
    const elapsed = Date.now() - startTime;
    const progress = Math.min(elapsed / scanDuration, 1.0);
    scanY = progress * h;

    // Redraw base image
    drawSimulatedCivicPhoto(ctx, currentVisionSample);

    // Draw HUD Grid
    ctx.strokeStyle = 'rgba(16, 185, 129, 0.25)';
    ctx.lineWidth = 1;
    for (let x = 0; x < w; x += 40) {
      ctx.beginPath();
      ctx.moveTo(x, 0);
      ctx.lineTo(x, h);
      ctx.stroke();
    }
    for (let y = 0; y < h; y += 40) {
      ctx.beginPath();
      ctx.moveTo(0, y);
      ctx.lineTo(w, y);
      ctx.stroke();
    }

    // Draw Laser Scan Line
    ctx.strokeStyle = '#10B981';
    ctx.lineWidth = 3;
    ctx.beginPath();
    ctx.moveTo(0, scanY);
    ctx.lineTo(w, scanY);
    ctx.stroke();

    // Laser glow strip
    ctx.fillStyle = 'rgba(16, 185, 129, 0.18)';
    ctx.fillRect(0, Math.max(0, scanY - 18), w, 36);

    if (progress < 1.0) {
      visionScanAnimationId = requestAnimationFrame(animateLaser);
    } else {
      // Finished scanning, now fetch diagnostics & render bounding boxes
      fetchAndRenderVisionDiagnostics(customImageName);
    }
  }

  if (visionScanAnimationId) cancelAnimationFrame(visionScanAnimationId);
  visionScanAnimationId = requestAnimationFrame(animateLaser);
}

async function fetchAndRenderVisionDiagnostics(customImageName = null) {
  const canvas = document.getElementById('vision-diagnostic-canvas');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  const w = canvas.width;
  const h = canvas.height;

  const imageId = customImageName || currentVisionSample;
  const latVal = parseFloat(document.getElementById('form-lat')?.value) || 12.9716;
  const lonVal = parseFloat(document.getElementById('form-lon')?.value) || 77.6412;

  try {
    const res = await fetch('/api/v1/complaints/vision-diagnostics', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        image_identifier: imageId,
        department: "Roads & Traffic Infrastructure",
        lat: latVal,
        lon: lonVal
      })
    });

    if (res.ok) {
      const data = await res.json();
      currentDiagnosticsResult = data;
      renderBoundingBoxesOnCanvas(ctx, data, w, h);
      updateVisionMetricsUI(data);

      if (data.is_authentic) {
        if (window.civicAudio && typeof window.civicAudio.playCelebrationFanfare === 'function') {
          window.civicAudio.playClick();
        }
      } else {
        if (window.civicAudio && typeof window.civicAudio.playTempleBell === 'function') {
          window.civicAudio.playTempleBell();
        }
      }
    }
  } catch (err) {
    console.error("Vision diagnostics failed:", err);
  }
}

function renderBoundingBoxesOnCanvas(ctx, data, w, h) {
  // Clear and redraw base photo
  drawSimulatedCivicPhoto(ctx, currentVisionSample);

  if (!data.objects || data.objects.length === 0) return;

  data.objects.forEach(obj => {
    const [nx, ny, nw, nh] = obj.box;
    const bx = nx * w;
    const by = ny * h;
    const bw = nw * w;
    const bh = nh * h;

    const boxColor = obj.color || (data.is_authentic ? '#10B981' : '#FF5A4E');

    // Solid bounding box with thick borders
    ctx.strokeStyle = boxColor;
    ctx.lineWidth = 2.5;
    ctx.strokeRect(bx, by, bw, bh);

    // Corner crosshairs
    const arm = 10;
    ctx.lineWidth = 4;
    // Top-left
    ctx.beginPath();
    ctx.moveTo(bx, by + arm); ctx.lineTo(bx, by); ctx.lineTo(bx + arm, by);
    ctx.stroke();
    // Top-right
    ctx.beginPath();
    ctx.moveTo(bx + bw - arm, by); ctx.lineTo(bx + bw, by); ctx.lineTo(bx + bw, by + arm);
    ctx.stroke();
    // Bottom-left
    ctx.beginPath();
    ctx.moveTo(bx, by + bh - arm); ctx.lineTo(bx, by + bh); ctx.lineTo(bx + arm, by + bh);
    ctx.stroke();
    // Bottom-right
    ctx.beginPath();
    ctx.moveTo(bx + bw - arm, by + bh); ctx.lineTo(bx + bw, by + bh); ctx.lineTo(bx + bw, by + bh - arm);
    ctx.stroke();

    // Tag chip pill above box
    const labelText = `${obj.label} (${Math.round(obj.confidence * 100)}%)`;
    ctx.font = 'bold 11px Fredoka, sans-serif';
    const textWidth = ctx.measureText(labelText).width;

    ctx.fillStyle = boxColor;
    ctx.fillRect(bx, Math.max(0, by - 22), textWidth + 14, 20);
    ctx.strokeStyle = '#231F20';
    ctx.lineWidth = 1.5;
    ctx.strokeRect(bx, Math.max(0, by - 22), textWidth + 14, 20);

    ctx.fillStyle = boxColor === '#FFC93C' ? '#231F20' : '#FFFFFF';
    ctx.fillText(labelText, bx + 7, Math.max(14, by - 8));
  });
}

function updateVisionMetricsUI(data) {
  const classEl = document.getElementById('vision-metric-class');
  const confEl = document.getElementById('vision-metric-confidence');
  const hazardEl = document.getElementById('vision-metric-hazard');
  const shieldEl = document.getElementById('vision-metric-shield');
  const prescEl = document.getElementById('vision-prescription-box');

  if (classEl) classEl.innerText = data.display_label;
  if (confEl) confEl.innerText = `${Math.round(data.confidence * 100)}% Confidence`;
  if (hazardEl) hazardEl.innerText = data.hazard_level;
  
  if (shieldEl) {
    if (data.spam_shield && data.spam_shield.is_spam) {
      shieldEl.innerHTML = `<span style="color: var(--tomato); font-weight: 900;">🚨 SPAM SHIELD TRIGGERED</span> (${Math.round(data.spam_shield.spam_probability * 100)}% Spam Risk)`;
    } else {
      shieldEl.innerHTML = `<span style="color: #059669; font-weight: 900;">🛡️ VERIFIED CIVIC EVIDENCE</span> (GPS &amp; EXIF Validated)`;
    }
  }

  if (prescEl) {
    if (data.is_authentic) {
      prescEl.innerHTML = `
        <div style="font-size: 0.76rem; font-weight: 800; color: var(--ink);">
          🛠️ <strong>Recommended Repair Prescription:</strong> ${data.recommended_material}
          <br>
          📐 <strong>Estimated Repair Area:</strong> ${data.estimated_repair_sqm} sq.m (${data.objects.length} distress regions identified)
        </div>
      `;
    } else {
      prescEl.innerHTML = `
        <div style="font-size: 0.76rem; font-weight: 800; color: var(--tomato);">
          🚫 <strong>Audit Verdict:</strong> Image contains no legitimate municipal asset. Deflected prior to field dispatch to conserve public resources.
        </div>
      `;
    }
  }
}

// Expose globals
window.initVisionCanvas = initVisionCanvas;
window.loadVisionSample = loadVisionSample;
window.loadUserPhotoToCanvas = loadUserPhotoToCanvas;
window.runVisionScan = runVisionScan;
