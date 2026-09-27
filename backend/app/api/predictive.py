from fastapi import APIRouter
from typing import List, Dict, Any
from ..models.schemas import WardRiskResponse, PredictiveAssetResponse
from ..db.database import db
from ..core.predictive_engine import predictive_engine
from ..utils.weather import fetch_open_meteo_forecast

router = APIRouter(prefix="/predictive-maintenance", tags=["Predictive Maintenance & Risk Index"])

@router.get("/ward-risk", response_model=List[WardRiskResponse], summary="Get Ward Vulnerability Scores ahead of monsoon")
async def get_ward_risk_index():
    """
    Computes real-time Ward Vulnerability Index (0-100) combining live Open-Meteo precipitation
    forecasts, elevation topography, drainage coverage, and recent grievance choke reports.
    """
    results: List[WardRiskResponse] = []

    for ward in db.wards:
        # Fetch weather for ward center
        weather = await fetch_open_meteo_forecast(ward["center_lat"], ward["center_lon"])
        rainfall_24h = weather["rainfall_24h_mm"]
        rainfall_48h = weather["rainfall_48h_mm"]

        # Count active open tickets in this ward
        active_count = sum(
            1 for t in db.master_tickets.values()
            if t.ward_id == ward["ward_id"] and t.status != "RESOLVED"
        )

        risk_data = predictive_engine.calculate_ward_risk(
            ward_data=ward,
            active_complaint_count=active_count,
            rainfall_24h_mm=rainfall_24h,
            rainfall_48h_mm=rainfall_48h
        )
        results.append(risk_data)

    results.sort(key=lambda x: x.risk_score, reverse=True)
    return results

@router.get("/assets", response_model=List[PredictiveAssetResponse], summary="Get physical municipal assets with failure probabilities")
async def get_predictive_assets():
    """
    Returns condition rating and failure likelihood of physical municipal infrastructure
    (stormwater drains, transformers, arterial roads).
    """
    results = []
    # Representative forecast rain for stress calculation
    typical_rain = 65.0

    for asset in db.assets:
        pred = predictive_engine.assess_asset_failure(asset, typical_rain)
        results.append(pred)

    results.sort(key=lambda x: x.failure_probability, reverse=True)
    return results
