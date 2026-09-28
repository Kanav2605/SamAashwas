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

def test_geo_dedup_agent_unit_with_proxy_complaint():
    agent = GeoDeduplicationAgent()
    from backend.app.models.domain import MasterTicketRecord
    master = MasterTicketRecord(
        master_ticket_id="MST-KB-0099",
        department="Water Supply & Sewage",
        title="Sewer overflow near Pusa Road",
        issue_type="Sewer Line Overflow",
        ward_id="MCD-KB-83",
        ward_name="Karol Bagh - Rajendra Nagar",
        lat=28.6514,
        lon=77.1907,
        report_count=1
    )
    context = {
        "department": "Water Supply & Sewage",
        "raw_text": "Gutter overflow and dirty water near Pusa road Karol Bagh",
        "lat": 28.6515,
        "lon": 77.1908,
        "active_masters": [master]
    }
    result = agent.run(context)
    assert result.status == "MERGED"
    assert result.outputs["is_duplicate"] is True
    assert result.outputs["master_ticket_id"] == "MST-KB-0099"
    assert context["report_count"] == 2

def test_duplicate_clustering_and_community_density_ombudsman_escalation():
    # 1. First complaint -> Creates new master ticket
    res1 = client.post("/api/v1/complaints/submit", json={
        "raw_text": "Dangerous deep pothole on Karol Bagh Pusa Road, two wheelers skidding",
        "lat": 28.6514,
        "lon": 77.1907,
        "citizen_name": "Citizen One",
        "citizen_phone": "9811000001",
        "channel": "web_portal"
    })
    assert res1.status_code == 200
    data1 = res1.json()
    master_id = data1["master_ticket_id"]
    assert data1["is_duplicate"] is False

    # 2. Second complaint -> Within 20m, clustered into existing master ticket
    res2 = client.post("/api/v1/complaints/submit", json={
        "raw_text": "Bada gaddha road pe Pusa road Karol Bagh bikes slipping",
        "lat": 28.6515,
        "lon": 77.1908,
        "citizen_name": "Citizen Two",
        "citizen_phone": "9811000002",
        "channel": "whatsapp"
    })
    assert res2.status_code == 200
    data2 = res2.json()
    assert data2["is_duplicate"] is True
    assert data2["master_ticket_id"] == master_id

    # Verify Agent 4 (Geo-Dedup) trace correctly recorded MERGED
    dedup_step = [s for s in data2["agent_trace"] if s["agent_name"] == "Geo-Deduplication & Clustering Agent"][0]
    assert dedup_step["status"] == "MERGED"
    assert dedup_step["outputs"]["is_duplicate"] is True

    # 3. Third complaint -> Reaches community grievance density of 3 reports
    res3 = client.post("/api/v1/complaints/submit", json={
        "raw_text": "Huge crater pothole please repair Pusa Road Karol bagh",
        "lat": 28.6514,
        "lon": 77.1907,
        "citizen_name": "Citizen Three",
        "citizen_phone": "9811000003",
        "channel": "mobile_app"
    })
    assert res3.status_code == 200
    data3 = res3.json()
    assert data3["is_duplicate"] is True
    assert data3["master_ticket_id"] == master_id

    # Verify Agent 6 (Ombudsman) auto-docketed to Friday Jan Sunwai
    ombudsman_step = [s for s in data3["agent_trace"] if s["agent_name"] == "Civic Ombudsman & Jan Sunwai Escalation Agent"][0]
    assert ombudsman_step["status"] == "ESCALATED"
    assert ombudsman_step["outputs"]["jan_sunwai_status"] == "ESCALATED"

    # Master ticket in database should now be ESCALATED
    master = db.get_master_ticket_by_id(master_id)
    assert master.jan_sunwai_status == "ESCALATED"
    assert master.report_count >= 3

def test_simulate_pothole_cluster_demonstrates_dedup_and_escalation():
    res = client.post("/api/v1/agents/simulate", json={"scenario": "pothole_cluster"})
    assert res.status_code == 200
    data = res.json()
    assert data["orchestration_status"] == "COMPLETED"
    
    dedup_step = [s for s in data["agent_trace"] if s["agent_name"] == "Geo-Deduplication & Clustering Agent"][0]
    assert dedup_step["status"] == "MERGED"
    assert dedup_step["outputs"]["is_duplicate"] is True

    ombudsman_step = [s for s in data["agent_trace"] if s["agent_name"] == "Civic Ombudsman & Jan Sunwai Escalation Agent"][0]
    assert ombudsman_step["status"] == "ESCALATED"
