from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional, Dict, Any
from ..models.schemas import MasterTicketResponse, MasterTicketUpdateRequest, TicketStatusEnum
from ..db.database import db

router = APIRouter(prefix="/master-tickets", tags=["ULB Officer Master Incidents"])

@router.get("", response_model=List[Dict[str, Any]], summary="List clustered master tickets")
async def list_master_tickets(
    status: Optional[str] = Query(None, description="Filter by status (OPEN, IN_PROGRESS, RESOLVED)"),
    jan_sunwai_only: bool = Query(False, description="Filter tickets escalated to Jan Sunwai / Public Grievance Day"),
    mission: Optional[str] = Query(None, description="Filter by National Civic Mission (Swachh Bharat, AMRUT, etc.)"),
    city: Optional[str] = Query(None, description="Filter by Indian City / Municipal Corporation (Bengaluru, Mumbai, Delhi, etc.)")
):
    """
    Retrieve auto-assigned Master Incidents with aggregated citizen report counts, SLA timers,
    Corporator/MLA linkages, and Jan Sunwai escalation flags.
    """
    return db.get_master_tickets(status=status, jan_sunwai_only=jan_sunwai_only, mission=mission, city=city)

@router.get("/{ticket_id}", summary="Get master ticket details and citizen report trail")
async def get_master_ticket(ticket_id: str):
    ticket = db.get_master_ticket_by_id(ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Master ticket not found")
    return ticket.to_dict()

@router.patch("/{ticket_id}", summary="Update master ticket status, SLA or Jan Sunwai docket")
async def update_master_ticket(ticket_id: str, update: MasterTicketUpdateRequest):
    ticket = db.update_master_ticket(ticket_id, update)
    if not ticket:
        raise HTTPException(status_code=404, detail="Master ticket not found")
    return ticket.to_dict()

@router.post("/{ticket_id}/escalate-jan-sunwai", summary="Escalate incident to Jan Sunwai / Public Grievance Day")
async def escalate_ticket_jan_sunwai(ticket_id: str):
    """
    Docket this master incident for Friday's Jan Sunwai / District Samadhan Diwas hearing.
    """
    ticket = db.get_master_ticket_by_id(ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Master ticket not found")
    ticket.jan_sunwai_status = "ESCALATED"
    return {
        "master_ticket_id": ticket_id,
        "jan_sunwai_status": ticket.jan_sunwai_status,
        "message": f"Ticket {ticket_id} has been docketed for the upcoming Jan Sunwai / Public Grievance Day hearing before the Municipal Commissioner."
    }

@router.post("/{ticket_id}/endorse", summary="Citizen endorsement (+1 Me too) for duplicate deflection")
async def endorse_master_ticket(
    ticket_id: str,
    payload: Optional[Dict[str, Any]] = None
):
    """
    Register an active citizen endorsement (+1 Me too) on an existing master incident.
    Deflects redundant ticket creation while boosting incident priority and citizen karma.
    """
    citizen_name = (payload or {}).get("citizen_name", "Citizen")
    citizen_phone = (payload or {}).get("citizen_phone", "9876543210")
    ticket = db.endorse_master_ticket(ticket_id, citizen_name=citizen_name, citizen_phone=citizen_phone)
    if not ticket:
        raise HTTPException(status_code=404, detail="Master ticket not found")
    return {
        "status": "success",
        "master_ticket_id": ticket_id,
        "report_count": ticket.report_count,
        "message": f"Endorsement recorded! Master Incident {ticket_id} now has {ticket.report_count} citizen endorsements.",
        "karma_points_awarded": 50
    }

