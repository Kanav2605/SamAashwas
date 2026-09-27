from fastapi import APIRouter, Request, Form
from typing import Optional
from ..models.schemas import WhatsAppMessageRequest, WhatsAppMessageResponse, ComplaintCreateRequest, ChannelEnum
from ..db.database import db

router = APIRouter(prefix="/webhook/whatsapp", tags=["WhatsApp Bot Ingestion"])

@router.post("", response_model=WhatsAppMessageResponse, summary="Ingest WhatsApp grievance message")
async def handle_whatsapp_webhook(payload: WhatsAppMessageRequest):
    """
    Webhook handler for incoming WhatsApp bot messages.
    Supports location pins, photo attachments, and multi-lingual Indian vernacular responses
    (Hindi, Hinglish, Kannada, Tamil, English).
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
    master_ticket = db.get_master_ticket_by_id(complaint.master_ticket_id)
    jan_status = master_ticket.jan_sunwai_status if master_ticket else "NORMAL"

    lang = payload.LanguagePref or complaint.language_detected

    if lang == "Kannada":
        if complaint.is_duplicate:
            reply = (
                f"ನಮಸ್ಕಾರ! 🙏\n"
                f"ನಿಮ್ಮ ದೂರು ({complaint.department}) ಸ್ವೀಕರಿಸಲಾಗಿದೆ.\n"
                f"📌 ಗಮನಿಸಿ: ನಿಮ್ಮ ವಾರ್ಡ್‌ನಲ್ಲಿ ಈಗಾಗಲೇ ನೋಂದಾಯಿಸಲಾದ ಮಾಸ್ಟರ್ ಟಿಕೆಟ್ #{complaint.master_ticket_id} "
                f"ಜೊತೆ ನಿಮ್ಮ ದೂರನ್ನು (+1) ವಿಲೀನಗೊಳಿಸಲಾಗಿದೆ.\n"
                f"ರಾಷ್ಟ್ರೀಯ ಮಿಷನ್: {complaint.national_mission}\n"
                f"ಕಾರ್ಪೊರೇಟರ್: {complaint.corporator_name}\n"
                f"ಸ್ಥಿತಿ: ಪರಿಶೀಲನೆಯಲ್ಲಿದೆ (Priority Upvoted) 🚀"
            )
        else:
            reply = (
                f"ನಮಸ್ಕಾರ! 🙏\n"
                f"ನಿಮ್ಮ ನಾಗರಿಕ ದೂರು ಯಶಸ್ವಿಯಾಗಿ ದಾಖಲಾಗಿದೆ.\n"
                f"🎫 ದೂರು ಸಂಖ್ಯೆ: {complaint.complaint_id}\n"
                f"🏛️ ಇಲಾಖೆ: {complaint.department}\n"
                f"📍 ಸ್ಥಳ: {complaint.location_landmark} ({complaint.ward_extracted})\n"
                f"⚡ ತುರ್ತುಸ್ಥಿತಿ: {complaint.urgency}\n"
                f"⏱️ ಸಿಟಿಜನ್ ಚಾರ್ಟರ್ SLA: {complaint.citizen_charter_sla_hours} ಗಂಟೆಗಳು\n"
                f"ರಾಷ್ಟ್ರೀಯ ಯೋಜನೆ: {complaint.national_mission}\n"
                f"ಜನಸ್ಪಂದನ / ಜನ ಸುನ್ವಾಯಿ ಸ್ಥಿತಿ: {jan_status}\n"
                f"ವಾರ್ಡ್ ಇಂಜಿನಿಯರ್‌ಗೆ ಸ್ವಯಂಚಾಲಿತವಾಗಿ ನಿಯೋಜಿಸಲಾಗಿದೆ."
            )
    elif lang == "Tamil":
        if complaint.is_duplicate:
            reply = (
                f"வணக்கம்! 🙏\n"
                f"உங்கள் புகார் ({complaint.department}) பெறப்பட்டது.\n"
                f"📌 அறிவிப்பு: உங்கள் வார்டில் ஏற்கனவே உள்ள மாஸ்டர் டிக்கெட் #{complaint.master_ticket_id} "
                f"உடன் உங்கள் புகார் (+1) இணைக்கப்பட்டுள்ளது.\n"
                f"திட்டம்: {complaint.national_mission}\n"
                f"கவுன்சிலர்: {complaint.corporator_name}\n"
                f"நிலை: பரிசீலனையில் உள்ளது 🚀"
            )
        else:
            reply = (
                f"வணக்கம்! 🙏\n"
                f"உங்கள் புகார் வெற்றிகரமாக பதிவு செய்யப்பட்டது.\n"
                f"🎫 புகார் எண்: {complaint.complaint_id}\n"
                f"🏛️ துறை: {complaint.department}\n"
                f"📍 இடம்: {complaint.location_landmark} ({complaint.ward_extracted})\n"
                f"⚡ அவசரம்: {complaint.urgency}\n"
                f"⏱️ குடிமக்கள் சாசனம் SLA: {complaint.citizen_charter_sla_hours} மணி நேரம்\n"
                f"தேசிய திட்டம்: {complaint.national_mission}\n"
                f"வார்டு பொறியாளருக்கு உடனடியாக ஒதுக்கப்பட்டுள்ளது."
            )
    elif lang == "Hindi (Devanagari)":
        if complaint.is_duplicate:
            reply = (
                f"नमस्ते! 🙏\n"
                f"आपकी शिकायत ({complaint.department}) दर्ज हो गई है।\n"
                f"📌 सूचना: आपके वार्ड में पहले से दर्ज मास्टर टिकट #{complaint.master_ticket_id} "
                f"के साथ आपकी रिपोर्ट (+1) जोड़ दी गई है ताकी वार्ड इंजीनियर तुरंत कार्रवाई कर सके।\n"
                f"🇮🇳 राष्ट्रीय मिशन: {complaint.national_mission}\n"
                f"🏛️ पार्षद: {complaint.corporator_name}\n"
                f"स्थिति: कतार में प्राथमिकता बढ़ाई गई (Priority Upvoted) 🚀"
            )
        else:
            reply = (
                f"नमस्ते! 🙏\n"
                f"आपकी नई नागरिक शिकायत सफलतापूर्वक दर्ज हो गई है।\n"
                f"🎫 शिकायत आईडी: {complaint.complaint_id}\n"
                f"🏛️ विभाग: {complaint.department} ({complaint.issue_type})\n"
                f"📍 स्थान: {complaint.location_landmark} ({complaint.ward_extracted})\n"
                f"⚡ तात्कालिकता: {complaint.urgency}\n"
                f"⏱️ सिटिज़न चार्टर SLA: {complaint.citizen_charter_sla_hours} घंटे\n"
                f"🇮🇳 राष्ट्रीय मिशन: {complaint.national_mission}\n"
                f"🏛️ पार्षद: {complaint.corporator_name} | विधायक: {complaint.mla_name}\n"
                f"📋 जन सुनवाई स्थिति: {jan_status}\n"
                f"वार्ड कनिष्ठ अभियंता को तत्काल समाधान हेतु प्रेषित कर दिया गया है।"
            )
    else: # Hinglish / English default
        if complaint.is_duplicate:
            reply = (
                f"Namaste! 🙏\n"
                f"Aapki complaint ({complaint.department}) receive ho gayi hai.\n"
                f"📌 Notice: Aapke ilaqe mein pehle se registered Master Ticket #{complaint.master_ticket_id} "
                f"ke saath aapki report (+1) merge kar di gayi hai taaki Ward Engineer ko turant action lene mein aasaani ho.\n"
                f"🇮🇳 Mission: {complaint.national_mission}\n"
                f"🏛️ Ward Corporator: {complaint.corporator_name}\n"
                f"Status: In Queue (Priority Upvoted) 🚀"
            )
        else:
            reply = (
                f"Namaste! 🙏\n"
                f"Aapki nayi grievance register kar li gayi hai.\n"
                f"🎫 Complaint ID: {complaint.complaint_id}\n"
                f"🏛️ Department: {complaint.department} ({complaint.issue_type})\n"
                f"📍 Location: {complaint.location_landmark} ({complaint.ward_extracted})\n"
                f"⚡ Urgency: {complaint.urgency}\n"
                f"⏱️ Citizen Charter SLA: {complaint.citizen_charter_sla_hours} Hours\n"
                f"🇮🇳 National Mission: {complaint.national_mission}\n"
                f"🏛️ Corporator: {complaint.corporator_name} | MLA: {complaint.mla_name}\n"
                f"📋 Jan Sunwai Docket: {jan_status}\n"
                f"Aapka ticket Ward Officer ko auto-assign ho gaya hai."
            )

    return WhatsAppMessageResponse(
        reply_message=reply,
        complaint_id=complaint.complaint_id,
        master_ticket_id=complaint.master_ticket_id,
        status="PROCESSED",
        national_mission=complaint.national_mission,
        jan_sunwai_status=jan_status
    )
