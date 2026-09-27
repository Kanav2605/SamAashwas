from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional, Dict, Any
from ..models.schemas import MasterTicketResponse, MasterTicketUpdateRequest, TicketStatusEnum
from ..db.database import db

router = APIRouter(prefix="/master-tickets", tags=["ULB Officer Master Incidents"])

@router.get("", response_model=List[Dict[str, Any]], summary="List clustered master tickets")
async def list_master_tickets(status: Optional[str] = Query(None, description="Filter by status (OPEN, IN_PROGRESS, RESOLVED)")):
    """
    Retrieve auto-assigned Master Incidents with aggregated citizen report counts and SLA timers.
    """
    return db.get_master_tickets(status=status)

@router.get("/{ticket_id}", summary="Get master ticket details and citizen report trail")
async def get_master_ticket(ticket_id: str):
    ticket = db.get_master_ticket_by_id(ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Master ticket not found")
    return ticket.to_dict()

@router.patch("/{ticket_id}", summary="Update master ticket status or assigned officer")
async def update_master_ticket(ticket_id: str, update: MasterTicketUpdateRequest):
    ticket = db.update_master_ticket(ticket_id, update)
    if not ticket:
        raise HTTPException(status_code=404, detail="Master ticket not found")
    return ticket.to_dict()
