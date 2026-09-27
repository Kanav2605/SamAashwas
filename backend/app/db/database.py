import json
import os
import logging
from typing import Dict, List, Optional, Any
from ..models.domain import ComplaintRecord, MasterTicketRecord
from ..models.schemas import (
    ComplaintCreateRequest,
    ComplaintResponse,
    MasterTicketResponse,
    TicketStatusEnum,
    UrgencyEnum,
    AnalyticsStatsResponse,
    MasterTicketUpdateRequest
)
from ..core.nlp_engine import nlp_engine
from ..core.vision_engine import vision_engine
from ..core.deduplication import deduplicator
from ..utils.geo_utils import find_closest_ward

logger = logging.getLogger(__name__)

class MunicipalDatabase:
    """
    In-memory and persistent spatial repository managing Complaints,
    Master Tickets, Municipal Assets, and Wards with Indian civic governance capabilities.
    """
    def __init__(self):
        self.complaints: Dict[str, ComplaintRecord] = {}
        self.master_tickets: Dict[str, MasterTicketRecord] = {}
        self.wards: List[Dict[str, Any]] = []
        self.assets: List[Dict[str, Any]] = []
        self._load_initial_metadata()

    def _load_initial_metadata(self):
        # Locate municipal_assets.json
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
        asset_path = os.path.join(base_dir, "data", "municipal_assets.json")
        
        if os.path.exists(asset_path):
            try:
                with open(asset_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.wards = data.get("wards", [])
                    self.assets = data.get("assets", [])
                    logger.info(f"Loaded {len(self.wards)} wards and {len(self.assets)} assets.")
            except Exception as e:
                logger.error(f"Error loading municipal assets: {e}")
        
        if not self.wards:
            # Fallback default wards if file not found
            self.wards = [
                {
                    "ward_id": "WARD-01",
                    "ward_name": "Indiranagar Central",
                    "city": "Bengaluru",
                    "center_lat": 12.9716,
                    "center_lon": 77.6412,
                    "population": 65000,
                    "low_lying_zone": false,
                    "drainage_coverage_pct": 82,
                    "corporator": {"name": "Smt. Lakshmi Devi", "designation": "Parshad", "phone": "+91-98450-11221"},
                    "mla": {"name": "Shri N.A. Haris", "constituency": "Shantinagar"},
                    "ward_sabha_schedule": "Every 1st Saturday, 10:30 AM",
                    "pre_monsoon_desilting_pct": 86,
                    "primary_mission": "Smart Cities & Urban Drainage"
                },
                {
                    "ward_id": "WARD-02",
                    "ward_name": "Koramangala 4th Block",
                    "city": "Bengaluru",
                    "center_lat": 12.9352,
                    "center_lon": 77.6245,
                    "population": 82000,
                    "low_lying_zone": true,
                    "drainage_coverage_pct": 68,
                    "corporator": {"name": "Shri M. Chandrappa", "designation": "Parshad", "phone": "+91-98450-22334"},
                    "mla": {"name": "Shri Ramalinga Reddy", "constituency": "BTM Layout"},
                    "ward_sabha_schedule": "Every 2nd Saturday, 11:00 AM",
                    "pre_monsoon_desilting_pct": 62,
                    "primary_mission": "AMRUT 2.0 & Jal Jeevan Mission"
                }
            ]

    def submit_complaint(self, req: ComplaintCreateRequest) -> ComplaintRecord:
        """
        Process a new citizen grievance through the end-to-end AI pipeline:
        1. NLP analysis (Code-mixed multilingual parsing, department routing, mission tagging, entity extraction)
        2. Vision verification (Spam check & photo authenticity)
        3. Ward determination (Associates Corporator, MLA, Ward Sabha schedule)
        4. Spatio-temporal deduplication (300m spatial gate + semantic similarity)
        5. Master Ticket creation or clustering with Jan Sunwai escalation
        """
        # Step 1: Code-mixed NLP Analysis
        nlp_result = nlp_engine.analyze(req.raw_text)

        # Step 2: Vision Verification
        vision_result = vision_engine.verify_image(
            text_complaint=req.raw_text,
            department=nlp_result.department,
            image_url=req.image_url,
            image_category_hint=req.image_category_hint
        )

        # Step 3: Ward Determination
        assigned_ward = find_closest_ward(req.lat, req.lon, self.wards)
        ward_id = assigned_ward.get("ward_id", "WARD-01")
        ward_name = assigned_ward.get("ward_name", "Local Ward")
        corporator_info = assigned_ward.get("corporator", {})
        mla_info = assigned_ward.get("mla", {})
        ward_sabha = assigned_ward.get("ward_sabha_schedule", "1st Saturday of Month, 10:30 AM")
        desilting_pct = assigned_ward.get("pre_monsoon_desilting_pct", 75)
        mission_name = nlp_result.national_mission or assigned_ward.get("primary_mission", "Swachh Bharat / AMRUT Urban Mission")

        # Create Complaint Record
        complaint = ComplaintRecord(
            raw_text=req.raw_text,
            department=nlp_result.department,
            issue_type=nlp_result.issue_type,
            urgency=nlp_result.urgency.value,
            location_landmark=nlp_result.location_landmark,
            ward_extracted=ward_name,
            language_detected=nlp_result.language_detected,
            lat=req.lat,
            lon=req.lon,
            channel=req.channel.value,
            citizen_name=req.citizen_name or "Citizen",
            citizen_phone=req.citizen_phone or "9876543210",
            image_verification=vision_result.dict() if vision_result else None,
            national_mission=mission_name,
            citizen_charter_sla_hours=nlp_result.citizen_charter_sla_hours,
            jan_sunwai_eligible=(nlp_result.urgency.value in ["High", "Critical"]),
            corporator_name=corporator_info.get("name", "Ward Councillor"),
            mla_name=mla_info.get("name", "Constituency MLA"),
            audio_transcript=req.audio_transcript
        )

        # Step 4: Spatio-Temporal Deduplication Check
        active_masters = [m for m in self.master_tickets.values() if m.status != "RESOLVED"]
        matching_master, dist, sim = deduplicator.find_matching_master_ticket(
            complaint,
            active_masters
        )

        if matching_master:
            # Duplicate detected! Cluster into existing Master Ticket
            complaint.master_ticket_id = matching_master.master_ticket_id
            complaint.is_duplicate = True
            matching_master.add_report(complaint)
            logger.info(f"Duplicate merged into {matching_master.master_ticket_id} (Dist: {dist:.1f}m, Sim: {sim:.2f})")
        else:
            # Unique incident! Generate new Master Ticket
            initial_jan_sunwai = "ESCALATED" if complaint.urgency in ["High", "Critical"] else "NONE"
            new_master = MasterTicketRecord(
                department=complaint.department,
                title=f"{complaint.issue_type} near {complaint.location_landmark}",
                issue_type=complaint.issue_type,
                ward_id=ward_id,
                ward_name=ward_name,
                lat=complaint.lat,
                lon=complaint.lon,
                urgency=complaint.urgency,
                status="OPEN",
                national_mission=mission_name,
                citizen_charter_sla_hours=complaint.citizen_charter_sla_hours,
                jan_sunwai_status=initial_jan_sunwai,
                corporator=corporator_info,
                mla=mla_info,
                ward_sabha_schedule=ward_sabha,
                desilting_readiness_pct=desilting_pct
            )
            new_master.add_report(complaint)
            complaint.master_ticket_id = new_master.master_ticket_id
            complaint.is_duplicate = False
            self.master_tickets[new_master.master_ticket_id] = new_master
            logger.info(f"Created new Master Ticket {new_master.master_ticket_id} in {ward_name}")

        self.complaints[complaint.complaint_id] = complaint
        return complaint

    def get_all_complaints(self, limit: int = 100) -> List[Dict[str, Any]]:
        items = list(self.complaints.values())
        items.sort(key=lambda x: x.created_at, reverse=True)
        return [c.to_dict() for c in items[:limit]]

    def get_master_tickets(
        self,
        status: Optional[str] = None,
        jan_sunwai_only: bool = False,
        mission: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        tickets = list(self.master_tickets.values())
        if status:
            tickets = [t for t in tickets if t.status == status]
        if jan_sunwai_only:
            tickets = [t for t in tickets if t.jan_sunwai_status == "ESCALATED"]
        if mission:
            tickets = [t for t in tickets if mission.lower() in (t.national_mission or "").lower()]

        tickets.sort(key=lambda x: (
            x.jan_sunwai_status == "ESCALATED",
            x.urgency == "Critical",
            x.urgency == "High",
            x.report_count
        ), reverse=True)
        return [t.to_dict() for t in tickets]

    def get_master_ticket_by_id(self, ticket_id: str) -> Optional[MasterTicketRecord]:
        return self.master_tickets.get(ticket_id)

    def update_master_ticket(self, ticket_id: str, update: MasterTicketUpdateRequest) -> Optional[MasterTicketRecord]:
        ticket = self.master_tickets.get(ticket_id)
        if not ticket:
            return None
        if update.status:
            ticket.status = update.status.value
        if update.urgency:
            ticket.urgency = update.urgency.value
        if update.assigned_engineer:
            ticket.assigned_engineer = update.assigned_engineer
        if update.jan_sunwai_status:
            ticket.jan_sunwai_status = update.jan_sunwai_status
        return ticket

    def get_analytics_stats(self) -> AnalyticsStatsResponse:
        total_complaints = len(self.complaints)
        total_masters = len(self.master_tickets)
        duplicates = sum(1 for c in self.complaints.values() if c.is_duplicate)
        rate = round((duplicates / total_complaints * 100.0), 1) if total_complaints > 0 else 0.0

        dept_counts: Dict[str, int] = {}
        ward_counts: Dict[str, int] = {}
        urgency_counts: Dict[str, int] = {}
        mission_counts: Dict[str, int] = {}
        lang_counts: Dict[str, int] = {}

        for c in self.complaints.values():
            dept_counts[c.department] = dept_counts.get(c.department, 0) + 1
            ward_counts[c.ward_extracted] = ward_counts.get(c.ward_extracted, 0) + 1
            urgency_counts[c.urgency] = urgency_counts.get(c.urgency, 0) + 1
            lang_counts[c.language_detected] = lang_counts.get(c.language_detected, 0) + 1
            if c.national_mission:
                mission_counts[c.national_mission] = mission_counts.get(c.national_mission, 0) + 1

        jan_sunwai_count = sum(1 for m in self.master_tickets.values() if m.jan_sunwai_status == "ESCALATED")

        return AnalyticsStatsResponse(
            total_complaints=total_complaints,
            total_master_tickets=total_masters,
            total_duplicates_filtered=duplicates,
            deduplication_rate_pct=rate,
            department_breakdown=dept_counts,
            ward_breakdown=ward_counts,
            urgency_breakdown=urgency_counts,
            high_risk_wards_count=sum(1 for w in self.wards if w.get("low_lying_zone")),
            national_mission_breakdown=mission_counts,
            jan_sunwai_escalated_count=jan_sunwai_count,
            language_breakdown=lang_counts
        )

# Global database singleton
db = MunicipalDatabase()
