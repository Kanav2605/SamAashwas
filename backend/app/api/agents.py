import logging
from typing import List, Dict, Any, Optional
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field

from ..agents.orchestrator import agent_orchestrator
from ..db.database import db
from ..models.schemas import (
    ComplaintCreateRequest,
    OrchestrationResponse,
    AgentStatusInfo,
    TrackingLookupResponse
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="", tags=["Multi-Agent Civic Orchestration"])

class SimulateScenarioRequest(BaseModel):
    scenario: str = Field("waterlogging_monsoon", description="Scenario type: waterlogging_monsoon, sparking_transformer, spam_selfie_meme, pothole_cluster, sewage_leak")

class OmbudsmanEscalateRequest(BaseModel):
    ticket_id: str = Field(..., description="Master Ticket ID or Complaint ID to escalate to Friday Jan Sunwai")
    escalation_reason: Optional[str] = Field("Ombudsman expedited escalation for Public Grievance Hearing", description="Reason for escalation")

@router.get("/agents/status", response_model=List[AgentStatusInfo], summary="Get status of all 6 civic agents")
async def get_agents_status():
    """
    Returns the real-time operational status, roles, and descriptions of the 6 autonomous civic agents.
    """
    manifest = agent_orchestrator.get_agent_manifest()
    return manifest

@router.post("/agents/orchestrate", response_model=OrchestrationResponse, summary="Run multi-agent deliberation for a grievance")
async def orchestrate_grievance(payload: ComplaintCreateRequest):
    """
    Executes the 6-agent orchestration pipeline transparently and returns the deliberation trace.
    """
    active_masters = [m for m in db.master_tickets.values() if m.status != "RESOLVED"]
    res = agent_orchestrator.orchestrate_complaint(
        raw_text=payload.raw_text,
        lat=payload.lat,
        lon=payload.lon,
        channel=payload.channel.value if hasattr(payload.channel, "value") else str(payload.channel),
        citizen_name=payload.citizen_name or "Citizen",
        citizen_phone=payload.citizen_phone or "9876543210",
        image_url=payload.image_url,
        image_category_hint=payload.image_category_hint,
        audio_transcript=payload.audio_transcript,
        wards=db.wards,
        active_masters=active_masters,
        assets=db.assets
    )
    return res

@router.post("/agents/simulate", response_model=OrchestrationResponse, summary="Simulate multi-agent scenario")
async def simulate_scenario(payload: SimulateScenarioRequest):
    """
    Simulate a realistic municipal crisis or grievance to demonstrate multi-agent deliberation.
    """
    scenarios = {
        "waterlogging_monsoon": {
            "raw_text": "Minto Bridge underpass completely flooded after heavy rain, 3 cars submerged and drainage choked",
            "lat": 28.6410,
            "lon": 77.2250,
            "image_category_hint": "waterlogging",
            "citizen_name": "Ramesh Gupta",
            "citizen_phone": "9811099881",
            "channel": "web_portal"
        },
        "sparking_transformer": {
            "raw_text": "Dangerous sparking from main distribution transformer near Karol Bagh market, fire risk urgent",
            "lat": 28.6520,
            "lon": 77.1915,
            "image_category_hint": "broken_streetlight",
            "citizen_name": "Anita Verma",
            "citizen_phone": "9811099882",
            "channel": "whatsapp"
        },
        "spam_selfie_meme": {
            "raw_text": "Gutter saaf nahi hua",
            "lat": 28.6814,
            "lon": 77.2228,
            "image_category_hint": "unrelated_or_spam",
            "citizen_name": "Troll User",
            "citizen_phone": "9811099883",
            "channel": "web_portal"
        },
        "pothole_cluster": {
            "raw_text": "Massive deep pothole on Rohini Sector 15 main road, two-wheelers skidding frequently",
            "lat": 28.7180,
            "lon": 77.1190,
            "image_category_hint": "pothole",
            "citizen_name": "Devinder Singh",
            "citizen_phone": "9811099884",
            "channel": "mobile_app"
        },
        "sewage_leak": {
            "raw_text": "Main sewer pipeline burst in Laxmi Nagar, black foul-smelling sewage entering residential lanes",
            "lat": 28.6300,
            "lon": 77.2770,
            "image_category_hint": "sewage_overflow",
            "citizen_name": "Pooja Sharma",
            "citizen_phone": "9811099885",
            "channel": "whatsapp"
        }
    }

    scen = scenarios.get(payload.scenario, scenarios["waterlogging_monsoon"])
    req = ComplaintCreateRequest(**scen)
    active_masters = [m for m in db.master_tickets.values() if m.status != "RESOLVED"]

    if payload.scenario == "pothole_cluster":
        has_cluster_master = any("Rohini" in (getattr(m, "ward_name", "") or "") and getattr(m, "department", "") == "Roads & Traffic Infrastructure" for m in active_masters)
        if not has_cluster_master:
            from ..models.domain import MasterTicketRecord
            mock_master = MasterTicketRecord(
                master_ticket_id="MST-ROH-0881",
                department="Roads & Traffic Infrastructure",
                title="Pothole / Road Cave-in near Rohini Sector 15",
                issue_type="Pothole / Road Cave-in",
                ward_id="MCD-ROH-54",
                ward_name="Rohini Sector 15 - Prashant Vihar",
                mcd_zone="Rohini",
                lat=28.7181,
                lon=77.1191,
                urgency="High",
                status="OPEN",
                report_count=2,
                national_mission="State PWD & Municipal Road Safety Program",
                assigned_engineer="Rohini Assistant Engineer (Roads Division)"
            )
            active_masters = [mock_master] + active_masters

    res = agent_orchestrator.orchestrate_complaint(
        raw_text=req.raw_text,
        lat=req.lat,
        lon=req.lon,
        channel=req.channel.value if hasattr(req.channel, "value") else str(req.channel),
        citizen_name=req.citizen_name or "Citizen",
        citizen_phone=req.citizen_phone or "9876543210",
        image_url=req.image_url,
        image_category_hint=req.image_category_hint,
        audio_transcript=req.audio_transcript,
        wards=db.wards,
        active_masters=active_masters,
        assets=db.assets
    )
    return res

@router.post("/agents/ombudsman/escalate", summary="Docket ticket to Friday Jan Sunwai")
async def ombudsman_escalate(payload: OmbudsmanEscalateRequest):
    """
    Civic Ombudsman endpoint to directly escalate an incident to Friday Jan Sunwai hearing.
    """
    ticket = db.get_master_ticket_by_id(payload.ticket_id)
    if not ticket:
        # Check if complaint_id was given
        comp = db.complaints.get(payload.ticket_id)
        if comp and comp.master_ticket_id:
            ticket = db.get_master_ticket_by_id(comp.master_ticket_id)

    if not ticket:
        raise HTTPException(status_code=404, detail="Incident or complaint ticket not found")

    ticket.jan_sunwai_status = "ESCALATED"
    return {
        "status": "SUCCESS",
        "ticket_id": ticket.master_ticket_id,
        "jan_sunwai_status": ticket.jan_sunwai_status,
        "hearing_schedule": "Upcoming Friday 11:00 AM @ Zonal Deputy Commissioner Office",
        "ombudsman_notes": payload.escalation_reason
    }

@router.get("/tracking/{tracking_id}", response_model=TrackingLookupResponse, summary="Track grievance status by Complaint ID or Master Ticket ID")
async def track_grievance(tracking_id: str):
    """
    Instant grievance tracking for citizens with transparent multi-agent deliberation log.
    """
    result = db.track_by_id(tracking_id)
    if not result:
        raise HTTPException(status_code=404, detail=f"Tracking ID '{tracking_id}' not found in municipal records")
    return result
