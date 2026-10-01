from fastapi import APIRouter, HTTPException, Query, Header
from typing import List, Optional, Dict, Any
from ..models.schemas import ComplaintCreateRequest, ComplaintResponse, VoiceNoteComplaintRequest, ChannelEnum
from ..db.database import db
from .auth import get_current_user_from_token

router = APIRouter(prefix="/complaints", tags=["Citizen Complaints"])

@router.post("/submit", response_model=ComplaintResponse, summary="Submit a new citizen complaint")
async def submit_complaint(payload: ComplaintCreateRequest, authorization: Optional[str] = Header(None)):
    """
    Ingests a grievance from WhatsApp, Mobile App, or Web Portal.
    Associates authenticated citizen profile if Authorization header is provided.
    Executes multilingual NLP classification, vision verification, and spatio-temporal deduplication.
    """
    try:
        user = get_current_user_from_token(authorization)
        if user:
            if not payload.citizen_name or payload.citizen_name == "Citizen":
                payload.citizen_name = user["name"]
            if not payload.citizen_phone or payload.citizen_phone == "9876543210":
                payload.citizen_phone = user["phone"]

        complaint = db.submit_complaint(payload)
        return complaint.to_dict()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process complaint: {str(e)}")

@router.post("/voice-note", response_model=ComplaintResponse, summary="Submit vernacular voice grievance")
async def submit_voice_grievance(payload: VoiceNoteComplaintRequest, authorization: Optional[str] = Header(None)):
    """
    Ingests speech-to-text transcribed voice note in Hindi, Kannada, Tamil, Hinglish, or English.
    Tags as ChannelEnum.VOICE_NOTE and passes through AI deduplication and routing pipeline.
    """
    try:
        user = get_current_user_from_token(authorization)
        c_name = payload.citizen_name
        c_phone = payload.citizen_phone
        if user:
            c_name = c_name if (c_name and c_name != "Citizen") else user["name"]
            c_phone = c_phone if (c_phone and c_phone != "9876543210") else user["phone"]

        complaint_req = ComplaintCreateRequest(
            raw_text=payload.audio_transcript,
            lat=payload.lat,
            lon=payload.lon,
            citizen_name=c_name or "Voice Citizen",
            citizen_phone=c_phone or "9876543210",
            channel=ChannelEnum.VOICE_NOTE,
            audio_transcript=f"[{payload.spoken_language}] {payload.audio_transcript}"
        )
        complaint = db.submit_complaint(complaint_req)
        return complaint.to_dict()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process voice grievance: {str(e)}")

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
