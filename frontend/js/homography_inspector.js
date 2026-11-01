// Visual Homography & False-Closure Audit Engine
// Two-party citizen sign-off, feature point alignment, and contractor penalty accountability

let currentHomographyData = null;

function openHomographyModal(complaintId = 'CMP-BLR-001') {
  const modal = document.getElementById('homography-audit-modal');
  if (!modal) return;
  modal.classList.add('active');

  if (window.civicAudio && typeof window.civicAudio.playRisingTone === 'function') {
    window.civicAudio.playRisingTone();
  }

  // Load default authentic scenario
  runHomographyAudit(complaintId, 'sample_pothole', 'sample_repaired_asphalt');
}

function closeHomographyModal() {
  const modal = document.getElementById('homography-audit-modal');
  if (modal) modal.classList.remove('active');
  if (window.civicAudio && typeof window.civicAudio.playClick === 'function') {
    window.civicAudio.playClick();
  }
}

async function runHomographyAudit(complaintId, origTag, resTag, isFraudDemo = false) {
  const statusPill = document.getElementById('homography-status-pill');
  if (statusPill) statusPill.innerText = 'Analyzing in-situ background landmarks...';

  const lat = 12.9716;
  const lon = 77.5946;
  const resLat = isFraudDemo ? (lat + 0.0018) : lat; // 200m away if fraud demo

  try {
    const res = await fetch('/api/v1/contractors/verify-resolution', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        complaint_id: complaintId,
        original_image_tag: origTag,
        resolution_image_tag: isFraudDemo ? 'sample_shoes_desk' : resTag,
        original_lat: lat,
        original_lon: lon,
        resolution_lat: resLat,
        resolution_lon: lon,
        resolution_notes: isFraudDemo ? "Engineer submitted indoor photo." : "Asphalt patching with cold-mix bitumen complete."
      })
    });

    if (res.ok) {
      const data = await res.json();
      currentHomographyData = data;
      renderHomographyCanvas(data, isFraudDemo);
      updateHomographyUI(data);

      if (data.is_authentic_resolution) {
        if (window.civicAudio) window.civicAudio.playClick();
      } else {
        if (window.civicAudio) window.civicAudio.playInspectorWhistle();
      }
    }
  } catch (err) {
    console.error("Homography audit failed:", err);
  }
}

function renderHomographyCanvas(data, isFraudDemo) {
  const canvas = document.getElementById('homography-canvas');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  const w = canvas.width;
  const h = canvas.height;
  const halfW = w / 2;

  ctx.clearRect(0, 0, w, h);

  // Left Panel: BEFORE (Original Citizen Grievance)
  ctx.fillStyle = '#3a3a3c';
  ctx.fillRect(0, 0, halfW - 2, h);

  // Road crater before
  ctx.fillStyle = '#1c1917';
  ctx.beginPath();
  ctx.ellipse(halfW * 0.5, h * 0.58, halfW * 0.35, h * 0.22, 0, 0, Math.PI * 2);
  ctx.fill();

  // Background curb
  ctx.fillStyle = '#78716c';
  ctx.fillRect(0, h * 0.15, halfW, 14);

  // Electric pole
  ctx.fillStyle = '#a8a29e';
  ctx.fillRect(halfW * 0.82, h * 0.08, 12, h * 0.8);

  ctx.fillStyle = '#FF5A4E';
  ctx.font = 'bold 12px Fredoka, sans-serif';
  ctx.fillText('BEFORE (Citizen Photo)', 14, 24);

  // Right Panel: AFTER (Resolution Submission)
  ctx.fillStyle = isFraudDemo ? '#fef08a' : '#3a3a3c';
  ctx.fillRect(halfW + 2, 0, halfW, h);

  if (isFraudDemo) {
    // False closure: shoes / desk
    ctx.fillStyle = '#78350f';
    ctx.fillRect(halfW + 40, h * 0.35, 180, 110);
    ctx.fillStyle = '#1e293b';
    ctx.beginPath();
    ctx.ellipse(halfW + 90, h * 0.55, 30, 45, 0.2, 0, Math.PI * 2);
    ctx.ellipse(halfW + 170, h * 0.55, 30, 45, -0.2, 0, Math.PI * 2);
    ctx.fill();

    ctx.fillStyle = '#dc2626';
    ctx.font = 'bold 12px Fredoka, sans-serif';
    ctx.fillText('AFTER (Flagged Non-Civic Subject)', halfW + 14, 24);
  } else {
    // Repaired fresh asphalt patch
    ctx.fillStyle = '#18181b';
    ctx.fillRect(halfW + 2, h * 0.35, halfW, h * 0.55);

    // Smooth patch outline
    ctx.strokeStyle = '#10B981';
    ctx.lineWidth = 2.5;
    ctx.strokeRect(halfW + 20, h * 0.40, halfW - 40, h * 0.45);

    // Matching background curb
    ctx.fillStyle = '#78716c';
    ctx.fillRect(halfW, h * 0.15, halfW, 14);

    // Matching electric pole
    ctx.fillStyle = '#a8a29e';
    ctx.fillRect(halfW + halfW * 0.82, h * 0.08, 12, h * 0.8);

    ctx.fillStyle = '#10B981';
    ctx.font = 'bold 12px Fredoka, sans-serif';
    ctx.fillText('AFTER (Paved & Sealed Asphalt)', halfW + 14, 24);
  }

  // Draw dividing barrier
  ctx.strokeStyle = '#231F20';
  ctx.lineWidth = 4;
  ctx.beginPath();
  ctx.moveTo(halfW, 0); ctx.lineTo(halfW, h);
  ctx.stroke();

  // Draw Homography Matching Feature Ties
  if (data.is_authentic_resolution && data.landmark_alignment_points) {
    data.landmark_alignment_points.forEach(pt => {
      const x1 = pt.x1 * halfW;
      const y1 = pt.y1 * h;
      const x2 = halfW + (pt.x2 * halfW);
      const y2 = pt.y2 * h;

      // Connecting line
      ctx.strokeStyle = 'rgba(16, 185, 129, 0.8)';
      ctx.lineWidth = 2;
      ctx.setLineDash([4, 4]);
      ctx.beginPath();
      ctx.moveTo(x1, y1);
      ctx.lineTo(x2, y2);
      ctx.stroke();
      ctx.setLineDash([]);

      // Tie points
      ctx.fillStyle = '#FFC93C';
      ctx.beginPath();
      ctx.arc(x1, y1, 5, 0, Math.PI * 2);
      ctx.arc(x2, y2, 5, 0, Math.PI * 2);
      ctx.fill();
      ctx.strokeStyle = '#231F20';
      ctx.lineWidth = 1.5;
      ctx.stroke();
    });
  }
}

function updateHomographyUI(data) {
  const scoreEl = document.getElementById('homography-score-val');
  const deltaEl = document.getElementById('homography-delta-val');
  const auditEl = document.getElementById('homography-audit-badge');
  const penaltyEl = document.getElementById('homography-penalty-info');

  if (scoreEl) scoreEl.innerText = `${Math.round(data.homography_match_score * 100)}% Match (${data.matched_landmark_points_count} Feature Points)`;
  if (deltaEl) deltaEl.innerText = `${data.spatial_delta_meters}m GPS Delta (${data.spatial_gate_passed ? 'Passed <50m' : 'FAILED'})`;

  if (auditEl) {
    if (data.is_authentic_resolution) {
      auditEl.innerHTML = `<span style="background: var(--mint); color: var(--ink); border: 2px solid var(--ink); padding: 4px 10px; border-radius: var(--radius-pill); font-weight: 900;">✅ HOMOGRAPHY VERIFIED (GENUINE REPAIR)</span>`;
    } else {
      auditEl.innerHTML = `<span style="background: var(--tomato); color: var(--cream-white); border: 2px solid var(--ink); padding: 4px 10px; border-radius: var(--radius-pill); font-weight: 900;">🚨 FALSE CLOSURE PREVENTED</span>`;
    }
  }

  if (penaltyEl) {
    if (data.contractor_accountability.penalty_levied_inr > 0) {
      penaltyEl.innerHTML = `
        <div style="background: #fee2e2; border: 2px solid var(--tomato); border-radius: 8px; padding: 10px; color: var(--ink);">
          <strong style="color: var(--tomato);">⚠️ Statutory Penalty Triggered:</strong> ₹${data.contractor_accountability.penalty_levied_inr.toLocaleString()} deducted from contractor retention escrow under Clause 14B.
          <br>
          <span style="font-size: 0.74rem; color: var(--text-muted);">${data.contractor_accountability.explanation}</span>
        </div>
      `;
    } else {
      penaltyEl.innerHTML = `
        <div style="background: #dcfce7; border: 2px solid #059669; border-radius: 8px; padding: 10px; color: var(--ink);">
          <strong style="color: #059669;">✔️ Contractor Compliance Verified:</strong> Zero false attestation penalty. Contractor eligible for milestone invoice approval upon citizen sign-off.
        </div>
      `;
    }
  }
}

async function submitCitizenSignOff(isSatisfied) {
  const cid = currentHomographyData ? currentHomographyData.complaint_id : 'CMP-BLR-001';
  try {
    const res = await fetch('/api/v1/contractors/citizen-signoff', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        complaint_id: cid,
        is_satisfied: isSatisfied,
        feedback_notes: isSatisfied ? "Inspected site. Asphalt paved properly." : "Pothole still present. Not paved."
      })
    });

    if (res.ok) {
      const data = await res.json();
      if (isSatisfied) {
        if (window.civicCelebration && typeof window.civicCelebration.fireTricolorCelebration === 'function') {
          window.civicCelebration.fireTricolorCelebration();
        }
        if (window.civicAudio && typeof window.civicAudio.playCelebrationFanfare === 'function') {
          window.civicAudio.playCelebrationFanfare();
        }
        alert(`🎉 Citizen Resolution Sign-Off Recorded!\n\n${data.message}\n+${data.karma_points_awarded} Citizen Karma points awarded.`);
      } else {
        if (window.civicAudio && typeof window.civicAudio.playTempleBell === 'function') {
          window.civicAudio.playTempleBell();
        }
        alert(`⚖️ Grievance Reopened & Escalated!\n\n${data.message}\nAssigned: ${data.assigned_sdo}`);
      }
      closeHomographyModal();
      if (typeof loadMasterTickets === 'function') loadMasterTickets();
    }
  } catch (err) {
    console.error("Citizen sign-off failed:", err);
  }
}

// Expose globals
window.openHomographyModal = openHomographyModal;
window.closeHomographyModal = closeHomographyModal;
window.runHomographyAudit = runHomographyAudit;
window.submitCitizenSignOff = submitCitizenSignOff;
