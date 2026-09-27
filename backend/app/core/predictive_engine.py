import logging
from typing import Dict, Any, List
from ..models.schemas import WardRiskResponse, PredictiveAssetResponse

logger = logging.getLogger(__name__)

class PredictiveMaintenanceEngine:
    """
    Module 4: Spatio-Temporal Predictive Risk Modeling.
    Calculates Ward Vulnerability Scores (0-100) and asset failure probabilities
    combining weather forecasts, historical grievance density, and asset age.
    """

    def calculate_ward_risk(
        self,
        ward_data: Dict[str, Any],
        active_complaint_count: int,
        rainfall_24h_mm: float,
        rainfall_48h_mm: float
    ) -> WardRiskResponse:
        """
        Calculate the multi-factor vulnerability score for a municipal ward.
        Formula components:
        1. Precipitation Severity (Weight: 35%)
        2. Low-Lying Topography & Elevation Deficit (Weight: 25%)
        3. Inadequate Drainage Coverage (Weight: 20%)
        4. Recent Grievance Load / Choking History (Weight: 20%)
        """
        # 1. Rain Factor (0 to 100)
        # 75mm in 48h in Indian urban settings is severe waterlogging threshold
        rain_score = min(100.0, (rainfall_48h_mm / 75.0) * 100.0)

        # 2. Topographical Factor
        is_low_lying = ward_data.get("low_lying_zone", False)
        topo_score = 85.0 if is_low_lying else 25.0

        # 3. Drainage Coverage Deficit
        drain_coverage = ward_data.get("drainage_coverage_pct", 75)
        drain_deficit_score = max(0.0, 100.0 - drain_coverage)

        # 4. Grievance Density Factor
        grievance_score = min(100.0, active_complaint_count * 5.0)

        # Weighted Composite Vulnerability Score
        risk_score = (
            (rain_score * 0.35) +
            (topo_score * 0.25) +
            (drain_deficit_score * 0.20) +
            (grievance_score * 0.20)
        )
        risk_score = round(min(100.0, max(0.0, risk_score)), 1)

        # Determine Risk Level Category
        if risk_score >= 80.0:
            risk_level = "CRITICAL"
            primary_factor = "High monsoon rainfall combined with low-lying catchment and blocked SWD drains."
            recommendation = "Deploy emergency high-discharge dewatering pumps and pre-monsoon desilting squads immediately."
        elif risk_score >= 60.0:
            risk_level = "HIGH"
            primary_factor = "Elevated drainage deficit with moderate-to-heavy rainfall warning."
            recommendation = "Inspect primary stormwater outlets, deploy mobile dewatering pumps, and execute desilting of bottlenecks within 24 hours."
        elif risk_score >= 35.0:
            risk_level = "MEDIUM"
            primary_factor = "Moderate rain forecast with adequate natural runoff."
            recommendation = "Put ward junior engineers on standby and verify pump fuel reserves."
        else:
            risk_level = "LOW"
            primary_factor = "Stable topography and minimal expected precipitation."
            recommendation = "Routine scheduled maintenance."

        return WardRiskResponse(
            ward_id=ward_data["ward_id"],
            ward_name=ward_data["ward_name"],
            center_lat=ward_data["center_lat"],
            center_lon=ward_data["center_lon"],
            risk_score=risk_score,
            risk_level=risk_level,
            primary_risk_factor=primary_factor,
            rainfall_forecast_24h_mm=rainfall_24h_mm,
            rainfall_forecast_48h_mm=rainfall_48h_mm,
            active_complaints_count=active_complaint_count,
            drainage_vulnerability_score=round(drain_deficit_score, 1),
            recommendation=recommendation,
            desilting_readiness_pct=ward_data.get("pre_monsoon_desilting_pct", 75),
            corporator=ward_data.get("corporator"),
            ward_sabha_schedule=ward_data.get("ward_sabha_schedule")
        )

    def assess_asset_failure(self, asset: Dict[str, Any], rainfall_48h_mm: float) -> PredictiveAssetResponse:
        """
        Assess failure probability of a physical municipal asset (Drain, Transformer, Road).
        """
        health_score = float(asset.get("structural_health_score", 60))
        installed_year = asset.get("installed_year", 2015)
        age_years = max(1, 2026 - installed_year)

        # Base failure rate increases with age and low health
        base_failure = (100.0 - health_score) * 0.6 + (age_years * 2.0)
        
        # Weather stress amplifier
        stress = min(30.0, (rainfall_48h_mm / 100.0) * 25.0)
        failure_prob = round(min(98.0, max(5.0, base_failure + stress)), 1)

        vulnerability = asset.get("vulnerability_flag", "NORMAL")
        
        if failure_prob >= 75.0:
            action = "Dispatch immediate preventative crew for reinforcement / desilting."
        elif failure_prob >= 50.0:
            action = "Schedule preventive inspection within 48 hours."
        else:
            action = "Normal operating condition."

        return PredictiveAssetResponse(
            asset_id=asset["asset_id"],
            type=asset["type"],
            ward_id=asset["ward_id"],
            lat=asset["lat"],
            lon=asset["lon"],
            structural_health_score=health_score,
            failure_probability=failure_prob,
            vulnerability_flag=vulnerability,
            recommended_action=action
        )

# Global predictive engine
predictive_engine = PredictiveMaintenanceEngine()
