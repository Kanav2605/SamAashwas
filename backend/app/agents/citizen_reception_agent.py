import logging
from typing import Dict, Any
from .base import BaseCivicAgent, AgentStepResult
from ..core.nlp_engine import nlp_engine

logger = logging.getLogger(__name__)

class CitizenReceptionAgent(BaseCivicAgent):
    """
    Agent 1: Citizen Reception Agent
    Responsibilities:
    - Multilingual & code-mixed parsing (Hinglish, Hindi, Kannada, Tamil, English).
    - Entity extraction (location landmarks, ward hints, issue type, urgency).
    - National mission tagging (Swachh Bharat, AMRUT 2.0, Smart Cities).
    - Channel ingestion & citizen tone analysis.
    """
    def __init__(self):
        super().__init__(
            name="Citizen Reception Agent",
            role="Multilingual Ingestion & Grievance Understanding",
            description="Ingests citizen complaints across WhatsApp, Web Portal, Voice notes, and Helplines; normalizes vernacular dialects and extracts civic entities."
        )

    def run(self, context: Dict[str, Any]) -> AgentStepResult:
        raw_text = context.get("raw_text", "")
        channel = context.get("channel", "web_portal")
        audio_transcript = context.get("audio_transcript")
        citizen_name = context.get("citizen_name", "Citizen")

        # Process through NLP engine
        nlp_result = nlp_engine.analyze(raw_text)

        # Build transparent thought reasoning
        thought = (
            f"Received report via {channel} from {citizen_name}. "
            f"Detected language '{nlp_result.language_detected}'. "
            f"Extracted department '{nlp_result.department}' and issue '{nlp_result.issue_type}' "
            f"with urgency rating '{nlp_result.urgency.value}' (Confidence: {nlp_result.confidence*100:.1f}%). "
            f"Identified landmark: '{nlp_result.location_landmark}'. "
            f"Tagged Flagship Scheme: '{nlp_result.national_mission}' with statutory SLA of {nlp_result.citizen_charter_sla_hours} hours."
        )

        outputs = {
            "department": nlp_result.department,
            "issue_type": nlp_result.issue_type,
            "urgency": nlp_result.urgency.value,
            "location_landmark": nlp_result.location_landmark,
            "ward_extracted": nlp_result.ward_extracted,
            "language_detected": nlp_result.language_detected,
            "confidence": nlp_result.confidence,
            "national_mission": nlp_result.national_mission,
            "citizen_charter_sla_hours": nlp_result.citizen_charter_sla_hours
        }

        # Update shared context
        context["nlp_result"] = nlp_result
        context["department"] = nlp_result.department
        context["issue_type"] = nlp_result.issue_type
        context["urgency"] = nlp_result.urgency.value
        context["location_landmark"] = nlp_result.location_landmark
        context["language_detected"] = nlp_result.language_detected
        context["national_mission"] = nlp_result.national_mission
        context["citizen_charter_sla_hours"] = nlp_result.citizen_charter_sla_hours

        return AgentStepResult(
            agent_name=self.name,
            status="SUCCESS",
            confidence=nlp_result.confidence,
            thought_log=thought,
            action_taken=f"Standardized intake & classified into '{nlp_result.department}' under '{nlp_result.national_mission}'.",
            outputs=outputs
        )
