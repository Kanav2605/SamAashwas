from typing import List, Optional, Dict, Any
from datetime import datetime, timezone
import uuid

class ComplaintRecord:
    def __init__(
        self,
        raw_text: str,
        department: str,
        issue_type: str,
        urgency: str,
        location_landmark: str,
        ward_extracted: str,
        language_detected: str,
        lat: float,
        lon: float,
        channel: str = "web_portal",
        citizen_name: str = "Citizen",
        citizen_phone: str = "9876543210",
        image_verification: Optional[Dict[str, Any]] = None,
        master_ticket_id: Optional[str] = None,
        is_duplicate: bool = False,
        complaint_id: Optional[str] = None,
        created_at: Optional[str] = None,
        national_mission: Optional[str] = None,
        citizen_charter_sla_hours: Optional[int] = None,
        jan_sunwai_eligible: bool = False,
        corporator_name: Optional[str] = None,
        mla_name: Optional[str] = None,
        audio_transcript: Optional[str] = None,
        mcd_zone: Optional[str] = None,
        city: Optional[str] = None,
        corporation: Optional[str] = None,
        zone: Optional[str] = None,
        agent_trace: Optional[List[Dict[str, Any]]] = None
    ):
        self.complaint_id = complaint_id or f"CMP-{uuid.uuid4().hex[:8].upper()}"
        self.raw_text = raw_text
        self.department = department
        self.issue_type = issue_type
        self.urgency = urgency
        self.location_landmark = location_landmark
        self.ward_extracted = ward_extracted
        self.language_detected = language_detected
        self.lat = lat
        self.lon = lon
        self.channel = channel
        self.citizen_name = citizen_name
        self.citizen_phone = citizen_phone
        self.image_verification = image_verification
        self.master_ticket_id = master_ticket_id or ""
        self.is_duplicate = is_duplicate
        self.created_at = created_at or datetime.now(timezone.utc).isoformat()
        self.national_mission = national_mission or "Swachh Bharat / AMRUT Urban Mission"
        self.citizen_charter_sla_hours = citizen_charter_sla_hours or (24 if urgency in ["High", "Critical"] else 48)
        self.jan_sunwai_eligible = jan_sunwai_eligible or (urgency in ["High", "Critical"])
        self.corporator_name = corporator_name or "Ward Councillor"
        self.mla_name = mla_name or "Constituency MLA"
        self.audio_transcript = audio_transcript
        self.mcd_zone = mcd_zone or "Central Zone"
        self.city = city or "Pan-India"
        self.corporation = corporation or "Municipal Corporation"
        self.zone = zone or self.mcd_zone
        self.agent_trace = agent_trace or []

    def to_dict(self) -> Dict[str, Any]:
        return {
            "complaint_id": self.complaint_id,
            "raw_text": self.raw_text,
            "department": self.department,
            "issue_type": self.issue_type,
            "urgency": self.urgency,
            "location_landmark": self.location_landmark,
            "ward_extracted": self.ward_extracted,
            "language_detected": self.language_detected,
            "lat": self.lat,
            "lon": self.lon,
            "channel": self.channel,
            "citizen_name": self.citizen_name,
            "citizen_phone": self.citizen_phone,
            "image_verification": self.image_verification,
            "master_ticket_id": self.master_ticket_id,
            "is_duplicate": self.is_duplicate,
            "created_at": self.created_at,
            "national_mission": self.national_mission,
            "citizen_charter_sla_hours": self.citizen_charter_sla_hours,
            "jan_sunwai_eligible": self.jan_sunwai_eligible,
            "corporator_name": self.corporator_name,
            "mla_name": self.mla_name,
            "audio_transcript": self.audio_transcript,
            "mcd_zone": self.mcd_zone,
            "city": self.city,
            "corporation": self.corporation,
            "zone": self.zone,
            "agent_trace": self.agent_trace
        }


class MasterTicketRecord:
    def __init__(
        self,
        department: str,
        title: str,
        issue_type: str,
        ward_id: str,
        ward_name: str,
        lat: float,
        lon: float,
        urgency: str = "Medium",
        status: str = "OPEN",
        assigned_engineer: str = "Ward Junior Engineer (AE-01)",
        master_ticket_id: Optional[str] = None,
        first_reported_at: Optional[str] = None,
        national_mission: Optional[str] = None,
        citizen_charter_sla_hours: Optional[int] = None,
        jan_sunwai_status: str = "NONE",
        corporator: Optional[Dict[str, str]] = None,
        mla: Optional[Dict[str, str]] = None,
        ward_sabha_schedule: Optional[str] = None,
        desilting_readiness_pct: Optional[int] = None,
        mcd_zone: Optional[str] = None,
        city: Optional[str] = None,
        corporation: Optional[str] = None,
        zone: Optional[str] = None,
        agent_trace: Optional[List[Dict[str, Any]]] = None,
        report_count: Optional[int] = None
    ):
        self.master_ticket_id = master_ticket_id or f"MST-{uuid.uuid4().hex[:8].upper()}"
        self.department = department
        self.title = title
        self.issue_type = issue_type
        self.ward_id = ward_id
        self.ward_name = ward_name
        self.lat = lat
        self.lon = lon
        self.urgency = urgency
        self.status = status
        self.assigned_engineer = assigned_engineer
        self.first_reported_at = first_reported_at or datetime.now(timezone.utc).isoformat()
        self.last_reported_at = self.first_reported_at
        self.citizen_reports: List[Dict[str, Any]] = []
        self._initial_report_count = report_count or 0
        self.national_mission = national_mission or "Swachh Bharat / AMRUT Urban Mission"
        self.citizen_charter_sla_hours = citizen_charter_sla_hours or (24 if urgency in ["High", "Critical"] else 48)
        self.sla_hours_remaining = self.citizen_charter_sla_hours
        self.jan_sunwai_status = jan_sunwai_status
        if self.urgency in ["High", "Critical"] and self.jan_sunwai_status == "NONE":
            self.jan_sunwai_status = "ESCALATED"
        self.corporator = corporator or {"name": "Ward Councillor", "designation": "Parshad", "phone": "N/A"}
        self.mla = mla or {"name": "Constituency MLA", "constituency": "Constituency"}
        self.ward_sabha_schedule = ward_sabha_schedule or "1st Saturday of Month, 10:30 AM"
        self.desilting_readiness_pct = desilting_readiness_pct or 75
        self.mcd_zone = mcd_zone or "Karol Bagh Zone"
        self.city = city or "Pan-India"
        self.corporation = corporation or "Municipal Corporation"
        self.zone = zone or self.mcd_zone
        self.agent_trace = agent_trace or []

    @property
    def report_count(self) -> int:
        return max(len(self.citizen_reports), self._initial_report_count)

    @property
    def current_sla_hours_remaining(self) -> int:
        if self.status == "RESOLVED":
            return 0
        try:
            created_dt = datetime.fromisoformat(self.first_reported_at.replace("Z", "+00:00"))
            now_dt = datetime.now(timezone.utc)
            elapsed_hours = (now_dt - created_dt).total_seconds() / 3600.0
            remaining = int(round(self.sla_hours_remaining - elapsed_hours))
            return max(0, remaining)
        except Exception:
            return max(0, self.sla_hours_remaining)

    @property
    def is_sla_breached(self) -> bool:
        if self.status == "RESOLVED":
            return False
        try:
            created_dt = datetime.fromisoformat(self.first_reported_at.replace("Z", "+00:00"))
            now_dt = datetime.now(timezone.utc)
            elapsed_hours = (now_dt - created_dt).total_seconds() / 3600.0
            return elapsed_hours > self.citizen_charter_sla_hours
        except Exception:
            return False

    def add_report(self, complaint: ComplaintRecord):
        self.citizen_reports.append({
            "complaint_id": complaint.complaint_id,
            "citizen_name": complaint.citizen_name,
            "citizen_phone": complaint.citizen_phone,
            "raw_text": complaint.raw_text,
            "channel": complaint.channel,
            "created_at": complaint.created_at,
            "lat": complaint.lat,
            "lon": complaint.lon
        })
        if self._initial_report_count > 0:
            self._initial_report_count += 1
        self.last_reported_at = complaint.created_at

        # Check if the incoming complaint has higher urgency than the master ticket
        urgency_ranks = {"Low": 1, "Medium": 2, "High": 3, "Critical": 4}
        complaint_urgency = complaint.urgency
        current_rank = urgency_ranks.get(self.urgency, 2)
        new_rank = urgency_ranks.get(complaint_urgency, 2)
        
        if new_rank > current_rank:
            self.urgency = complaint_urgency
            if complaint_urgency == "Critical":
                self.sla_hours_remaining = min(self.sla_hours_remaining, 12)
            elif complaint_urgency == "High":
                self.sla_hours_remaining = min(self.sla_hours_remaining, 24)

        # Dynamic urgency escalation on high volume of reports
        if len(self.citizen_reports) >= 5 and urgency_ranks.get(self.urgency, 2) < 3:
            self.urgency = "High"
            self.sla_hours_remaining = min(self.sla_hours_remaining, 12)
        elif len(self.citizen_reports) >= 15:
            self.urgency = "Critical"
            self.sla_hours_remaining = min(self.sla_hours_remaining, 6)

        # Automatic Jan Sunwai / Samadhan Diwas escalation for high-traction civic issues
        # or when any complaint/hazard is High or Critical
        if len(self.citizen_reports) >= 3 or self.urgency in ["High", "Critical"]:
            self.jan_sunwai_status = "ESCALATED"

    def to_dict(self) -> Dict[str, Any]:
        # Statutory Jan Sunwai escalation if Citizen Charter SLA is breached
        if self.is_sla_breached and self.jan_sunwai_status == "NONE":
            self.jan_sunwai_status = "ESCALATED"

        return {
            "master_ticket_id": self.master_ticket_id,
            "department": self.department,
            "title": self.title,
            "issue_type": self.issue_type,
            "ward_id": self.ward_id,
            "ward_name": self.ward_name,
            "lat": self.lat,
            "lon": self.lon,
            "urgency": self.urgency,
            "status": self.status,
            "report_count": self.report_count,
            "citizen_reports": self.citizen_reports,
            "first_reported_at": self.first_reported_at,
            "last_reported_at": self.last_reported_at,
            "sla_hours_remaining": self.current_sla_hours_remaining,
            "is_sla_breached": self.is_sla_breached,
            "assigned_engineer": self.assigned_engineer,
            "national_mission": self.national_mission,
            "citizen_charter_sla_hours": self.citizen_charter_sla_hours,
            "jan_sunwai_status": self.jan_sunwai_status,
            "corporator": self.corporator,
            "mla": self.mla,
            "ward_sabha_schedule": self.ward_sabha_schedule,
            "desilting_readiness_pct": self.desilting_readiness_pct,
            "mcd_zone": self.mcd_zone,
            "city": self.city,
            "corporation": self.corporation,
            "zone": self.zone,
            "agent_trace": self.agent_trace
        }
