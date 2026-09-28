"""
SamAashwas Multi-Agent Civic Orchestration System.
Coordinates 6 specialized autonomous agents:
1. Citizen Reception Agent
2. Visual Verification & Fraud Agent
3. Geo-Deduplication & Clustering Agent
4. Ward & SLA Routing Agent
5. Predictive Maintenance & Disaster Warning Agent
6. Civic Ombudsman & Jan Sunwai Escalation Agent
"""

from .orchestrator import MultiAgentOrchestrator, agent_orchestrator

__all__ = ["MultiAgentOrchestrator", "agent_orchestrator"]
