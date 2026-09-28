from typing import Optional
from fastapi import APIRouter
from ..models.schemas import AnalyticsStatsResponse
from ..db.database import db

router = APIRouter(prefix="/analytics", tags=["ULB Command Center Analytics"])

@router.get("/stats", response_model=AnalyticsStatsResponse, summary="Get city-wide incident and deduplication analytics")
async def get_city_analytics(city: Optional[str] = None):
    """
    Returns aggregated metrics: total citizen reports, master tickets created,
    deduplication reduction rate, and department distribution.
    """
    return db.get_analytics_stats(city=city)
