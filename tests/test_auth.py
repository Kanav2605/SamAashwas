import pytest
from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def test_auth_presets_endpoint():
    res = client.get("/api/v1/auth/presets")
    assert res.status_code == 200
    presets = res.json()
    assert isinstance(presets, list)
    assert len(presets) >= 4
    preset_ids = [p["preset_id"] for p in presets]
    assert "rajesh_kumar" in preset_ids
    assert "priya_sharma" in preset_ids
    assert "aarav_sharma" in preset_ids
    assert "sunita_patel" in preset_ids

def test_preset_login_rajesh_kumar():
    res = client.post("/api/v1/auth/login", json={"preset_id": "rajesh_kumar"})
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "SUCCESS"
    assert "access_token" in data
    assert data["user"]["name"] == "Rajesh Kumar"
    assert data["user"]["phone"] == "9876543210"
    assert data["user"]["karma_points"] == 850

    # Test me endpoint with bearer token
    token = data["access_token"]
    me_res = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert me_res.status_code == 200
    me_data = me_res.json()
    assert me_data["name"] == "Rajesh Kumar"

def test_preset_login_priya_sharma():
    res = client.post("/api/v1/auth/login", json={"preset_id": "priya_sharma"})
    assert res.status_code == 200
    data = res.json()
    assert data["user"]["name"] == "Priya Sharma"
    assert data["user"]["role"] == "Ward Volunteer"
    assert data["user"]["city"] == "Delhi"

def test_mobile_otp_flow():
    # 1. Request OTP
    phone = "9823456789"
    res_otp = client.post("/api/v1/auth/login", json={"phone": phone})
    assert res_otp.status_code == 200
    otp_data = res_otp.json()
    assert otp_data["status"] == "OTP_SENT"
    assert otp_data["otp_sent"] is True
    assert otp_data["demo_otp"] == "123456"

    # 2. Verify with wrong OTP
    res_wrong = client.post("/api/v1/auth/verify-otp", json={"phone": phone, "otp": "999999"})
    assert res_wrong.status_code == 400

    # 3. Verify with correct OTP
    res_correct = client.post("/api/v1/auth/verify-otp", json={"phone": phone, "otp": "123456", "name": "Vikas Rao", "city": "Bengaluru"})
    assert res_correct.status_code == 200
    auth_data = res_correct.json()
    assert auth_data["status"] == "SUCCESS"
    assert auth_data["user"]["phone"] == phone
    assert auth_data["user"]["name"] == "Vikas Rao"

def test_auth_me_unauthorized():
    res = client.get("/api/v1/auth/me")
    assert res.status_code == 401

    res_invalid = client.get("/api/v1/auth/me", headers={"Authorization": "Bearer invalid_tok_123"})
    assert res_invalid.status_code == 401

def test_logout_flow():
    login_res = client.post("/api/v1/auth/login", json={"preset_id": "aarav_sharma"})
    token = login_res.json()["access_token"]

    # Verify session is active
    assert client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"}).status_code == 200

    # Logout
    logout_res = client.post("/api/v1/auth/logout", headers={"Authorization": f"Bearer {token}"})
    assert logout_res.status_code == 200

    # Verify session is now invalidated
    assert client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"}).status_code == 401

def test_complaint_submission_with_citizen_auth():
    # Login as Sunita Patel
    login_res = client.post("/api/v1/auth/login", json={"preset_id": "sunita_patel"})
    token = login_res.json()["access_token"]

    # Submit complaint using auth token
    payload = {
        "raw_text": "Streetlight broken on FC Road near college gate since 3 days",
        "lat": 18.5204,
        "lon": 73.8567,
        "channel": "web_portal"
    }
    res = client.post("/api/v1/complaints/submit", json=payload, headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 200
    data = res.json()
    assert data["citizen_name"] == "Sunita Patel"
    assert data["citizen_phone"] == "9822054321"

def test_direct_tracking_endpoint():
    # Test tracking lookup for seeded tickets (e.g. SYN-0001 or any master ticket)
    res_tickets = client.get("/api/v1/master-tickets")
    assert res_tickets.status_code == 200
    tickets = res_tickets.json()
    assert len(tickets) > 0
    test_id = tickets[0]["master_ticket_id"]

    # Direct tracking lookup
    res_track = client.get(f"/api/v1/tracking/{test_id}")
    assert res_track.status_code == 200
    data = res_track.json()
    assert data["tracking_id"] == test_id
    assert "ward_name" in data

    # Non-existent tracking id
    res_404 = client.get("/api/v1/tracking/NON_EXISTENT_ID")
    assert res_404.status_code == 404

def test_frontend_auth_and_button_components():
    res = client.get("/")
    assert res.status_code == 200
    html = res.text
    # Verify Citizen Authentication widget and Login Modal
    assert "citizen-auth-widget" in html
    assert "citizen-login-modal" in html
    assert "मेरी पहचान" in html
    assert "Rajesh Kumar" in html
    assert "Priya Sharma" in html
    assert "Aarav Sharma" in html
    assert "Sunita Patel" in html

    # Verify interactive controls
    assert "gallery-filter-bar" in html
    assert "map-floating-controls" in html
    assert "jan-filter-all" in html
    assert "handleReportIssueClick" in html
    assert "handleGrievanceTabClick" in html

def test_transformations_category_filter():
    res_all = client.get("/api/v1/transformations")
    assert res_all.status_code == 200
    all_items = res_all.json()
    assert len(all_items) > 0

    res_roads = client.get("/api/v1/transformations?category=Roads")
    assert res_roads.status_code == 200
    road_items = res_roads.json()
    assert len(road_items) > 0
    for item in road_items:
        assert "road" in item["category"].lower() or "road" in item["title"].lower()

def test_voice_grievance_with_citizen_auth():
    login_res = client.post("/api/v1/auth/login", json={"preset_id": "priya_sharma"})
    token = login_res.json()["access_token"]

    payload = {
        "spoken_language": "hi-IN",
        "audio_transcript": "Ward 83 mein street light band hai andhera faila hua hai",
        "lat": 28.6514,
        "lon": 77.1907
    }
    res = client.post("/api/v1/complaints/voice-note", json=payload, headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 200
    data = res.json()
    assert data["citizen_name"] == "Priya Sharma"
    assert data["citizen_phone"] == "9811012002"

