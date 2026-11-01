import pytest
from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def test_health_check_endpoint():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"

def test_submit_and_deduplicate_complaints():
    # Submit first grievance
    payload1 = {
        "raw_text": "Bhaiya road par street light 4 din se band hai near Sharma General Store Ward 7",
        "lat": 12.9716,
        "lon": 77.6412,
        "citizen_name": "Rohan Verma",
        "citizen_phone": "9876543211",
        "channel": "web_portal"
    }
    res1 = client.post("/api/v1/complaints/submit", json=payload1)
    assert res1.status_code == 200
    data1 = res1.json()
    master_id = data1["master_ticket_id"]
    assert data1["department"] == "Electrical & Streetlighting"
    assert data1["national_mission"] is not None

    # Submit duplicate grievance 40 meters away with code-mixed text
    payload2 = {
        "raw_text": "Street light is completely dead near Sharma general store since 4 days",
        "lat": 12.9718,
        "lon": 77.6414,
        "citizen_name": "Priya Nair",
        "citizen_phone": "9876543212",
        "channel": "whatsapp"
    }
    res2 = client.post("/api/v1/complaints/submit", json=payload2)
    assert res2.status_code == 200
    data2 = res2.json()
    assert data2["master_ticket_id"] == master_id # Clustered into same master ticket!
    assert data2["is_duplicate"] is True

def test_get_master_tickets():
    res = client.get("/api/v1/master-tickets")
    assert res.status_code == 200
    tickets = res.json()
    assert isinstance(tickets, list)
    assert len(tickets) > 0
    assert "national_mission" in tickets[0]
    assert "corporator" in tickets[0]

def test_whatsapp_webhook_flow():
    payload = {
        "From": "whatsapp:+919811223344",
        "Body": "Ward 2 gali mein sewer overflow ho raha hai badbu aa rahi hai",
        "Latitude": 12.9352,
        "Longitude": 77.6245
    }
    res = client.post("/api/v1/webhook/whatsapp", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert "Namaste" in data["reply_message"]
    assert data["status"] == "PROCESSED"
    assert data["national_mission"] is not None

def test_predictive_ward_risk():
    res = client.get("/api/v1/predictive-maintenance/ward-risk")
    assert res.status_code == 200
    wards = res.json()
    assert len(wards) > 0
    assert "risk_score" in wards[0]
    assert "desilting_readiness_pct" in wards[0]
    assert "corporator" in wards[0]

def test_analytics_stats_with_missions_and_jan_sunwai():
    res = client.get("/api/v1/analytics/stats")
    assert res.status_code == 200
    data = res.json()
    assert "national_mission_breakdown" in data
    assert "jan_sunwai_escalated_count" in data

def test_pwa_and_frontend_serving():
    res_index = client.get("/")
    assert res_index.status_code == 200
    assert "CivicSense AI" in res_index.text

    res_manifest = client.get("/manifest.json")
    assert res_manifest.status_code == 200
    assert "SamAashwas" in res_manifest.text

    res_sw = client.get("/sw.js")
    assert res_sw.status_code == 200
    assert "civicsense" in res_sw.text

def test_endorse_master_ticket():
    # First get an existing master ticket
    res = client.get("/api/v1/master-tickets")
    assert res.status_code == 200
    tickets = res.json()
    assert len(tickets) > 0
    t_id = tickets[0]["master_ticket_id"]
    initial_reports = tickets[0]["report_count"]

    # Endorse ticket
    endorse_res = client.post(f"/api/v1/master-tickets/{t_id}/endorse", json={
        "citizen_name": "Test Endorser",
        "citizen_phone": "9876543299"
    })
    assert endorse_res.status_code == 200
    data = endorse_res.json()
    assert data["status"] == "success"
    assert data["report_count"] == initial_reports + 1
    assert data["karma_points_awarded"] == 50

def test_academic_prototype_banner_and_new_views_present():
    res = client.get("/")
    assert res.status_code == 200
    html = res.text
    # Academic Prototype Banner (Rule 4)
    assert "Academic Capstone Prototype" in html
    assert "Not an official government service" in html
    # New Views for Phase 1
    assert "field-tasks-view" in html
    assert "triage-view" in html
    assert "dispatch-view" in html
    assert "transparency-view" in html
    # 4-step wizard
    assert "wizard-node-1" in html
    assert "dpdp-consent-checkbox" in html

def test_city_weather_aqi_endpoint():
    res = client.get("/api/v1/cities/bengaluru/weather-aqi")
    assert res.status_code == 200
    data = res.json()
    assert data["city_name"] == "Bengaluru"
    assert data["corporation"] == "BBMP"
    assert "temperature_c" in data
    assert "aqi" in data
    assert "aqi_category" in data
    assert "flood_hazard_level" in data
    assert data["control_rooms_active"] is True

def test_signature_interactive_features_present_in_index():
    res = client.get("/")
    assert res.status_code == 200
    html = res.text
    # Audio Engine & Celebration & Certificate scripts
    assert "js/audio_engine.js" in html
    assert "js/celebration.js" in html
    assert "js/certificate_generator.js" in html
    # Live Weather & AQI widget
    assert "city-weather-widget" in html
    # Scenario Presets
    assert "scenario-preset-container" in html
    assert "applyGrievancePreset" in html
    # Visual Agent Flowchart
    assert "agent-flow-container" in html
    assert "agent-visual-flowtrack" in html
    # Keyboard Shortcuts modal
    assert "shortcuts-modal" in html
    # Certificate button
    assert "openCertificateModal" in html
    # Flagship Feature Scripts
    assert "js/oscilloscope.js" in html
    assert "js/vision_canvas.js" in html
    assert "js/fleet_simulation.js" in html
    assert "js/rupee_ledger.js" in html
    assert "js/homography_inspector.js" in html
    assert "js/h3_hex_grid.js" in html
    assert "js/ivr_simulator.js" in html
    assert "js/contractor_scorecard.js" in html
    assert "js/offline_pwa_sync.js" in html
    assert "js/realtime_client.js" in html
    # Canvases & Interactive Panels
    assert "vision-diagnostic-canvas" in html
    assert "voice-oscilloscope-canvas" in html
    assert "fleet-telemetry-panel" in html
    assert "btn-toggle-simulation" in html
    assert "rupee-transparency-ledger" in html
    assert "tax-calculator-input" in html
    assert "homography-audit-modal" in html
    assert "ivr-phone-modal" in html
    assert "homography-canvas" in html
    assert "realtime-wire-drawer" in html
    assert "realtime-status-pill" in html
    assert "live-ist-clock" in html
    assert "national-tricolor-stripe" in html

def test_vision_diagnostics_endpoint():
    # Test authentic pothole detection
    res = client.post("/api/v1/complaints/vision-diagnostics", json={
        "image_identifier": "sample_pothole",
        "department": "Roads & Traffic Infrastructure",
        "lat": 12.9716,
        "lon": 77.5946
    })
    assert res.status_code == 200
    data = res.json()
    assert data["detected_class"] == "pothole"
    assert data["is_authentic"] is True
    assert data["status_label"] == "Auto-Verified"
    assert len(data["objects"]) > 0
    assert "box" in data["objects"][0]
    assert data["spam_shield"]["is_spam"] is False

    # Test spam/meme shield trigger
    res_spam = client.post("/api/v1/complaints/vision-diagnostics", json={
        "image_identifier": "sample_meme_selfie.png",
        "department": "Roads & Traffic Infrastructure"
    })
    assert res_spam.status_code == 200
    data_spam = res_spam.json()
    assert data_spam["detected_class"] == "unrelated_or_spam"
    assert data_spam["is_authentic"] is False
    assert data_spam["spam_shield"]["is_spam"] is True
    assert data_spam["spam_shield"]["verdict"] == "FLAGGED_SPAM_SHIELD_ACTIVE"

def test_fleet_telemetry_endpoint():
    res = client.get("/api/v1/dispatch/fleet-telemetry?city=bengaluru")
    assert res.status_code == 200
    data = res.json()
    assert data["active_squads_count"] >= 3
    assert len(data["squads"]) >= 3
    squad_alpha = data["squads"][0]
    assert "Squad Alpha-1" in squad_alpha["name"]
    assert "lat" in squad_alpha and "lon" in squad_alpha
    assert "equipment" in squad_alpha
    assert len(data["radio_chatter"]) > 0

def test_rupee_transparency_ledger_endpoint():
    res = client.get("/api/v1/analytics/rupee-ledger?city=bengaluru")
    assert res.status_code == 200
    data = res.json()
    assert data["total_annual_budget_crores"] > 0
    assert data["taxpayer_savings_inr"] > 0
    assert "₹" in data["taxpayer_savings_formatted"]
    assert len(data["schedule_of_rates"]) >= 5
    assert len(data["property_tax_distribution"]) >= 5

def test_contractor_scorecards_endpoint():
    res = client.get("/api/v1/contractors/scorecards")
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, list)
    assert len(data) >= 4
    c1 = data[0]
    assert "contractor_id" in c1
    assert "name" in c1
    assert "sla_compliance_pct" in c1
    assert "recurrence_failure_rate_pct" in c1
    assert "performance_grade" in c1
    assert "penalties_levied_inr" in c1

    # Filter by city
    res_city = client.get("/api/v1/contractors/scorecards?city=Bengaluru")
    assert res_city.status_code == 200
    data_city = res_city.json()
    assert isinstance(data_city, list)
    assert len(data_city) >= 1
    assert data_city[0]["city"] == "Bengaluru"

def test_homography_verification_endpoint():
    # Test genuine repair verification
    res_valid = client.post("/api/v1/contractors/verify-resolution", json={
        "complaint_id": "CMP-BLR-001",
        "original_image_tag": "sample_pothole",
        "resolution_image_tag": "sample_repaired_asphalt",
        "original_lat": 12.9716,
        "original_lon": 77.5946,
        "resolution_lat": 12.9716,
        "resolution_lon": 77.5946,
        "resolution_notes": "Bituminous cold-mix patching completed."
    })
    assert res_valid.status_code == 200
    data_valid = res_valid.json()
    assert data_valid["is_authentic_resolution"] is True
    assert data_valid["homography_match_score"] >= 0.70
    assert data_valid["status_verdict"] == "VERIFIED_GENUINE_REPAIR"
    assert data_valid["contractor_accountability"]["penalty_levied_inr"] == 0
    assert len(data_valid["landmark_alignment_points"]) >= 3

    # Test false-closure detection (shoes/office desk photo)
    res_fake = client.post("/api/v1/contractors/verify-resolution", json={
        "complaint_id": "CMP-BLR-001",
        "original_image_tag": "sample_pothole",
        "resolution_image_tag": "sample_shoes_desk",
        "original_lat": 12.9716,
        "original_lon": 77.5946,
        "resolution_lat": 12.9734,
        "resolution_lon": 77.5946,
        "resolution_notes": "Fake indoor photo."
    })
    assert res_fake.status_code == 200
    data_fake = res_fake.json()
    assert data_fake["is_authentic_resolution"] is False
    assert data_fake["status_verdict"] == "FALSE_CLOSURE_PREVENTED"
    assert "Clause 14B" in data_fake["contractor_accountability"]["statutory_clause"]
    assert data_fake["contractor_accountability"]["penalty_levied_inr"] > 0

def test_citizen_signoff_endpoint():
    # Test citizen satisfaction approval
    res_appr = client.post("/api/v1/contractors/citizen-signoff", json={
        "complaint_id": "CMP-BLR-001",
        "is_satisfied": True,
        "feedback_notes": "Road looks great now!",
        "citizen_phone": "9876543210"
    })
    assert res_appr.status_code == 200
    data_appr = res_appr.json()
    assert data_appr["status"] == "RESOLVED_VERIFIED"
    assert data_appr["karma_points_awarded"] > 0
    assert data_appr["certificate_eligible"] is True

    # Test citizen escalation / rejection
    res_esc = client.post("/api/v1/contractors/citizen-signoff", json={
        "complaint_id": "CMP-BLR-001",
        "is_satisfied": False,
        "feedback_notes": "Pothole is still completely open and filled with water!",
        "citizen_phone": "9876543210"
    })
    assert res_esc.status_code == 200
    data_esc = res_esc.json()
    assert data_esc["status"] == "ESCALATED_TO_JAN_SUNWAI"
    assert data_esc["penalty_notice_issued"] is True

def test_h3_hex_cells_endpoint():
    res = client.get("/api/v1/contractors/h3-cells?city=bengaluru")
    assert res.status_code == 200
    data = res.json()
    assert data["city"] == "Bengaluru"
    assert "total_hex_cells" in data
    assert len(data["cells"]) > 0
    cell0 = data["cells"][0]
    assert cell0["h3_index"].startswith("89")
    assert len(cell0["boundary"]) == 6  # 6 hexagon vertices
    assert "incident_count" in cell0
    assert "critical_count" in cell0




