import pytest
from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.db.database import db

client = TestClient(app)

def test_endorse_transformation_success():
    res_before = client.get("/api/v1/transformations")
    assert res_before.status_code == 200
    t0 = res_before.json()[0]
    initial_endorsements = t0["endorsements"]
    tid = t0["id"]

    res_endorse = client.post(f"/api/v1/transformations/{tid}/endorse")
    assert res_endorse.status_code == 200
    data = res_endorse.json()
    assert data["success"] is True
    assert data["transformation_id"] == tid
    assert data["endorsements"] == initial_endorsements + 1
    assert data["karma_points_awarded"] == 50

def test_endorse_transformation_404():
    res = client.post("/api/v1/transformations/NON-EXISTENT-TR-999/endorse")
    assert res.status_code == 404
    assert "not found" in res.json()["detail"].lower()

def test_copilot_emergency_helplines():
    payload = {
        "query": "What is the emergency municipal control room helpline number?",
        "language": "en-IN",
        "city": "bengaluru"
    }
    res = client.post("/api/v1/copilot/query", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["intent"] == "emergency_helplines"
    assert "112" in data["reply_text"]
    assert "1533" in data["reply_text"]
    assert data["suggested_action"]["action_type"] == "call"

def test_copilot_file_complaint_hindi():
    payload = {
        "query": "सड़क पर गहरा गड्ढा है दुर्घटना हो सकती है कृपया ठीक करें",
        "language": "hi-IN"
    }
    res = client.post("/api/v1/copilot/query", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["intent"] == "file_complaint"
    assert data["language"] == "hi-IN"
    assert data["suggested_action"]["action_type"] == "prefill_complaint"
    assert "Roads & Traffic Infrastructure" in data["suggested_action"]["params"]["category"]

def test_copilot_karma_and_tax_rebate():
    payload = {
        "query": "How can I earn citizen karma points and claim the 5% property tax rebate?",
        "language": "en-IN"
    }
    res = client.post("/api/v1/copilot/query", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["intent"] == "karma_rewards"
    assert "5%" in data["reply_text"] or "rebate" in data["reply_text"].lower()
    assert data["suggested_action"]["target"] == "section-rewards"

def test_copilot_ticket_tracking_with_seeded_master():
    masters = list(db.master_tickets.keys())
    if masters:
        target_id = masters[0]
        payload = {"query": f"Check status of ticket {target_id}", "language": "en-IN"}
        res = client.post("/api/v1/copilot/query", json=payload)
        assert res.status_code == 200
        data = res.json()
        assert data["intent"] == "ticket_lookup"
        assert target_id in data["reply_text"]
        assert data["suggested_action"]["action_type"] == "track_id"

def test_copilot_general_greeting():
    payload = {"query": "Hello, how can you help me today?", "language": "en-IN", "user_name": "Pooja"}
    res = client.post("/api/v1/copilot/query", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["intent"] == "general_greeting"
    assert "Pooja" in data["reply_text"]
    assert len(data["audio_speakable_text"]) > 10
