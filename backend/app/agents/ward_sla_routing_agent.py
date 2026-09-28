import logging
from typing import Dict, Any, List
from .base import BaseCivicAgent, AgentStepResult
from ..utils.geo_utils import find_closest_ward

logger = logging.getLogger(__name__)

class WardSlaRoutingAgent(BaseCivicAgent):
    """
    Agent 4: Ward & SLA Routing Agent
    Responsibilities:
    - Geo-spatial administrative boundary routing (MCD Zones & Ward allocation).
    - Citizen Charter SLA calculation based on issue urgency and statutory service guarantees.
    - Official assignment: Ward Junior Engineer (JE), Assistant Engineer (AE), Sanitary Inspector.
    - Democratic accountability binding: Ward Councillor (Parshad) and Constituency MLA.
    """
    def __init__(self):
        super().__init__(
            name="Ward & SLA Routing Agent",
            role="Jurisdictional Mapping, Officer Assignment & Citizen Charter SLA",
            description="Maps grievance coordinates to administrative Municipal Corporation of Delhi (MCD) zones and wards; binds responsible engineers, corporators, and enforces statutory Citizen Charter turnaround times."
        )

    def run(self, context: Dict[str, Any]) -> AgentStepResult:
        lat = context.get("lat", 0.0)
        lon = context.get("lon", 0.0)
        wards = context.get("wards", [])
        urgency = context.get("urgency", "Medium")
        department = context.get("department", "General")
        national_mission = context.get("national_mission", "Urban Municipal Mission")

        assigned_ward = find_closest_ward(lat, lon, wards)
        ward_id = assigned_ward.get("ward_id", "MCD-KB-01")
        ward_name = assigned_ward.get("ward_name", "Municipal Ward")
        mcd_zone = assigned_ward.get("mcd_zone") or assigned_ward.get("zone", "Karol Bagh Zone")
        corporator = assigned_ward.get("corporator", {"name": "Ward Councillor (Parshad)", "designation": "Parshad"})
        mla = assigned_ward.get("mla", {"name": "Constituency MLA", "constituency": "Delhi Vidhan Sabha"})
        ward_sabha = assigned_ward.get("ward_sabha_schedule", "Every 1st Saturday, 10:30 AM")

        # Officer assignment based on department
        if "Electrical" in department:
            assigned_engineer = f"{mcd_zone} AE (Electrical) / JE (Works)"
        elif "Sanitation" in department:
            assigned_engineer = f"{mcd_zone} Sanitary Inspector (SBM-Urban)"
        elif "Water" in department:
            assigned_engineer = f"{mcd_zone} Junior Engineer (Drainage & Water Supply)"
        elif "Road" in department:
            assigned_engineer = f"{mcd_zone} Assistant Engineer (Roads Division)"
        else:
            assigned_engineer = f"{mcd_zone} Ward Junior Engineer (JE-Works)"

        # Citizen Charter statutory SLA
        if urgency == "Critical":
            sla_hours = 12
        elif urgency == "High":
            sla_hours = 24
        else:
            sla_hours = 48

        thought = (
            f"ADMINISTRATIVE ROUTING: Mapped coordinates ({lat:.4f}, {lon:.4f}) to MCD Zone '{mcd_zone}', "
            f"Ward '{ward_name}' ({ward_id}). Assigned field officer: '{assigned_engineer}'. "
            f"Bound democratic accountability to Parshad: {corporator.get('name', 'N/A')} and MLA: {mla.get('name', 'N/A')}. "
            f"Citizen Charter SLA locked to {sla_hours} Hours under {national_mission}."
        )

        outputs = {
            "mcd_zone": mcd_zone,
            "ward_id": ward_id,
            "ward_name": ward_name,
            "assigned_engineer": assigned_engineer,
            "corporator": corporator,
            "mla": mla,
            "ward_sabha_schedule": ward_sabha,
            "citizen_charter_sla_hours": sla_hours
        }

        context["assigned_ward"] = assigned_ward
        context["mcd_zone"] = mcd_zone
        context["ward_id"] = ward_id
        context["ward_name"] = ward_name
        context["assigned_engineer"] = assigned_engineer
        context["corporator"] = corporator
        context["mla"] = mla
        context["ward_sabha_schedule"] = ward_sabha
        context["sla_hours"] = sla_hours

        return AgentStepResult(
            agent_name=self.name,
            status="ROUTED",
            confidence=0.99,
            thought_log=thought,
            action_taken=f"Routed to {mcd_zone} ({ward_name}), assigned to {assigned_engineer} with {sla_hours}h SLA.",
            outputs=outputs
        )
