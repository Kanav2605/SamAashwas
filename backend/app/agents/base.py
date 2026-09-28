from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from datetime import datetime, timezone
from pydantic import BaseModel, Field

class AgentStepResult(BaseModel):
    agent_name: str
    status: str # e.g. "SUCCESS", "VERIFIED", "MERGED", "NEW_MASTER", "ROUTED", "ALERT", "ESCALATED", "FLAGGED"
    confidence: float = 1.0
    thought_log: str
    action_taken: str
    outputs: Dict[str, Any] = Field(default_factory=dict)
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

class BaseCivicAgent(ABC):
    def __init__(self, name: str, role: str, description: str):
        self.name = name
        self.role = role
        self.description = description

    @abstractmethod
    def run(self, context: Dict[str, Any]) -> AgentStepResult:
        """
        Execute the agent's designated task given the blackboard context.
        Must return an AgentStepResult.
        """
        pass
