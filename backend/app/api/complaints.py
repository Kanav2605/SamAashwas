from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional, Dict, Any
from ..models.schemas import ComplaintCreateRequest, ComplaintResponse
from ..db.database import db

router = APIRouter(prefix="/complaints", tags=["Citizen Complaints"])

@router.post("/submit", response_model=ComplaintResponse, summary="Submit a new citizen complaint")
async def submit_complaint(payload: ComplaintCreateRequest):
    """
    Ingests a grievance from WhatsApp, Mobile App, or Web Portal.
    Executes multilingual NLP classification, vision verification, and spatio-temporal deduplication.
    """
    try:
        complaint = db.submit_complaint(payload)
        return complaint.to_dict()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process complaint: {str(e)}")

@router.get("", response_model=List[Dict[str, Any]], summary="List recent citizen complaints")
async def list_complaints(limit: int = Query(50, ge=1, le=200)):
    """
    Retrieve recent citizen complaints including duplicate and non-duplicate submissions.
    """
    return db.get_all_complaints(limit=limit)

@router.get("/{complaint_id}", summary="Get complaint by ID")
async def get_complaint(complaint_id: str):
    complaint = db.complaints.get(complaint_id)
    if not complaint:
        raise HTTPException(status_code=404, detail="Complaint not found")
    return complaint.to_dict()
