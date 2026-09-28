import logging
from typing import Dict, Any
from .base import BaseCivicAgent, AgentStepResult

logger = logging.getLogger(__name__)

class CivicOmbudsmanJanSunwaiAgent(BaseCivicAgent):
    """
    Agent 6: Civic Ombudsman & Jan Sunwai Escalation Agent
    Responsibilities:
    - Independent citizen ombudsman oversight.
    - Automatic escalation to Friday Jan Sunwai (Public Grievance Day / Samadhan Diwas) docket.
    - Monitors SLA non-compliance, recurring neighborhood issues, and severe safety hazards.
    - Ensures public transparency and democratic review by Municipal Commissioner & Ward Council.
    """
    def __init__(self):
        super().__init__(
            name="Civic Ombudsman & Jan Sunwai Escalation Agent",
            role="Public Accountability, SLA Oversight & Jan Sunwai Docketing",
            description="Autonomous civic ombudsman protecting citizen rights; audits SLA compliance, recurrent hazard clusters, and automatically dockets neglected grievances directly before the Municipal Commissioner."
        )

    def run(self, context: Dict[str, Any]) -> AgentStepResult:
        urgency = context.get("urgency", "Medium")
        report_count = context.get("report_count", 1)
        is_sla_breached = context.get("is_sla_breached", False)
        manual_escalation = context.get("manual_escalation", False)
        department = context.get("department", "General")
        ward_name = context.get("ward_name", "Municipal Ward")
        mcd_zone = context.get("mcd_zone", "MCD Zone")

        # Statutory Jan Sunwai Trigger criteria
        is_escalated = False
        reasons = []

        if manual_escalation:
            is_escalated = True
            reasons.append("Manual Ombudsman docketing requested by citizen/councillor")

        if urgency in ["Critical", "High"]:
            is_escalated = True
            reasons.append(f"Statutory high-severity hazard classification ({urgency})")

        if report_count >= 3:
            is_escalated = True
            reasons.append(f"Community grievance density reached ({report_count} citizen reports)")

        if is_sla_breached:
            is_escalated = True
            reasons.append("Statutory Citizen Charter SLA exceeded without field resolution")

        if is_escalated:
            status = "ESCALATED"
            jan_sunwai_docket_status = "ESCALATED"
            reason_text = " | ".join(reasons)
            thought = (
                f"OMBUDSMAN INTERVENTION ACTIVATED: Grievance meets statutory Jan Sunwai criteria: {reason_text}. "
                f"Auto-docketed for hearing on next Friday 11:00 AM at {mcd_zone} Zonal Office. "
                f"Mandatory appearance logged for Executive Engineer and Ward Junior Engineer."
            )
            action = f"Docketed to Jan Sunwai Public Hearing. Direct review by Municipal Commissioner & Zonal DC."
        else:
            status = "MONITORED"
            jan_sunwai_docket_status = "NONE"
            thought = (
                f"SLA COMPLIANCE MONITORING: Incident urgency is {urgency} with {report_count} report(s). "
                f"Standard executive workflow active under SLA timer. Case maintained on ombudsman watch docket."
            )
            action = "Maintained in active monitoring state. Standard SLA countdown in effect."

        outputs = {
            "jan_sunwai_status": jan_sunwai_docket_status,
            "hearing_day": "Friday 11:00 AM (Zonal Jan Sunwai / Samadhan Diwas)",
            "ombudsman_audit_passed": True,
            "escalation_reasons": reasons
        }

        context["jan_sunwai_status"] = jan_sunwai_docket_status

        return AgentStepResult(
            agent_name=self.name,
            status=status,
            confidence=0.99,
            thought_log=thought,
            action_taken=action,
            outputs=outputs
        )
