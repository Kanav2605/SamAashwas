import logging
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone

from .base import BaseCivicAgent, AgentStepResult
from .citizen_reception_agent import CitizenReceptionAgent
from .vision_fraud_agent import VisualVerificationFraudAgent
from .geo_dedup_agent import GeoDeduplicationAgent
from .ward_sla_routing_agent import WardSlaRoutingAgent
from .predictive_warning_agent import PredictiveDisasterWarningAgent
from .ombudsman_escalation_agent import CivicOmbudsmanJanSunwaiAgent

logger = logging.getLogger(__name__)

class MultiAgentOrchestrator:
    """
    Central Controller for SamAashwas Autonomous Civic Agents.
    Orchestrates the continuous lifecycle of grievance resolution across:
    1. Citizen Reception Agent
    2. Visual Verification & Fraud Agent
    3. Ward & SLA Routing Agent
    4. Geo-Deduplication & Clustering Agent
    5. Predictive Maintenance & Disaster Warning Agent
    6. Civic Ombudsman & Jan Sunwai Escalation Agent
    """

    def __init__(self):
        self.reception_agent = CitizenReceptionAgent()
        self.vision_agent = VisualVerificationFraudAgent()
        self.ward_routing_agent = WardSlaRoutingAgent()
        self.dedup_agent = GeoDeduplicationAgent()
        self.predictive_agent = PredictiveDisasterWarningAgent()
        self.ombudsman_agent = CivicOmbudsmanJanSunwaiAgent()

        self.agents: List[BaseCivicAgent] = [
            self.reception_agent,
            self.vision_agent,
            self.ward_routing_agent,
            self.dedup_agent,
            self.predictive_agent,
            self.ombudsman_agent
        ]

    def get_agent_manifest(self) -> List[Dict[str, Any]]:
        """Return operational status and metadata for all 6 agents."""
        return [
            {
                "id": f"agent_{i+1}",
                "name": agent.name,
                "role": agent.role,
                "description": agent.description,
                "status": "OPERATIONAL",
                "framework": "SamAashwas Multi-Agent Engine v2.0"
            }
            for i, agent in enumerate(self.agents)
        ]

    def orchestrate_complaint(
        self,
        raw_text: str,
        lat: float,
        lon: float,
        channel: str = "web_portal",
        citizen_name: str = "Citizen",
        citizen_phone: str = "9876543210",
        image_url: Optional[str] = None,
        image_category_hint: Optional[str] = None,
        audio_transcript: Optional[str] = None,
        wards: Optional[List[Dict[str, Any]]] = None,
        active_masters: Optional[List[Any]] = None,
        assets: Optional[List[Dict[str, Any]]] = None,
        complaint_record_ref: Optional[Any] = None
    ) -> Dict[str, Any]:
        """
        Executes end-to-end multi-agent evaluation and returns complete transparent trace.
        """
        trace: List[Dict[str, Any]] = []

        context: Dict[str, Any] = {
            "raw_text": raw_text,
            "lat": lat,
            "lon": lon,
            "channel": channel,
            "citizen_name": citizen_name,
            "citizen_phone": citizen_phone,
            "image_url": image_url,
            "image_category_hint": image_category_hint,
            "audio_transcript": audio_transcript,
            "wards": wards or [],
            "active_masters": active_masters or [],
            "assets": assets or [],
            "complaint_record": complaint_record_ref
        }

        # Step 1: Citizen Reception Agent
        step1 = self.reception_agent.run(context)
        trace.append(step1.dict())

        # Step 2: Visual Verification & Fraud Agent
        step2 = self.vision_agent.run(context)
        trace.append(step2.dict())

        # Step 3: Ward & SLA Routing Agent
        step3 = self.ward_routing_agent.run(context)
        trace.append(step3.dict())

        # Step 4: Geo-Deduplication & Clustering Agent
        step4 = self.dedup_agent.run(context)
        trace.append(step4.dict())

        # Prepare context for Predictive & Ombudsman
        context["report_count"] = 1
        if context.get("matching_master"):
            context["report_count"] = context["matching_master"].report_count + 1

        # Step 5: Predictive Maintenance & Disaster Warning Agent
        step5 = self.predictive_agent.run(context)
        trace.append(step5.dict())

        # Step 6: Civic Ombudsman & Jan Sunwai Escalation Agent
        step6 = self.ombudsman_agent.run(context)
        trace.append(step6.dict())

        narrative = (
            f"Grievance near '{context.get('location_landmark')}' ingested by {self.reception_agent.name} as '{context.get('department')}' ({context.get('urgency')}). "
            f"Visual verification: {step2.status}. "
            f"Routed to {context.get('mcd_zone')} ({context.get('ward_name')}) with {context.get('sla_hours')}h Citizen Charter SLA. "
            f"Deduplication status: {step4.status}. "
            f"Vulnerability risk score: {context.get('risk_score', 'N/A')}/100 ({context.get('risk_level', 'NORMAL')}). "
            f"Ombudsman status: {context.get('jan_sunwai_status')} for Friday Jan Sunwai hearing."
        )

        return {
            "orchestration_status": "COMPLETED",
            "agent_trace": trace,
            "narrative_summary": narrative,
            "department": context.get("department"),
            "issue_type": context.get("issue_type"),
            "urgency": context.get("urgency"),
            "location_landmark": context.get("location_landmark"),
            "mcd_zone": context.get("mcd_zone"),
            "ward_name": context.get("ward_name"),
            "assigned_engineer": context.get("assigned_engineer"),
            "sla_hours": context.get("sla_hours"),
            "is_duplicate": context.get("is_duplicate", False),
            "matching_master_id": context.get("matching_master").master_ticket_id if context.get("matching_master") else None,
            "jan_sunwai_status": context.get("jan_sunwai_status"),
            "vision_result": context.get("vision_result").dict() if context.get("vision_result") else None
        }

# Global singleton
agent_orchestrator = MultiAgentOrchestrator()
