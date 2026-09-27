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

def test_predictive_ward_risk():
    res = client.get("/api/v1/predictive-maintenance/ward-risk")
    assert res.status_code == 200
    wards = res.json()
    assert len(wards) > 0
    assert "risk_score" in wards[0]
