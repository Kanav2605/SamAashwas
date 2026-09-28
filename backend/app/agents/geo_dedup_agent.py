import logging
from typing import Dict, Any, List
from .base import BaseCivicAgent, AgentStepResult
from ..core.deduplication import deduplicator

logger = logging.getLogger(__name__)

class GeoDeduplicationAgent(BaseCivicAgent):
    """
    Agent 3: Geo-Deduplication & Clustering Agent
    Responsibilities:
    - 300m spatial perimeter gate check around incoming latitude/longitude.
    - Semantic similarity matching against active neighborhood incidents.
    - Prevents duplicate ticket clutter; aggregates citizen endorsements into unified Master Tickets.
    - Elevates incident priority when multiple citizens report the same issue.
    """
    def __init__(self):
        super().__init__(
            name="Geo-Deduplication & Clustering Agent",
            role="Spatial-Temporal Incident Aggregation & Deduplication",
            description="Evaluates 300-meter GPS radius and semantic embedding similarity to cluster redundant neighborhood reports into single authoritative Master Incidents."
        )

    def run(self, context: Dict[str, Any]) -> AgentStepResult:
        complaint = context.get("complaint_record")
        active_masters = context.get("active_masters", [])

        if not complaint:
            from types import SimpleNamespace
            complaint = SimpleNamespace(
                department=context.get("department", "General"),
                lat=context.get("lat", 0.0),
                lon=context.get("lon", 0.0),
                raw_text=context.get("raw_text", "")
            )

        if not active_masters:
            thought = (
                "No active master tickets found in local vicinity. "
                "Marking as initial incident anchor."
            )
            context["is_duplicate"] = False
            context["matching_master"] = None
            context["report_count"] = 1
            return AgentStepResult(
                agent_name=self.name,
                status="NEW_MASTER",
                confidence=0.98,
                thought_log=thought,
                action_taken="Determined unique spatial incident. Designating as new Master Ticket.",
                outputs={"is_duplicate": False, "merged_into": None}
            )

        matching_master, dist_m, similarity = deduplicator.find_matching_master_ticket(
            complaint,
            active_masters
        )

        if matching_master:
            new_report_count = matching_master.report_count + 1
            thought = (
                f"DUPLICATE DETECTED & CLUSTERED: Complaint is located {dist_m:.1f} meters from active Master Ticket "
                f"'{matching_master.master_ticket_id}' with text semantic similarity of {similarity*100:.1f}%. "
                f"Clustering into existing master ticket. Community weight increased to {new_report_count} citizen endorsements."
            )
            context["is_duplicate"] = True
            context["matching_master"] = matching_master
            context["dedup_distance_m"] = dist_m
            context["dedup_similarity"] = similarity
            context["report_count"] = new_report_count

            return AgentStepResult(
                agent_name=self.name,
                status="MERGED",
                confidence=similarity,
                thought_log=thought,
                action_taken=f"Clustered into existing Master Ticket {matching_master.master_ticket_id}. Prevented duplicate crew dispatch.",
                outputs={
                    "is_duplicate": True,
                    "master_ticket_id": matching_master.master_ticket_id,
                    "distance_meters": round(dist_m, 1),
                    "semantic_similarity": round(similarity, 3),
                    "new_report_count": matching_master.report_count + 1
                }
            )
        else:
            thought = (
                f"UNIQUE INCIDENT CONFIRMED: Evaluated {len(active_masters)} active master tickets within municipal jurisdiction. "
                f"No matching active incident within the 300m spatial gate & similarity threshold. Initializing new Master Ticket."
            )
            context["is_duplicate"] = False
            context["matching_master"] = None

            return AgentStepResult(
                agent_name=self.name,
                status="NEW_MASTER",
                confidence=0.95,
                thought_log=thought,
                action_taken="Spawned new Master Ticket anchor for local neighborhood.",
                outputs={"is_duplicate": False, "active_candidates_evaluated": len(active_masters)}
            )
