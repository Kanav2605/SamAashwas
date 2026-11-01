import pytest
from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.core.realtime import realtime_hub

client = TestClient(app)

def test_realtime_stream_history_endpoint():
    res = client.get("/api/v1/stream/history")
    assert res.status_code == 200
    data = res.json()
    assert "total_buffered" in data
    assert "events" in data
    assert isinstance(data["events"], list)

def test_realtime_broadcast_test_endpoint():
    res = client.post("/api/v1/stream/broadcast-test", json={
        "type": "CUSTOM_ALERT",
        "data": {"message": "Road work in progress"}
    })
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "broadcasted"
    assert data["type"] == "CUSTOM_ALERT"

    # Verify event appears in history
    hist = client.get("/api/v1/stream/history").json()
    found = any(e.get("type") == "CUSTOM_ALERT" for e in hist["events"])
    assert found is True

def test_realtime_websocket_connection_and_ping():
    with client.websocket_connect("/ws/live") as websocket:
        # First message is connection handshake
        handshake = websocket.receive_json()
        assert handshake["type"] == "CONNECTION_ESTABLISHED"
        assert "server_time_ist" in handshake

        # Send PING
        websocket.send_json({"action": "PING", "timestamp": 123456789})

        # Receive until PONG is returned (skipping any replayed history)
        pong_received = False
        for _ in range(10):
            msg = websocket.receive_json()
            if msg.get("type") == "PONG":
                assert msg.get("client_timestamp") == 123456789
                pong_received = True
                break
        assert pong_received is True

def test_realtime_complaint_submission_broadcast():
    # Submit complaint and verify broadcast event in realtime_hub
    res = client.post("/api/v1/complaints/submit", json={
        "raw_text": "Severe watermain leakage flooding pavement near MG Road metro station",
        "lat": 12.9716,
        "lon": 77.5946,
        "citizen_name": "Deepak Mehta",
        "citizen_phone": "9876543210"
    })
    assert res.status_code == 200

    # Verify NEW_GRIEVANCE_LODGED was logged in event history
    history = realtime_hub.get_history()
    complaint_events = [e for e in history if e.get("type") == "NEW_GRIEVANCE_LODGED"]
    assert len(complaint_events) > 0
    latest_event = complaint_events[-1]
    assert latest_event["data"]["citizen_name"] == "Deepak Mehta"

def test_realtime_citizen_login_logout_broadcast():
    # Login via preset
    res_login = client.post("/api/v1/auth/login", json={"preset_id": "rajesh_kumar"})
    assert res_login.status_code == 200
    login_data = res_login.json()
    token = login_data["access_token"]

    # Verify CITIZEN_PRESENCE_LOGIN was broadcast
    history = realtime_hub.get_history()
    login_events = [e for e in history if e.get("type") == "CITIZEN_PRESENCE_LOGIN"]
    assert len(login_events) > 0
    assert login_events[-1]["data"]["name"] == "Rajesh Kumar"

    # Logout
    res_logout = client.post("/api/v1/auth/logout", headers={"Authorization": f"Bearer {token}"})
    assert res_logout.status_code == 200

    # Verify CITIZEN_PRESENCE_LOGOUT was broadcast
    history_after = realtime_hub.get_history()
    logout_events = [e for e in history_after if e.get("type") == "CITIZEN_PRESENCE_LOGOUT"]
    assert len(logout_events) > 0
    assert logout_events[-1]["data"]["status"] == "LOGGED_OUT"
