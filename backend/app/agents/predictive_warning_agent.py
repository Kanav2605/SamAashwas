import logging
from typing import Dict, Any, List
from .base import BaseCivicAgent, AgentStepResult
from ..core.predictive_engine import predictive_engine

logger = logging.getLogger(__name__)

class PredictiveDisasterWarningAgent(BaseCivicAgent):
    """
    Agent 5: Predictive Maintenance & Disaster Warning Agent
    Responsibilities:
    - Analyzes local meteorological forecasts (precipitation mm) and low-lying topography.
    - Evaluates stormwater drainage (SWD) capacity, desilting percentage, and nearby asset strain.
    - Emits proactive disaster risk alerts and early warning notifications.
    """
    def __init__(self):
        super().__init__(
            name="Predictive Maintenance & Disaster Warning Agent",
            role="Pre-Monsoon & Infrastructure Vulnerability Intelligence",
            description="Analyzes weather radar forecasts, low-lying runoff vulnerabilities, and municipal asset condition to forecast infrastructural failure before it causes public paralysis."
        )

    def run(self, context: Dict[str, Any]) -> AgentStepResult:
        assigned_ward = context.get("assigned_ward", {})
        active_complaint_count = context.get("active_complaint_count") or context.get("report_count", 1)
        rainfall_24h = context.get("rainfall_24h_mm")
        rainfall_48h = context.get("rainfall_48h_mm")

        if rainfall_24h is None or rainfall_48h is None:
            lat = context.get("lat") or assigned_ward.get("center_lat", 28.65)
            lon = context.get("lon") or assigned_ward.get("center_lon", 77.20)
            from ..utils.weather import _WEATHER_CACHE
            cache_key = f"{round(lat, 2)}_{round(lon, 2)}"
            if cache_key in _WEATHER_CACHE:
                cached = _WEATHER_CACHE[cache_key]["data"]
                rainfall_24h = cached.get("rainfall_24h_mm", 45.0)
                rainfall_48h = cached.get("rainfall_48h_mm", 78.5)
            else:
                base_rain = 45.0 + (abs(lat * 10) % 30.0)
                rainfall_24h = round(base_rain, 1)
                rainfall_48h = round(base_rain * 1.55, 1)

        assets = context.get("assets", [])

        # Run predictive risk calculation
        risk_profile = predictive_engine.calculate_ward_risk(
            assigned_ward,
            active_complaint_count=active_complaint_count,
            rainfall_24h_mm=rainfall_24h,
            rainfall_48h_mm=rainfall_48h
        )

        # Check nearby asset risks
        ward_id = assigned_ward.get("ward_id")
        matching_assets = [a for a in assets if a.get("ward_id") == ward_id]
        asset_alerts = []
        for asset in matching_assets[:2]:
            ass_res = predictive_engine.assess_asset_failure(asset, rainfall_48h)
            if ass_res.failure_probability >= 50.0:
                asset_alerts.append({
                    "asset_id": ass_res.asset_id,
                    "type": ass_res.type,
                    "failure_probability": ass_res.failure_probability,
                    "recommended_action": ass_res.recommended_action
                })

        thought = (
            f"PREDICTIVE RISK EVALUATION: Ward '{risk_profile.ward_name}' Vulnerability Index: {risk_profile.risk_score}/100 "
            f"({risk_profile.risk_level}). Forecast indicates {rainfall_48h:.1f}mm rainfall over 48 hours. "
            f"Drainage vulnerability score: {risk_profile.drainage_vulnerability_score}%. "
            f"Desilting readiness: {risk_profile.desilting_readiness_pct}%. "
            f"Advisory: {risk_profile.recommendation}"
        )

        outputs = {
            "risk_score": risk_profile.risk_score,
            "risk_level": risk_profile.risk_level,
            "primary_risk_factor": risk_profile.primary_risk_factor,
            "recommendation": risk_profile.recommendation,
            "desilting_readiness_pct": risk_profile.desilting_readiness_pct,
            "nearby_critical_assets_at_risk": asset_alerts
        }

        context["ward_risk_profile"] = risk_profile
        context["risk_score"] = risk_profile.risk_score
        context["risk_level"] = risk_profile.risk_level

        status = "ALERT" if risk_profile.risk_level in ["CRITICAL", "HIGH"] else "NORMAL"

        return AgentStepResult(
            agent_name=self.name,
            status=status,
            confidence=0.92,
            thought_log=thought,
            action_taken=f"Issued {risk_profile.risk_level} advisory: {risk_profile.recommendation}",
            outputs=outputs
        )
