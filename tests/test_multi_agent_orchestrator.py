import pytest
from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.agents.orchestrator import agent_orchestrator
from backend.app.agents.citizen_reception_agent import CitizenReceptionAgent
from backend.app.agents.vision_fraud_agent import VisualVerificationFraudAgent
from backend.app.agents.geo_dedup_agent import GeoDeduplicationAgent
from backend.app.agents.ward_sla_routing_agent import WardSlaRoutingAgent
from backend.app.agents.predictive_warning_agent import PredictiveDisasterWarningAgent
from backend.app.agents.ombudsman_escalation_agent import CivicOmbudsmanJanSunwaiAgent
from backend.app.db.database import db

client = TestClient(app)

def test_agent_manifest():
    manifest = agent_orchestrator.get_agent_manifest()
    assert len(manifest) == 6
    names = [a["name"] for a in manifest]
    assert "Citizen Reception Agent" in names
    assert "Visual Verification & Fraud Agent" in names
    assert "Geo-Deduplication & Clustering Agent" in names
    assert "Ward & SLA Routing Agent" in names
    assert "Predictive Maintenance & Disaster Warning Agent" in names
    assert "Civic Ombudsman & Jan Sunwai Escalation Agent" in names

def test_citizen_reception_agent_hinglish():
    agent = CitizenReceptionAgent()
    context = {
        "raw_text": "Bhaiya road par street light 4 din se band hai, near metro pillar 108",
        "channel": "whatsapp",
        "citizen_name": "Rohan"
    }
    result = agent.run(context)
    assert result.status == "SUCCESS"
    assert "Electrical & Streetlighting" in context["department"]
    assert "pillar 108" in context["location_landmark"].lower() or "metro" in context["location_landmark"].lower() or "road" in context["location_landmark"].lower()
    assert result.outputs["citizen_charter_sla_hours"] is not None

def test_visual_verification_fraud_agent_detection():
    agent = VisualVerificationFraudAgent()
    
    # Authentic image matching department
    ctx_authentic = {
        "raw_text": "Deep pothole causing accidents",
        "department": "Roads & Traffic Infrastructure",
        "image_category_hint": "pothole"
    }
    res_auth = agent.run(ctx_authentic)
    assert res_auth.status == "VERIFIED"
    assert res_auth.outputs["is_authentic"] is True

    # Spam / meme fraud image
    ctx_spam = {
        "raw_text": "Sewer overflow",
        "department": "Water Supply & Sewage",
        "image_category_hint": "unrelated_or_spam"
    }
    res_spam = agent.run(ctx_spam)
    assert "FLAGGED" in res_spam.status
    assert res_spam.outputs["is_authentic"] is False

def test_ward_sla_routing_agent_delhi_mcd():
    agent = WardSlaRoutingAgent()
    context = {
        "lat": 28.6514,
        "lon": 77.1907,
        "wards": db.wards,
        "urgency": "Critical",
        "department": "Water Supply & Sewage"
    }
    result = agent.run(context)
    assert result.status == "ROUTED"
    assert "Karol Bagh" in result.outputs["mcd_zone"]
    assert result.outputs["citizen_charter_sla_hours"] == 12
    assert "corporator" in result.outputs

def test_predictive_disaster_warning_agent():
    agent = PredictiveDisasterWarningAgent()
    context = {
        "assigned_ward": db.wards[0],
        "active_complaint_count": 5,
        "rainfall_24h_mm": 50.0,
        "rainfall_48h_mm": 85.0,
        "assets": db.assets
    }
    result = agent.run(context)
    assert result.status in ["ALERT", "NORMAL"]
    assert "risk_score" in result.outputs
    assert result.outputs["desilting_readiness_pct"] is not None

def test_civic_ombudsman_escalation():
    agent = CivicOmbudsmanJanSunwaiAgent()
    
    # Standard low-urgency grievance
    ctx_normal = {"urgency": "Low", "report_count": 1, "is_sla_breached": False}
    res_norm = agent.run(ctx_normal)
    assert res_norm.status == "MONITORED"

    # Multi-citizen cluster (3+ reports) -> Automatic Jan Sunwai docketing
    ctx_escalated = {"urgency": "Low", "report_count": 4, "is_sla_breached": False}
    res_esc = agent.run(ctx_escalated)
    assert res_esc.status == "ESCALATED"
    assert res_esc.outputs["jan_sunwai_status"] == "ESCALATED"

def test_api_agents_status():
    res = client.get("/api/v1/agents/status")
    assert res.status_code == 200
    agents = res.json()
    assert len(agents) == 6

def test_api_agents_orchestrate_and_simulate():
    payload = {
        "scenario": "waterlogging_monsoon"
    }
    res = client.post("/api/v1/agents/simulate", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["orchestration_status"] == "COMPLETED"
    assert len(data["agent_trace"]) == 6
    assert data["department"] == "Water Supply & Sewage"
    assert "Minto Bridge" in data["narrative_summary"] or "water" in data["narrative_summary"].lower()

def test_complaint_submission_with_agent_trace_and_mcd_zone():
    payload = {
        "raw_text": "Yamuna floodplain Kashmiri gate area waterlogging danger near Civil Lines bus stop",
        "lat": 28.6814,
        "lon": 77.2228,
        "citizen_name": "Devendra Tyagi",
        "citizen_phone": "9811099889",
        "channel": "web_portal",
        "image_category_hint": "waterlogging"
    }
    res = client.post("/api/v1/complaints/submit", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert "Civil Lines" in data["mcd_zone"]
    assert data["agent_trace"] is not None
    assert len(data["agent_trace"]) == 6
    complaint_id = data["complaint_id"]

    # Test tracking endpoint
    track_res = client.get(f"/api/v1/tracking/{complaint_id}")
    assert track_res.status_code == 200
    track_data = track_res.json()
    assert track_data["tracking_id"] == complaint_id
    assert track_data["type"] == "complaint"
    assert track_data["mcd_zone"] == data["mcd_zone"]
    assert len(track_data["agent_trace"]) == 6

def test_ombudsman_manual_escalate_api():
    # Submit complaint
    sub_res = client.post("/api/v1/complaints/submit", json={
        "raw_text": "Minor street sign loose on corner",
        "lat": 12.9716,
        "lon": 77.6412,
        "citizen_name": "Alok",
        "citizen_phone": "9811099880"
    })
    c_id = sub_res.json()["complaint_id"]

    esc_res = client.post("/api/v1/agents/ombudsman/escalate", json={
        "ticket_id": c_id,
        "escalation_reason": "Direct public ombudsman intervention by ward sabha"
    })
    assert esc_res.status_code == 200
    assert esc_res.json()["jan_sunwai_status"] == "ESCALATED"
