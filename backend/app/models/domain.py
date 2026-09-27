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
        created_at: Optional[str] = None
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
            "created_at": self.created_at
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
        first_reported_at: Optional[str] = None
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
        self.sla_hours_remaining = 24 if urgency in ["High", "Critical"] else 48

    @property
    def report_count(self) -> int:
        return len(self.citizen_reports)

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
        self.last_reported_at = complaint.created_at
        # Dynamic urgency escalation on high volume of reports
        if len(self.citizen_reports) >= 5 and self.urgency not in ["High", "Critical"]:
            self.urgency = "High"
            self.sla_hours_remaining = 12
        elif len(self.citizen_reports) >= 15:
            self.urgency = "Critical"
            self.sla_hours_remaining = 6

    def to_dict(self) -> Dict[str, Any]:
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
            "sla_hours_remaining": self.sla_hours_remaining,
            "assigned_engineer": self.assigned_engineer
        }
