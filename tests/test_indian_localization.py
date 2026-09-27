import pytest
from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.core.nlp_engine import (
    nlp_engine,
    detect_language,
    extract_ward,
    get_national_mission_and_sla
)
from backend.app.models.schemas import UrgencyEnum
from backend.app.db.database import db

client = TestClient(app)

def test_kannada_language_detection_and_nlp():
    # Kannada pothole grievance
    kannada_text = "ರಸ್ತೆಯಲ್ಲಿ ದೊಡ್ಡ ಗುಂಡಿ ಬಿದ್ದಿದೆ, ವಾಹನ ಸವಾರರಿಗೆ ಅಪಘಾತವಾಗುವ ಸಂಭವವಿದೆ ಬೇಗ ಸರಿಮಾಡಿ"
    lang = detect_language(kannada_text)
    assert lang == "Kannada"

    res = nlp_engine.analyze(kannada_text)
    assert res.language_detected == "Kannada"
    assert res.department == "Roads & Traffic Infrastructure"
    assert "Swachh" not in res.national_mission
    assert "Road Safety" in res.national_mission

def test_kannada_ward_and_digits():
    text = "ವಾರ್ಡ್ ೨ ಕಸದ ಸಮಸ್ಯೆ ಹೆಚ್ಚಾಗಿದೆ ದುರ್ವಾಸನೆ ಬರುತ್ತಿದೆ"
    ward = extract_ward(text)
    assert "2" in ward
    res = nlp_engine.analyze(text)
    assert res.department == "Sanitation & Solid Waste"
    assert "Swachh Bharat" in res.national_mission

def test_tamil_language_detection_and_nlp():
    # Tamil streetlight complaint
    tamil_text = "தெரு விளக்கு எரியவில்லை, இரவு நேரத்தில் மிகவும் இருட்டாக உள்ளது"
    lang = detect_language(tamil_text)
    assert lang == "Tamil"

    res = nlp_engine.analyze(tamil_text)
    assert res.language_detected == "Tamil"
    assert res.department == "Electrical & Streetlighting"
    assert "Smart Cities" in res.national_mission

def test_tamil_water_sewage_routing():
    tamil_sewage = "சாக்கடை நீர் சாலையில் வழிகிறது, உடனடியாக சரிசெய்யவும்"
    res = nlp_engine.analyze(tamil_sewage)
    assert res.department == "Water Supply & Sewage"
    assert "AMRUT" in res.national_mission or "Jal Jeevan" in res.national_mission

def test_national_mission_and_sla_mapping():
    mission, sla = get_national_mission_and_sla("Sanitation & Solid Waste", UrgencyEnum.HIGH)
    assert "Swachh Bharat" in mission
    assert sla == 24

    mission_water, sla_water = get_national_mission_and_sla("Water Supply & Sewage", UrgencyEnum.CRITICAL)
    assert "AMRUT" in mission_water or "Jal Jeevan" in mission_water
    assert sla_water == 12

def test_voice_note_api_endpoint():
    payload = {
        "spoken_language": "kn-IN",
        "audio_transcript": "ರಸ್ತೆ ಗುಂಡಿ ದುರಸ್ತಿ ಮಾಡಿ, 27th Main HSR Layout",
        "lat": 12.9121,
        "lon": 77.6446,
        "citizen_name": "Suresh Gowda",
        "citizen_phone": "9845012399"
    }
    res = client.post("/api/v1/complaints/voice-note", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["channel"] == "voice_note"
    assert "kn-IN" in (data.get("audio_transcript") or "")
    assert data["department"] == "Roads & Traffic Infrastructure"
    assert data["master_ticket_id"] is not None

def test_jan_sunwai_escalation_endpoint_and_filter():
    # Submit critical grievance
    payload = {
        "raw_text": "Emergency! Dangerous open transformer wire sparking near school gate, Ward 1",
        "lat": 12.9716,
        "lon": 77.6412,
        "citizen_name": "Rajesh Kumar",
        "citizen_phone": "9811223399",
        "channel": "web_portal"
    }
    submit_res = client.post("/api/v1/complaints/submit", json=payload)
    assert submit_res.status_code == 200
    sub_data = submit_res.json()
    master_id = sub_data["master_ticket_id"]

    # Verify ticket was automatically marked ESCALATED to Jan Sunwai due to critical urgency
    ticket_res = client.get(f"/api/v1/master-tickets/{master_id}")
    assert ticket_res.status_code == 200
    ticket_data = ticket_res.json()
    assert ticket_data["jan_sunwai_status"] == "ESCALATED"
    assert ticket_data["corporator"] is not None
    assert "name" in ticket_data["corporator"]

    # Test filtering by Jan Sunwai
    js_res = client.get("/api/v1/master-tickets?jan_sunwai_only=true")
    assert js_res.status_code == 200
    js_tickets = js_res.json()
    assert any(t["master_ticket_id"] == master_id for t in js_tickets)

    # Test explicit manual escalate endpoint
    esc_res = client.post(f"/api/v1/master-tickets/{master_id}/escalate-jan-sunwai")
    assert esc_res.status_code == 200
    assert esc_res.json()["jan_sunwai_status"] == "ESCALATED"

def test_whatsapp_webhook_kannada():
    payload = {
        "From": "whatsapp:+919845012345",
        "Body": "ರಸ್ತೆಯಲ್ಲಿ ದೊಡ್ಡ ಗುಂಡಿ ಬಿದ್ದಿದೆ, ವಾಹನ ಸಂಚಾರ ಕಷ್ಟವಾಗಿದೆ",
        "Latitude": 12.9121,
        "Longitude": 77.6446,
        "LanguagePref": "Kannada"
    }
    res = client.post("/api/v1/webhook/whatsapp", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert "ನಮಸ್ಕಾರ" in data["reply_message"]
    assert data["national_mission"] is not None
    assert data["status"] == "PROCESSED"

def test_whatsapp_webhook_tamil():
    payload = {
        "From": "whatsapp:+919845012346",
        "Body": "குப்பை கொட்டப்பட்டு துர்நாற்றம் வீசுகிறது",
        "Latitude": 12.9716,
        "Longitude": 77.6412,
        "LanguagePref": "Tamil"
    }
    res = client.post("/api/v1/webhook/whatsapp", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert "வணக்கம்" in data["reply_message"]
    assert data["status"] == "PROCESSED"
