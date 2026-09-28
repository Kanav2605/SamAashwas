from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

class ChannelEnum(str, Enum):
    WHATSAPP = "whatsapp"
    WEB_PORTAL = "web_portal"
    MOBILE_APP = "mobile_app"
    HELPLINE = "helpline"
    VOICE_NOTE = "voice_note"

class TicketStatusEnum(str, Enum):
    OPEN = "OPEN"
    IN_PROGRESS = "IN_PROGRESS"
    RESOLVED = "RESOLVED"
    REJECTED = "REJECTED"

class UrgencyEnum(str, Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    CRITICAL = "Critical"

class VisionVerificationResult(BaseModel):
    is_authentic: bool
    detected_class: str
    confidence: float
    mismatch_detected: bool
    status_label: str # "Auto-Verified" or "Possible Spam / Flagged"
    explanation: str

class ComplaintCreateRequest(BaseModel):
    raw_text: str = Field(..., description="Complaint description in Hinglish, Hindi, Kannada, Tamil, or English")
    lat: float = Field(..., description="Latitude coordinate of grievance")
    lon: float = Field(..., description="Longitude coordinate of grievance")
    ward_hint: Optional[str] = Field(None, description="Optional user-provided ward name/id")
    citizen_name: Optional[str] = Field("Citizen", description="Citizen name")
    citizen_phone: Optional[str] = Field("9876543210", description="Citizen phone or WhatsApp number")
    channel: ChannelEnum = Field(ChannelEnum.WEB_PORTAL, description="Reporting channel")
    image_url: Optional[str] = Field(None, description="Image URL or base64 data")
    image_category_hint: Optional[str] = Field(None, description="Vision verification hint")
    audio_transcript: Optional[str] = Field(None, description="Voice note speech-to-text transcript")
    mcd_zone: Optional[str] = Field(None, description="MCD Administrative Zone")

class VoiceNoteComplaintRequest(BaseModel):
    spoken_language: str = Field("hi-IN", description="Language code: hi-IN, kn-IN, ta-IN, en-IN, or hinglish")
    audio_transcript: str = Field(..., description="Transcribed vernacular voice grievance text")
    lat: float = Field(..., description="Latitude coordinate")
    lon: float = Field(..., description="Longitude coordinate")
    citizen_name: Optional[str] = Field("Citizen", description="Citizen name")
    citizen_phone: Optional[str] = Field("9876543210", description="Citizen phone")
    mcd_zone: Optional[str] = Field(None, description="MCD Zone")

class ExtractedNLPData(BaseModel):
    department: str
    issue_type: str
    urgency: UrgencyEnum
    location_landmark: str
    ward_extracted: str
    language_detected: str
    confidence: float
    national_mission: Optional[str] = None
    citizen_charter_sla_hours: Optional[int] = None

class ComplaintResponse(BaseModel):
    complaint_id: str
    raw_text: str
    department: str
    issue_type: str
    urgency: str
    location_landmark: str
    ward_extracted: str
    language_detected: str
    lat: float
    lon: float
    channel: str
    citizen_name: str
    citizen_phone: str
    image_verification: Optional[VisionVerificationResult]
    master_ticket_id: str
    is_duplicate: bool
    created_at: str
    national_mission: Optional[str] = None
    citizen_charter_sla_hours: Optional[int] = None
    jan_sunwai_eligible: Optional[bool] = None
    corporator_name: Optional[str] = None
    mla_name: Optional[str] = None
    audio_transcript: Optional[str] = None
    mcd_zone: Optional[str] = None
    agent_trace: Optional[List[Dict[str, Any]]] = None

class MasterTicketResponse(BaseModel):
    master_ticket_id: str
    department: str
    title: str
    issue_type: str
    ward_id: str
    ward_name: str
    lat: float
    lon: float
    urgency: str
    status: TicketStatusEnum
    report_count: int
    citizen_reports: List[Dict[str, Any]]
    first_reported_at: str
    last_reported_at: str
    sla_hours_remaining: int
    is_sla_breached: Optional[bool] = False
    assigned_engineer: str
    national_mission: Optional[str] = None
    citizen_charter_sla_hours: Optional[int] = None
    jan_sunwai_status: Optional[str] = None
    corporator: Optional[Dict[str, str]] = None
    mla: Optional[Dict[str, str]] = None
    ward_sabha_schedule: Optional[str] = None
    desilting_readiness_pct: Optional[int] = None
    mcd_zone: Optional[str] = None
    agent_trace: Optional[List[Dict[str, Any]]] = None

class MasterTicketUpdateRequest(BaseModel):
    status: Optional[TicketStatusEnum] = None
    urgency: Optional[UrgencyEnum] = None
    assigned_engineer: Optional[str] = None
    resolution_notes: Optional[str] = None
    jan_sunwai_status: Optional[str] = None

class WardRiskResponse(BaseModel):
    ward_id: str
    ward_name: str
    center_lat: float
    center_lon: float
    risk_score: float # 0 - 100
    risk_level: str   # LOW, MEDIUM, HIGH, CRITICAL
    primary_risk_factor: str
    rainfall_forecast_24h_mm: float
    rainfall_forecast_48h_mm: float
    active_complaints_count: int
    drainage_vulnerability_score: float
    recommendation: str
    desilting_readiness_pct: Optional[int] = 75
    corporator: Optional[Dict[str, str]] = None
    ward_sabha_schedule: Optional[str] = None

class PredictiveAssetResponse(BaseModel):
    asset_id: str
    type: str
    ward_id: str
    lat: float
    lon: float
    structural_health_score: float
    failure_probability: float
    vulnerability_flag: str
    recommended_action: str

class AnalyticsStatsResponse(BaseModel):
    total_complaints: int
    total_master_tickets: int
    total_duplicates_filtered: int
    deduplication_rate_pct: float
    department_breakdown: Dict[str, int]
    ward_breakdown: Dict[str, int]
    urgency_breakdown: Dict[str, int]
    high_risk_wards_count: int
    national_mission_breakdown: Optional[Dict[str, int]] = None
    jan_sunwai_escalated_count: Optional[int] = 0
    language_breakdown: Optional[Dict[str, int]] = None

class WhatsAppMessageRequest(BaseModel):
    From: str = Field(..., description="WhatsApp user phone number e.g. whatsapp:+919876543210")
    Body: str = Field(..., description="Message text or transcription")
    Latitude: Optional[float] = Field(None, description="User shared location latitude")
    Longitude: Optional[float] = Field(None, description="User shared location longitude")
    MediaUrl: Optional[str] = Field(None, description="Uploaded photo link")
    LanguagePref: Optional[str] = Field(None, description="Preferred language code (en, hi, kn, ta)")

class WhatsAppMessageResponse(BaseModel):
    reply_message: str
    complaint_id: Optional[str] = None
    master_ticket_id: Optional[str] = None
    status: str
    national_mission: Optional[str] = None
    jan_sunwai_status: Optional[str] = None

class AgentStepResultSchema(BaseModel):
    agent_name: str
    status: str
    confidence: float
    thought_log: str
    action_taken: str
    outputs: Dict[str, Any]
    timestamp: str

class OrchestrationResponse(BaseModel):
    orchestration_status: str
    narrative_summary: str
    complaint_id: Optional[str] = None
    master_ticket_id: Optional[str] = None
    department: Optional[str] = None
    issue_type: Optional[str] = None
    urgency: Optional[str] = None
    location_landmark: Optional[str] = None
    mcd_zone: Optional[str] = None
    ward_name: Optional[str] = None
    assigned_engineer: Optional[str] = None
    sla_hours: Optional[int] = None
    is_duplicate: bool = False
    jan_sunwai_status: Optional[str] = None
    agent_trace: List[Dict[str, Any]]

class AgentStatusInfo(BaseModel):
    id: str
    name: str
    role: str
    description: str
    status: str
    framework: str

class TrackingLookupResponse(BaseModel):
    tracking_id: str
    type: str # "complaint" or "master_ticket"
    title: str
    department: str
    urgency: str
    status: str
    ward_name: str
    mcd_zone: Optional[str] = None
    sla_hours_remaining: int
    is_sla_breached: bool = False
    assigned_engineer: str
    jan_sunwai_status: str
    created_at: str
    report_count: int = 1
    national_mission: Optional[str] = None
    corporator: Optional[Dict[str, str]] = None
    agent_trace: Optional[List[Dict[str, Any]]] = None

