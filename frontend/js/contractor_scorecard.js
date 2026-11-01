// Municipal Contractor Accountability & Penalty Scorecards
// Public performance league table, defect recurrence monitoring, and statutory escrow penalty audits

let currentContractorsData = null;

async function loadContractorScorecards() {
  const activeCity = (typeof currentSelectedCity !== 'undefined' && currentSelectedCity) ? currentSelectedCity : 'bengaluru';
  try {
    const res = await fetch(`/api/v1/contractors/scorecards?city=${encodeURIComponent(activeCity)}`);
    if (res.ok) {
      const data = await res.json();
      currentContractorsData = data;
      renderContractorScorecards(data);
    }
  } catch (err) {
    console.error("Failed to load contractor scorecards:", err);
  }
}

function renderContractorScorecards(data) {
  const tbody = document.getElementById('contractor-scorecard-tbody');
  if (!tbody || !data) return;

  tbody.innerHTML = data.map(c => {
    let gradeBadge = 'background: #dcfce7; color: #065f46; border: 1.5px solid #059669;';
    if (c.performance_grade === 'C') {
      gradeBadge = 'background: #fee2e2; color: #991b1b; border: 1.5px solid #dc2626;';
    } else if (c.performance_grade === 'B') {
      gradeBadge = 'background: #fef3c7; color: #92400e; border: 1.5px solid #d97706;';
    }

    const penaltyText = c.penalties_levied_inr > 0
      ? `<span style="color: var(--tomato); font-weight: 900;">₹${c.penalties_levied_inr.toLocaleString()}</span>`
      : `<span style="color: #059669; font-weight: 800;">₹0 (Clean)</span>`;

    return `
      <tr>
        <td>
          <strong style="color: var(--ink); font-size: 0.88rem;">${c.name}</strong><br>
          <span style="font-size: 0.72rem; color: var(--text-muted); font-weight: 700;">Lead: ${c.key_officer}</span>
        </td>
        <td style="font-size: 0.76rem; font-weight: 700;">${c.department}</td>
        <td style="font-size: 0.76rem;">${c.active_wards.join(', ')}</td>
        <td style="font-family: var(--font-display); font-weight: 900;">₹${c.total_contracts_cr} Cr</td>
        <td style="font-weight: 900; color: ${c.sla_compliance_pct >= 90 ? '#059669' : '#dc2626'};">${c.sla_compliance_pct}%</td>
        <td style="font-weight: 800; color: ${c.recurrence_failure_rate_pct > 10 ? '#dc2626' : 'var(--ink)'};">${c.recurrence_failure_rate_pct}%</td>
        <td>${penaltyText}</td>
        <td>
          <span style="padding: 2px 8px; border-radius: 9999px; font-weight: 900; font-size: 0.76rem; ${gradeBadge}">
            ${c.performance_grade} Grade
          </span>
        </td>
        <td>
          <button class="btn-secondary" style="font-size: 0.72rem; padding: 3px 8px;" onclick="openHomographyModal('CMP-BLR-001')">
            🔍 Audit Proof
          </button>
        </td>
      </tr>
    `;
  }).join('');
}

// Expose globals
window.loadContractorScorecards = loadContractorScorecards;
