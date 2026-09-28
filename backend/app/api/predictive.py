import asyncio
from fastapi import APIRouter, Query
from typing import List, Dict, Any, Optional
from ..models.schemas import WardRiskResponse, PredictiveAssetResponse
from ..db.database import db
from ..core.predictive_engine import predictive_engine
from ..utils.weather import fetch_open_meteo_forecast

router = APIRouter(prefix="/predictive-maintenance", tags=["Predictive Maintenance & Risk Index"])

@router.get("/ward-risk", response_model=List[WardRiskResponse], summary="Get Ward Vulnerability Scores ahead of monsoon")
async def get_ward_risk_index(city: Optional[str] = Query(None, description="Optional city filter")):
    """
    Computes real-time Ward Vulnerability Index (0-100) combining live Open-Meteo precipitation
    forecasts, elevation topography, drainage coverage, and recent grievance choke reports.
    """
    wards = db.wards
    if city:
        c_low = city.lower().strip()
        wards = [w for w in wards if c_low in (w.get("city") or "").lower() or c_low in (w.get("corporation") or "").lower()]

    async def _compute_ward(ward):
        weather = await fetch_open_meteo_forecast(ward["center_lat"], ward["center_lon"])
        rainfall_24h = weather["rainfall_24h_mm"]
        rainfall_48h = weather["rainfall_48h_mm"]

        active_count = sum(
            1 for t in db.master_tickets.values()
            if t.ward_id == ward["ward_id"] and t.status != "RESOLVED"
        )

        return predictive_engine.calculate_ward_risk(
            ward_data=ward,
            active_complaint_count=active_count,
            rainfall_24h_mm=rainfall_24h,
            rainfall_48h_mm=rainfall_48h
        )

    results = await asyncio.gather(*[_compute_ward(w) for w in wards])
    results = list(results)
    results.sort(key=lambda x: x.risk_score, reverse=True)
    return results

@router.get("/assets", response_model=List[PredictiveAssetResponse], summary="Get physical municipal assets with failure probabilities")
async def get_predictive_assets(city: Optional[str] = Query(None, description="Optional city filter")):
    """
    Returns condition rating and failure likelihood of physical municipal infrastructure
    (stormwater drains, transformers, arterial roads).
    """
    results = []
    typical_rain = 65.0
    assets = db.assets
    if city:
        c_low = city.lower().strip()
        # Find ward IDs for city
        matching_ward_ids = {w["ward_id"] for w in db.wards if c_low in (w.get("city") or "").lower() or c_low in (w.get("corporation") or "").lower()}
        assets = [a for a in assets if a.get("ward_id") in matching_ward_ids]

    for asset in assets:
        pred = predictive_engine.assess_asset_failure(asset, typical_rain)
        results.append(pred)

    results.sort(key=lambda x: x.failure_probability, reverse=True)
    return results
