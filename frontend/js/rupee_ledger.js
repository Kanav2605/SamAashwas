// Public Rupee Tax Transparency & Municipal Expenditure Savings Ledger
// Transparent Schedule of Rates (SoR), Deduplication Taxpayer Savings, and Citizen Tax ROI Calculator

let currentLedgerData = null;

async function loadRupeeLedger() {
  const activeCity = (typeof currentSelectedCity !== 'undefined' && currentSelectedCity) ? currentSelectedCity : 'bengaluru';
  try {
    const res = await fetch(`/api/v1/analytics/rupee-ledger?city=${encodeURIComponent(activeCity)}`);
    if (res.ok) {
      const data = await res.json();
      currentLedgerData = data;
      renderRupeeLedger(data);
    }
  } catch (err) {
    console.error("Failed to load rupee transparency ledger:", err);
  }
}

function renderRupeeLedger(data) {
  // Update savings KPIs
  const savingsEl = document.getElementById('ledger-savings-amt');
  const dispatchesEl = document.getElementById('ledger-dispatches-val');
  const dieselEl = document.getElementById('ledger-diesel-val');
  const co2El = document.getElementById('ledger-co2-val');

  if (savingsEl) savingsEl.innerText = data.taxpayer_savings_formatted;
  if (dispatchesEl) dispatchesEl.innerText = `${data.redundant_dispatches_prevented} Redundant Dispatches`;
  if (dieselEl) dieselEl.innerText = `${data.diesel_saved_liters} Liters Saved`;
  if (co2El) co2El.innerText = `${data.co2_emissions_averted_kg} kg Averted`;

  // Render Schedule of Rates table
  const sorTbody = document.getElementById('ledger-sor-tbody');
  if (sorTbody && data.schedule_of_rates) {
    sorTbody.innerHTML = data.schedule_of_rates.map(item => `
      <tr>
        <td style="font-weight: 800; color: var(--ink);">${item.service}</td>
        <td style="color: var(--text-muted); font-size: 0.76rem;">${item.unit}</td>
        <td style="font-weight: 900; color: #059669; font-family: var(--font-display); font-size: 0.88rem;">₹${item.rate_inr.toLocaleString()}</td>
        <td style="color: var(--text-muted); font-size: 0.72rem;">${item.agency}</td>
      </tr>
    `).join('');
  }

  // Run initial Tax ROI with default ₹5,000
  calculateTaxROI(5000);
}

function calculateTaxROI(amount) {
  const val = Math.max(500, parseFloat(amount) || 5000);
  const inputEl = document.getElementById('tax-calculator-input');
  if (inputEl && inputEl.value !== val.toString()) {
    inputEl.value = val;
  }

  const container = document.getElementById('tax-roi-breakdown');
  if (!container) return;

  const roadAmt = val * 0.28;
  const roadMeters = (roadAmt / 185).toFixed(1);

  const wasteAmt = val * 0.32;
  const wasteKg = ((wasteAmt / 1650) * 1000).toFixed(0);

  const lightAmt = val * 0.15;
  const lightNights = (lightAmt / 4.1).toFixed(0);

  const drainAmt = val * 0.15;
  const drainMeters = (drainAmt / 95).toFixed(1);

  const parkAmt = val * 0.10;
  const treeCount = Math.max(1, (parkAmt / 250).toFixed(0));

  container.innerHTML = `
    <div class="tax-breakdown-item" style="border-left: 4px solid #FF5A4E;">
      <div>
        <div style="color: var(--tomato); font-weight: 900;">🚧 Roads &amp; Asphalt Carriageways (28%)</div>
        <div style="font-size: 0.72rem; color: var(--text-muted);">Paves &amp; patches approx. <strong>${roadMeters} sq. meters</strong> of all-weather road</div>
      </div>
      <div style="font-size: 0.95rem; font-weight: 900; font-family: var(--font-display); color: var(--ink);">₹${roadAmt.toLocaleString(undefined, {maximumFractionDigits: 0})}</div>
    </div>

    <div class="tax-breakdown-item" style="border-left: 4px solid #10B981;">
      <div>
        <div style="color: #059669; font-weight: 900;">🧹 Swachhata &amp; Solid Waste (32%)</div>
        <div style="font-size: 0.72rem; color: var(--text-muted);">Collects, segregates &amp; composts <strong>${wasteKg} kg</strong> of household waste</div>
      </div>
      <div style="font-size: 0.95rem; font-weight: 900; font-family: var(--font-display); color: var(--ink);">₹${wasteAmt.toLocaleString(undefined, {maximumFractionDigits: 0})}</div>
    </div>

    <div class="tax-breakdown-item" style="border-left: 4px solid #FFC93C;">
      <div>
        <div style="color: #b45309; font-weight: 900;">💡 24/7 Smart Streetlighting (15%)</div>
        <div style="font-size: 0.72rem; color: var(--text-muted);">Powers an energy-efficient 45W LED streetlight for <strong>${lightNights} nights</strong></div>
      </div>
      <div style="font-size: 0.95rem; font-weight: 900; font-family: var(--font-display); color: var(--ink);">₹${lightAmt.toLocaleString(undefined, {maximumFractionDigits: 0})}</div>
    </div>

    <div class="tax-breakdown-item" style="border-left: 4px solid #3B82F6;">
      <div>
        <div style="color: #2563eb; font-weight: 900;">💧 Stormwater Drainage &amp; Flood Sump (15%)</div>
        <div style="font-size: 0.72rem; color: var(--text-muted);">De-silts &amp; cleans <strong>${drainMeters} linear meters</strong> of roadside stormwater drain</div>
      </div>
      <div style="font-size: 0.95rem; font-weight: 900; font-family: var(--font-display); color: var(--ink);">₹${drainAmt.toLocaleString(undefined, {maximumFractionDigits: 0})}</div>
    </div>

    <div class="tax-breakdown-item" style="border-left: 4px solid #8B5CF6;">
      <div>
        <div style="color: #7c3aed; font-weight: 900;">🌳 Ward Parks &amp; Urban Forest (10%)</div>
        <div style="font-size: 0.72rem; color: var(--text-muted);">Nurtures <strong>${treeCount} urban saplings</strong> and ward botanical garden beds</div>
      </div>
      <div style="font-size: 0.95rem; font-weight: 900; font-family: var(--font-display); color: var(--ink);">₹${parkAmt.toLocaleString(undefined, {maximumFractionDigits: 0})}</div>
    </div>
  `;
}

// Expose globals
window.loadRupeeLedger = loadRupeeLedger;
window.calculateTaxROI = calculateTaxROI;
