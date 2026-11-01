// Uber H3 Hexagonal Spatial Indexing & Micro-Ward Clustering GIS Layer
// O(1) micro-spatial cell rendering, cluster density overlays, and polygon boundaries

let isH3GridActive = false;
let h3LayerGroup = null;

async function toggleH3HexGrid() {
  const btn = document.getElementById('btn-toggle-h3-grid');
  isH3GridActive = !isH3GridActive;

  if (btn) {
    btn.classList.toggle('active', isH3GridActive);
    btn.innerHTML = isH3GridActive ? '⬡ Hide H3 Hex Grid' : '⬡ Uber H3 Hex Grid';
  }

  if (typeof map === 'undefined' || !map) return;

  if (!h3LayerGroup) {
    h3LayerGroup = L.layerGroup().addTo(map);
  }

  if (isH3GridActive) {
    if (window.civicAudio && typeof window.civicAudio.playRisingTone === 'function') {
      window.civicAudio.playRisingTone();
    }
    await renderH3HexCells();
  } else {
    h3LayerGroup.clearLayers();
    if (window.civicAudio && typeof window.civicAudio.playClick === 'function') {
      window.civicAudio.playClick();
    }
  }
}

async function renderH3HexCells() {
  if (!h3LayerGroup || typeof map === 'undefined' || !map) return;
  h3LayerGroup.clearLayers();

  const activeCity = (typeof currentSelectedCity !== 'undefined' && currentSelectedCity) ? currentSelectedCity : 'bengaluru';

  try {
    const res = await fetch(`/api/v1/contractors/h3-cells?city=${encodeURIComponent(activeCity)}`);
    if (res.ok) {
      const data = await res.json();
      if (!data.cells || data.cells.length === 0) return;

      data.cells.forEach(cell => {
        // Flat solid color based on incident count
        let hexColor = '#FFC93C'; // yellow
        if (cell.critical_count > 0 || cell.incident_count >= 5) {
          hexColor = '#FF5A4E'; // red
        } else if (cell.incident_count >= 2) {
          hexColor = '#FFB88A'; // peach
        }

        const polygon = L.polygon(cell.boundary, {
          color: '#231F20',
          weight: 2,
          fillColor: hexColor,
          fillOpacity: 0.35,
          dashArray: '3, 3'
        });

        polygon.bindPopup(`
          <div style="font-family: 'Nunito', sans-serif; font-size: 12px; color: #231F20; min-width: 190px;">
            <div style="font-weight: 900; font-family: 'Fredoka', cursive; font-size: 13px; color: ${hexColor === '#FF5A4E' ? '#FF5A4E' : '#231F20'};">
              ⬡ H3 Hex Cell: Res 9
            </div>
            <code style="font-size: 10px; background: #FFEFD0; padding: 2px 4px; border-radius: 4px; border: 1px solid #231F20;">
              ${cell.h3_index}
            </code>
            <hr style="margin: 6px 0; border: none; border-top: 1px dashed #231F20;">
            <div>👥 Incidents in Cell: <strong>${cell.incident_count}</strong></div>
            <div>🚨 Critical Hazards: <strong>${cell.critical_count}</strong></div>
            <div>📍 Spatial Diameter: <strong>~100 meters</strong></div>
          </div>
        `);

        h3LayerGroup.addLayer(polygon);
      });
    }
  } catch (err) {
    console.error("Failed to load H3 hex cells:", err);
  }
}

// Expose globals
window.toggleH3HexGrid = toggleH3HexGrid;
