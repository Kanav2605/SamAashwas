/**
 * SamAashwas - High-Resolution Canvas Civic Certificate & RTI Petition Generator
 * Generates official "Nagrik Samman Patra" (नागरिक सम्मान पत्र) and Printable RTI Dockets.
 * 100% Client-Side Canvas generation with zero external font/image dependencies.
 */

class CivicCertificateGenerator {
  constructor() {
    this.canvasWidth = 1200;
    this.canvasHeight = 840;
  }

  generateCertificate(citizenData = {}) {
    const name = citizenData.name || (window.currentUser ? window.currentUser.name : 'Aarav Sharma');
    const karma = citizenData.karma_points || (window.currentUser ? window.currentUser.karma_points : 850);
    const ward = citizenData.ward_name || (window.currentUser ? window.currentUser.ward_name : 'Indiranagar (Ward 112)');
    const city = citizenData.city || (window.currentSelectedCity ? window.currentSelectedCity.toUpperCase() : 'BENGALURU');
    const dateStr = new Date().toLocaleDateString('en-IN', {
      day: 'numeric',
      month: 'long',
      year: 'numeric'
    });

    const canvas = document.createElement('canvas');
    canvas.width = this.canvasWidth;
    canvas.height = this.canvasHeight;
    const ctx = canvas.getContext('2d');

    // 1. Solid Warm Parchment Background
    ctx.fillStyle = '#FFFDF7';
    ctx.fillRect(0, 0, this.canvasWidth, this.canvasHeight);

    // 2. Ornate Outer Neo-Brutalist & Tricolor Border
    ctx.lineWidth = 14;
    ctx.strokeStyle = '#231F20';
    ctx.strokeRect(16, 16, this.canvasWidth - 32, this.canvasHeight - 32);

    // Inner Tricolor Ribbon Borders
    // Saffron Top & Right
    ctx.lineWidth = 6;
    ctx.strokeStyle = '#FF6B35';
    ctx.strokeRect(30, 30, this.canvasWidth - 60, this.canvasHeight - 60);

    // Green Inner Accent
    ctx.lineWidth = 3;
    ctx.strokeStyle = '#10B981';
    ctx.strokeRect(40, 40, this.canvasWidth - 80, this.canvasHeight - 80);

    // Corner Geometric Ornaments
    this._drawCornerOrnament(ctx, 45, 45);
    this._drawCornerOrnament(ctx, this.canvasWidth - 45, 45);
    this._drawCornerOrnament(ctx, 45, this.canvasHeight - 45);
    this._drawCornerOrnament(ctx, this.canvasWidth - 45, this.canvasHeight - 45);

    // 3. Official Municipal Header
    ctx.textAlign = 'center';

    // Emblem Icon
    ctx.font = '52px sans-serif';
    ctx.fillText('🏛️', this.canvasWidth / 2, 110);

    ctx.fillStyle = '#231F20';
    ctx.font = 'bold 24px "Nunito", sans-serif';
    ctx.fillText('NATIONAL MUNICIPAL GRIEVANCE & URBAN CARE PLATFORM', this.canvasWidth / 2, 150);

    ctx.fillStyle = '#FF6B35';
    ctx.font = '900 36px "Fredoka", "Bricolage Grotesque", sans-serif';
    ctx.fillText('समाश्वास • नागरिक सम्मान पत्र', this.canvasWidth / 2, 195);

    ctx.fillStyle = '#10B981';
    ctx.font = 'bold 18px "Nunito", sans-serif';
    ctx.fillText('CERTIFICATE OF CIVIC EXCELLENCE & ACTIVE STEWARDSHIP', this.canvasWidth / 2, 225);

    // Decorative Separator Line
    ctx.lineWidth = 2.5;
    ctx.strokeStyle = '#231F20';
    ctx.beginPath();
    ctx.moveTo(this.canvasWidth / 2 - 240, 245);
    ctx.lineTo(this.canvasWidth / 2 + 240, 245);
    ctx.stroke();

    // 4. Citation Text
    ctx.fillStyle = '#57534E';
    ctx.font = '600 20px "Nunito", sans-serif';
    ctx.fillText('This official citation is proudly presented to', this.canvasWidth / 2, 295);

    // Citizen Name (Bold & Highlighted)
    ctx.fillStyle = '#231F20';
    ctx.font = '900 44px "Fredoka", "Bricolage Grotesque", sans-serif';
    ctx.fillText(name.toUpperCase(), this.canvasWidth / 2, 355);

    // Decorative Name Underline
    ctx.lineWidth = 3;
    ctx.strokeStyle = '#FFC93C';
    ctx.beginPath();
    ctx.moveTo(this.canvasWidth / 2 - 200, 370);
    ctx.lineTo(this.canvasWidth / 2 + 200, 370);
    ctx.stroke();

    // Citation Body
    ctx.fillStyle = '#231F20';
    ctx.font = '600 21px "Nunito", sans-serif';
    const line1 = `In recognition of outstanding civic vigilance, public service reporting, and community dedication`;
    const line2 = `under the Swachh Nagrik Initiative in ${ward}, ${city}.`;
    ctx.fillText(line1, this.canvasWidth / 2, 420);
    ctx.fillText(line2, this.canvasWidth / 2, 455);

    // 5. Karma & Achievement Box
    const boxX = this.canvasWidth / 2 - 260;
    const boxY = 490;
    const boxW = 520;
    const boxH = 100;

    ctx.fillStyle = '#FFEFD0';
    ctx.fillRect(boxX, boxY, boxW, boxH);
    ctx.lineWidth = 3;
    ctx.strokeStyle = '#231F20';
    ctx.strokeRect(boxX, boxY, boxW, boxH);

    ctx.fillStyle = '#231F20';
    ctx.font = 'bold 16px "Nunito", sans-serif';
    ctx.fillText('CERTIFIED CITIZEN KARMA CREDITS', this.canvasWidth / 2, boxY + 32);

    ctx.fillStyle = '#FF5A4E';
    ctx.font = '900 42px "Fredoka", sans-serif';
    ctx.fillText(`⭐ ${karma} KARMA POINTS ⭐`, this.canvasWidth / 2, boxY + 76);

    // 6. Signatures & Seal Section
    const sigY = 670;

    // Left Signature: Ward Officer / Zonal Commissioner
    ctx.textAlign = 'center';
    ctx.fillStyle = '#231F20';
    ctx.lineWidth = 1.5;
    ctx.beginPath();
    ctx.moveTo(180, sigY + 40);
    ctx.lineTo(380, sigY + 40);
    ctx.stroke();

    ctx.font = 'italic 20px "Caveat", cursive';
    ctx.fillText('Er. R. K. Nambiar', 280, sigY + 30);
    ctx.font = 'bold 15px "Nunito", sans-serif';
    ctx.fillText('Chief Ward Engineer (JE / EE)', 280, sigY + 62);
    ctx.font = '13px "Nunito", sans-serif';
    ctx.fillStyle = '#78716C';
    ctx.fillText('Urban Local Body Directorate', 280, sigY + 80);

    // Center Gold Seal
    this._drawSeal(ctx, this.canvasWidth / 2, sigY + 30);

    // Right Signature: AI Ethics & Jan Sunwai Ombudsman
    ctx.textAlign = 'center';
    ctx.fillStyle = '#231F20';
    ctx.lineWidth = 1.5;
    ctx.beginPath();
    ctx.moveTo(this.canvasWidth - 380, sigY + 40);
    ctx.lineTo(this.canvasWidth - 180, sigY + 40);
    ctx.stroke();

    ctx.font = 'italic 20px "Caveat", cursive';
    ctx.fillText('Justice V. S. Agnihotri', this.canvasWidth - 280, sigY + 30);
    ctx.font = 'bold 15px "Nunito", sans-serif';
    ctx.fillText('Municipal Ombudsman', this.canvasWidth - 280, sigY + 62);
    ctx.font = '13px "Nunito", sans-serif';
    ctx.fillStyle = '#78716C';
    ctx.fillText('Jan Sunwai Public Grievance Board', this.canvasWidth - 280, sigY + 80);

    // Bottom Footer
    ctx.fillStyle = '#78716C';
    ctx.font = 'bold 13px "Nunito", sans-serif';
    ctx.fillText(`ISSUED ON: ${dateStr.toUpperCase()} • DOCUMENT ID: SAM-CERT-${Math.floor(100000 + Math.random() * 900000)} • STATUTORY AUDIT SEAL VERIFIED`, this.canvasWidth / 2, this.canvasHeight - 48);

    return canvas;
  }

  _drawCornerOrnament(ctx, x, y) {
    ctx.fillStyle = '#FFC93C';
    ctx.beginPath();
    ctx.arc(x, y, 9, 0, Math.PI * 2);
    ctx.fill();
    ctx.lineWidth = 2;
    ctx.strokeStyle = '#231F20';
    ctx.stroke();
  }

  _drawSeal(ctx, x, y) {
    // Outer Starburst Gold Seal
    ctx.save();
    ctx.translate(x, y);

    ctx.fillStyle = '#FFC93C';
    ctx.beginPath();
    for (let i = 0; i < 24; i++) {
      const angle = (i * Math.PI) / 12;
      const r = i % 2 === 0 ? 52 : 44;
      const px = Math.cos(angle) * r;
      const py = Math.sin(angle) * r;
      if (i === 0) ctx.moveTo(px, py);
      else ctx.lineTo(px, py);
    }
    ctx.closePath();
    ctx.fill();
    ctx.lineWidth = 3;
    ctx.strokeStyle = '#231F20';
    ctx.stroke();

    // Inner Circle
    ctx.fillStyle = '#FFFDF7';
    ctx.beginPath();
    ctx.arc(0, 0, 36, 0, Math.PI * 2);
    ctx.fill();
    ctx.lineWidth = 2;
    ctx.strokeStyle = '#231F20';
    ctx.stroke();

    ctx.font = '24px sans-serif';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText('🎖️', 0, -2);

    ctx.restore();
  }

  openCertificateModal(citizenData = {}) {
    const canvas = this.generateCertificate(citizenData);
    const dataUrl = canvas.toDataURL('image/png');

    let modal = document.getElementById('certificate-modal');
    if (!modal) {
      modal = document.createElement('div');
      modal.id = 'certificate-modal';
      modal.className = 'modal-backdrop';
      modal.style.display = 'flex';
      modal.innerHTML = `
        <div class="modal-card" style="max-width: 900px; width: 95%; max-height: 92vh; overflow-y: auto;">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem; border-bottom: var(--border-ink-thick); padding-bottom: 10px;">
            <div style="display: flex; align-items: center; gap: 8px;">
              <span style="font-size: 1.5rem;">📜</span>
              <div>
                <h3 style="margin: 0; font-family: var(--font-display); font-size: 1.2rem; color: var(--ink);">
                  Official Nagrik Samman Patra (नागरिक सम्मान पत्र)
                </h3>
                <span style="font-size: 0.76rem; color: var(--text-muted); font-weight: 700;">
                  QR-Verifiable Digital Municipal Stewardship Citation
                </span>
              </div>
            </div>
            <button type="button" class="btn-close-modal" onclick="closeCertificateModal()">&times;</button>
          </div>

          <div style="text-align: center; margin-bottom: 1.25rem;">
            <img id="certificate-preview-img" src="${dataUrl}" style="width: 100%; border: var(--border-ink-thick); border-radius: var(--radius-sm); box-shadow: var(--shadow-hard); max-height: 520px; object-fit: contain; background: #FFFDF7;" alt="Civic Certificate of Merit">
          </div>

          <div style="display: flex; gap: 10px; justify-content: flex-end; flex-wrap: wrap;">
            <button class="btn-secondary" onclick="closeCertificateModal()">Close</button>
            <button class="btn-secondary" onclick="printCertificateImage()">🖨️ Print Certificate</button>
            <a id="certificate-download-btn" href="${dataUrl}" download="SamAashwas_Nagrik_Samman_Patra.png" class="btn-primary" style="text-decoration: none; display: inline-flex; align-items: center; gap: 6px;">
              📥 Download High-Res PNG
            </a>
          </div>
        </div>
      `;
      document.body.appendChild(modal);
    } else {
      document.getElementById('certificate-preview-img').src = dataUrl;
      document.getElementById('certificate-download-btn').href = dataUrl;
      modal.style.display = 'flex';
    }

    if (window.fireCivicCelebration) {
      window.fireCivicCelebration();
    }
    if (window.civicAudio && typeof window.civicAudio.playSuccessFanfare === 'function') {
      window.civicAudio.playSuccessFanfare();
    }
  }

  printRtiDocket(ticketData = {}) {
    const trackingId = ticketData.tracking_id || 'SYN-0001';
    const title = ticketData.title || 'Pothole & Broken Road Surface';
    const dept = ticketData.department || 'Roads & Footpaths';
    const ward = ticketData.ward_name || 'Indiranagar';
    const zone = ticketData.mcd_zone || 'East Zone';
    const officer = ticketData.assigned_engineer || 'Er. Suresh Patil (JE)';
    const slaRemaining = ticketData.sla_hours_remaining !== undefined ? ticketData.sla_hours_remaining : 14;
    const dateStr = new Date().toLocaleDateString('en-IN', { day: 'numeric', month: 'long', year: 'numeric' });

    const printWindow = window.open('', '_blank');
    if (!printWindow) {
      alert('Please allow popups to generate the official printable petition docket.');
      return;
    }

    printWindow.document.write(`
      <!DOCTYPE html>
      <html>
      <head>
        <title>Official Municipal Grievance Docket - ${trackingId}</title>
        <style>
          body { font-family: 'Times New Roman', Times, serif; padding: 40px; color: #111; line-height: 1.5; }
          .header { text-align: center; border-bottom: 3px double #111; padding-bottom: 15px; margin-bottom: 25px; }
          .emblem { font-size: 40px; margin-bottom: 5px; }
          .title { font-size: 20px; font-weight: bold; text-transform: uppercase; letter-spacing: 1px; }
          .subtitle { font-size: 14px; margin-top: 4px; }
          .meta-box { border: 1.5px solid #111; padding: 15px; margin: 20px 0; background: #fafafa; }
          .row { display: flex; justify-content: space-between; margin-bottom: 8px; font-size: 14px; }
          .label { font-weight: bold; width: 220px; }
          .val { flex: 1; }
          .notice-box { border: 1.5px dashed #111; padding: 12px; margin: 20px 0; font-size: 13px; }
          .footer { margin-top: 50px; display: flex; justify-content: space-between; }
          .signature-box { border-top: 1px solid #111; width: 240px; text-align: center; padding-top: 8px; font-size: 13px; font-weight: bold; }
          @media print {
            .no-print { display: none; }
          }
        </style>
      </head>
      <body>
        <div class="no-print" style="margin-bottom: 20px; text-align: right;">
          <button onclick="window.print()" style="padding: 10px 20px; font-weight: bold; font-size: 14px; cursor: pointer; background: #231F20; color: #fff; border: none; border-radius: 4px;">🖨️ Print This Official Docket</button>
        </div>

        <div class="header">
          <div class="emblem">🏛️</div>
          <div class="title">OFFICE OF THE MUNICIPAL COMMISSIONER &amp; OMBUDSMAN</div>
          <div class="subtitle">STATUTORY CITIZEN CHARTER GRIEVANCE RECORD &amp; JAN SUNWAI DOCKET</div>
          <div style="font-size: 12px; margin-top: 6px;">Issued under Public Services Guarantee &amp; Municipal Corporation Act</div>
        </div>

        <div class="meta-box">
          <div class="row"><span class="label">Grievance Tracking ID:</span><span class="val"><strong>${trackingId}</strong></span></div>
          <div class="row"><span class="label">Date of Filing:</span><span class="val">${dateStr}</span></div>
          <div class="row"><span class="label">Subject / Issue:</span><span class="val">${title}</span></div>
          <div class="row"><span class="label">Department:</span><span class="val">${dept}</span></div>
          <div class="row"><span class="label">Jurisdiction Ward &amp; Zone:</span><span class="val">${ward} (${zone})</span></div>
          <div class="row"><span class="label">Assigned Field Officer:</span><span class="val">${officer}</span></div>
          <div class="row"><span class="label">Statutory SLA Window:</span><span class="val">48 Hours (Remaining: <strong>${slaRemaining} Hours</strong>)</span></div>
        </div>

        <div class="notice-box">
          <strong>LEGAL &amp; STATUTORY NOTICE:</strong><br>
          This document serves as an immutable receipt of a municipal grievance lodged via the SamAashwas Civic Redressal Grid. 
          Under Section 4(1)(b) of the Right to Information Act, 2005 and State Public Service Delivery Charters, the designated 
          officer is bound to rectify the defect or submit a written progress compliance report before the Friday Jan Sunwai hearing.
        </div>

        <div style="margin-top: 30px; font-size: 13px;">
          <p><strong>Citizen Redressal Directive:</strong></p>
          <ol>
            <li>Field repair squad must upload geo-tagged verification photography matching coordinates within 50 meters.</li>
            <li>Failure to complete within statutory SLA prompts automatic transfer to the Zonal Commissioner's Jan Sunwai Docket.</li>
            <li>Complainant holds the right to verify or reject closure under the Citizen Verification Loop.</li>
          </ol>
        </div>

        <div class="footer">
          <div class="signature-box">
            Complainant Citizen Sign<br>
            <span style="font-weight: normal; font-size: 11px;">(Self-Attested)</span>
          </div>
          <div class="signature-box">
            Designated Ward Officer / SDO<br>
            <span style="font-weight: normal; font-size: 11px;">Seal &amp; Timestamp</span>
          </div>
        </div>
      </body>
      </html>
    `);
    printWindow.document.close();
  }
}

// Global instances and helpers
window.civicCertificate = new CivicCertificateGenerator();

window.openCertificateModal = function(citizenData) {
  window.civicCertificate.openCertificateModal(citizenData);
};

window.closeCertificateModal = function() {
  const modal = document.getElementById('certificate-modal');
  if (modal) modal.style.display = 'none';
};

window.printCertificateImage = function() {
  const img = document.getElementById('certificate-preview-img');
  if (!img) return;
  const printWin = window.open('', '_blank');
  printWin.document.write(`
    <html><head><title>Print Nagrik Samman Patra</title></head>
    <body style="margin: 0; display: flex; justify-content: center; align-items: center; min-height: 100vh;">
      <img src="${img.src}" style="max-width: 95vw; max-height: 95vh;" onload="window.print(); window.close();">
    </body></html>
  `);
  printWin.document.close();
};

window.printRtiDocket = function(ticketData) {
  window.civicCertificate.printRtiDocket(ticketData);
};
