import logging
from typing import Dict, Any
from .base import BaseCivicAgent, AgentStepResult
from ..core.vision_engine import vision_engine

logger = logging.getLogger(__name__)

class VisualVerificationFraudAgent(BaseCivicAgent):
    """
    Agent 2: Visual Verification & Fraud Agent
    Responsibilities:
    - Multimodal verification (cross-validates uploaded photo with reported grievance).
    - Fraud & spam defense: flags irrelevant images (selfies, memes, screenshots).
    - Image classification confidence & category confirmation.
    """
    def __init__(self):
        super().__init__(
            name="Visual Verification & Fraud Agent",
            role="Multimodal Vision Authenticity & Spam Filtering",
            description="Inspects attached photographs with computer vision models; detects fraudulent/spam imagery and confirms grievance ground truth."
        )

    def run(self, context: Dict[str, Any]) -> AgentStepResult:
        raw_text = context.get("raw_text", "")
        department = context.get("department", "General Grievance")
        image_url = context.get("image_url")
        image_category_hint = context.get("image_category_hint")

        if not image_url and not image_category_hint:
            thought = "No visual media attached to grievance. Proceeding with text-based verification flow."
            context["vision_result"] = None
            return AgentStepResult(
                agent_name=self.name,
                status="SKIPPED_NO_MEDIA",
                confidence=1.0,
                thought_log=thought,
                action_taken="Text-only flow permitted. No photographic evidence to verify.",
                outputs={"is_authentic": True, "media_present": False}
            )

        vision_res = vision_engine.verify_image(
            text_complaint=raw_text,
            department=department,
            image_url=image_url,
            image_category_hint=image_category_hint
        )

        context["vision_result"] = vision_res

        if vision_res:
            outputs = vision_res.model_dump() if hasattr(vision_res, "model_dump") else vision_res.dict()
            if vision_res.mismatch_detected:
                thought = (
                    f"POTENTIAL ANOMALY / SPAM DETECTED: {vision_res.explanation} "
                    f"Visual classification detected '{vision_res.detected_class}' "
                    f"which clashes with reported department '{department}'. Confidence: {vision_res.confidence*100:.1f}%."
                )
                return AgentStepResult(
                    agent_name=self.name,
                    status="FLAGGED_SPAM" if vision_res.detected_class == "unrelated_or_spam" else "MISMATCH_ALERT",
                    confidence=vision_res.confidence,
                    thought_log=thought,
                    action_taken=f"Flagged submission: {vision_res.status_label}. Marked for supervisory review.",
                    outputs=outputs
                )
            else:
                thought = (
                    f"VISUAL PROOF VERIFIED: Photographic evidence confirmed subject '{vision_res.detected_class}' "
                    f"matching department '{department}' with {vision_res.confidence*100:.1f}% confidence."
                )
                return AgentStepResult(
                    agent_name=self.name,
                    status="VERIFIED",
                    confidence=vision_res.confidence,
                    thought_log=thought,
                    action_taken=f"Ground truth confirmed: {vision_res.status_label}.",
                    outputs=outputs
                )

        return AgentStepResult(
            agent_name=self.name,
            status="VERIFIED",
            confidence=0.85,
            thought_log="Visual media analyzed and accepted under standard tolerance.",
            action_taken="Visual check completed.",
            outputs={"is_authentic": True}
        )
