from fastapi import APIRouter, Request, Form
from typing import Optional
from ..models.schemas import WhatsAppMessageRequest, WhatsAppMessageResponse, ComplaintCreateRequest, ChannelEnum
from ..db.database import db

router = APIRouter(prefix="/webhook/whatsapp", tags=["WhatsApp Bot Ingestion"])

@router.post("", response_model=WhatsAppMessageResponse, summary="Ingest WhatsApp grievance message")
async def handle_whatsapp_webhook(payload: WhatsAppMessageRequest):
    """
    Webhook handler for incoming WhatsApp bot messages.
    Supports location pins and photo attachments.
    """
    # Coordinates fallback if location pin wasn't sent
    lat = payload.Latitude if payload.Latitude is not None else 12.9716
    lon = payload.Longitude if payload.Longitude is not None else 77.6412

    # Clean phone number
    phone = payload.From.replace("whatsapp:", "").strip()

    complaint_req = ComplaintCreateRequest(
        raw_text=payload.Body,
        lat=lat,
        lon=lon,
        citizen_name="WhatsApp Citizen",
        citizen_phone=phone,
        channel=ChannelEnum.WHATSAPP,
        image_url=payload.MediaUrl
    )

    complaint = db.submit_complaint(complaint_req)

    # Construct citizen-friendly response
    if complaint.is_duplicate:
        reply = (
            f"Namaste! 🙏\n"
            f"Aapki complaint ({complaint.department}) receive ho gayi hai.\n"
            f"📌 Notice: Aapke ilaqe mein pehle se registered Master Ticket #{complaint.master_ticket_id} "
            f"ke saath aapki report (+1) merge kar di gayi hai taaki Ward Engineer ko turant action lene mein aasaani ho.\n"
            f"Status: In Queue (Priority Upvoted) 🚀"
        )
    else:
        reply = (
            f"Namaste! 🙏\n"
            f"Aapki nayi grievance register kar li gayi hai.\n"
            f"🎫 Complaint ID: {complaint.complaint_id}\n"
            f"🏛️ Department: {complaint.department}\n"
            f"📍 Location: {complaint.location_landmark} ({complaint.ward_extracted})\n"
            f"⚡ Urgency: {complaint.urgency}\n"
            f"Aapka ticket Ward Officer ko auto-assign ho gaya hai."
        )

    return WhatsAppMessageResponse(
        reply_message=reply,
        complaint_id=complaint.complaint_id,
        master_ticket_id=complaint.master_ticket_id,
        status="PROCESSED"
    )
