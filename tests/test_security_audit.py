import pytest
from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.config import settings
from backend.app.db.seed_data import seed_database_and_export
from backend.app.db.database import db

client = TestClient(app)

@pytest.fixture(autouse=True)
def ensure_db_seeded():
    if not db.master_tickets:
        seed_database_and_export()

def _get_any_active_ticket_id():
    for t_id, t in db.master_tickets.items():
        if t.status in ["OPEN", "IN_PROGRESS"]:
            return t_id
    # If none, submit one
    resp = client.post("/api/v1/complaints/submit", json={
        "raw_text": "Broken street light wire sparking near market Ward 1",
        "lat": 12.9716,
        "lon": 77.6412,
        "citizen_name": "Rohan Verma",
        "citizen_phone": "9876543211",
        "channel": "web_portal"
    })
    return resp.json()["master_ticket_id"]

def test_s1_authentication_guard_on_patch_master_ticket():
    ticket_id = _get_any_active_ticket_id()

    # 1. Unauthenticated request must return 401
    resp = client.patch(f"/api/v1/master-tickets/{ticket_id}", json={"status": "IN_PROGRESS"})
    assert resp.status_code == 401
    assert "Authentication required" in resp.json()["detail"]

    # 2. Authenticated Citizen (non-officer) must return 403 Forbidden
    login_resp = client.post("/api/v1/auth/login", json={"preset_id": "rajesh_kumar"})
    assert login_resp.status_code == 200
    citizen_token = login_resp.json()["access_token"]

    resp_forbidden = client.patch(
        f"/api/v1/master-tickets/{ticket_id}",
        json={"status": "IN_PROGRESS"},
        headers={"Authorization": f"Bearer {citizen_token}"}
    )
    assert resp_forbidden.status_code == 403
    assert "Forbidden" in resp_forbidden.json()["detail"]

    # 3. Authenticated Officer must succeed
    officer_login = client.post("/api/v1/auth/login", json={"preset_id": "vikas_officer"})
    assert officer_login.status_code == 200
    officer_token = officer_login.json()["access_token"]

    resp_allowed = client.patch(
        f"/api/v1/master-tickets/{ticket_id}",
        json={"status": "IN_PROGRESS"},
        headers={"Authorization": f"Bearer {officer_token}"}
    )
    assert resp_allowed.status_code == 200
    assert resp_allowed.json()["status"] == "IN_PROGRESS"


def test_s1_authentication_guard_on_jan_sunwai_escalation():
    ticket_id = _get_any_active_ticket_id()

    # 1. Unauthenticated request must return 401
    resp = client.post(f"/api/v1/master-tickets/{ticket_id}/escalate-jan-sunwai")
    assert resp.status_code == 401

    # 2. Authenticated citizen can escalate
    login_resp = client.post("/api/v1/auth/login", json={"preset_id": "rajesh_kumar"})
    token = login_resp.json()["access_token"]

    resp_esc = client.post(
        f"/api/v1/master-tickets/{ticket_id}/escalate-jan-sunwai",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert resp_esc.status_code == 200
    assert resp_esc.json()["jan_sunwai_status"] == "ESCALATED"
    assert resp_esc.json()["escalated_by"] == "Rajesh Kumar"


def test_s2_pii_masking_on_public_complaints_endpoint():
    # Submit a complaint first to guarantee data
    client.post("/api/v1/complaints/submit", json={
        "raw_text": "Severe gutter overflow near market entrance",
        "lat": 12.9716,
        "lon": 77.6412,
        "citizen_name": "Rohan Verma",
        "citizen_phone": "9876543211",
        "channel": "web_portal"
    })

    # 1. Unauthenticated public request -> masked PII
    public_resp = client.get("/api/v1/complaints?limit=10")
    assert public_resp.status_code == 200
    items = public_resp.json()
    assert len(items) > 0

    first = items[0]
    # Phone must contain masking asterisks and NOT reveal full number
    phone = first.get("citizen_phone", "")
    assert "***" in phone

    # 2. Privileged officer request -> unmasked PII
    officer_login = client.post("/api/v1/auth/login", json={"preset_id": "vikas_officer"})
    officer_token = officer_login.json()["access_token"]

    officer_resp = client.get(
        "/api/v1/complaints?limit=10",
        headers={"Authorization": f"Bearer {officer_token}"}
    )
    assert officer_resp.status_code == 200
    officer_items = officer_resp.json()
    assert len(officer_items) > 0
    assert not officer_items[0].get("citizen_phone", "").startswith("+91 98***")


def test_s2_pii_masking_on_master_ticket_details():
    ticket_id = _get_any_active_ticket_id()
    # Unauthenticated caller -> citizen reports in ticket must have masked phone
    resp = client.get(f"/api/v1/master-tickets/{ticket_id}")
    assert resp.status_code == 200
    reports = resp.json().get("citizen_reports", [])
    if reports:
        assert "***" in reports[0].get("citizen_phone", "")


def test_s4_cors_allowlist_configured():
    # Settings must have an explicit origin allowlist
    assert settings.CORS_ORIGINS != "*"
    assert "http://127.0.0.1:8000" in settings.CORS_ORIGINS


def test_s5_input_bounds_validation():
    # 1. Text too short (< 3 chars)
    resp_short = client.post("/api/v1/complaints/submit", json={
        "raw_text": "hi",
        "lat": 12.9716,
        "lon": 77.6412
    })
    assert resp_short.status_code == 422

    # 2. Text too long (> 2000 chars)
    resp_long = client.post("/api/v1/complaints/submit", json={
        "raw_text": "a" * 2005,
        "lat": 12.9716,
        "lon": 77.6412
    })
    assert resp_long.status_code == 422

    # 3. Latitude outside India bounding box (< 6.0 or > 38.0)
    resp_bad_lat = client.post("/api/v1/complaints/submit", json={
        "raw_text": "Broken streetlight near main gate",
        "lat": 48.8566,
        "lon": 77.6412
    })
    assert resp_bad_lat.status_code == 422

    # 4. Longitude outside India bounding box (< 68.0 or > 98.0)
    resp_bad_lon = client.post("/api/v1/complaints/submit", json={
        "raw_text": "Broken streetlight near main gate",
        "lat": 12.9716,
        "lon": 2.3522
    })
    assert resp_bad_lon.status_code == 422
