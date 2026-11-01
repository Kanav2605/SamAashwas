from fastapi import APIRouter, HTTPException, Query, Body
from typing import Dict, Any, List, Optional
from ..core.dispatch_optimizer import dispatch_optimizer
from ..db.database import db

router = APIRouter(prefix="/dispatch", tags=["Municipal Field Crew Dispatch"])

@router.post("/optimize", summary="Optimize squad dispatch route vs FIFO baseline")
async def optimize_dispatch(
    lat: float = Query(12.9716, ge=6.0, le=38.0, description="Field squad current latitude"),
    lon: float = Query(77.6412, ge=68.0, le=98.0, description="Field squad current longitude"),
    city: Optional[str] = Query(None, description="City filter"),
    department: Optional[str] = Query(None, description="Department filter (e.g. Roads, Sanitation)")
):
    """
    Computes an optimized dispatch visiting order for pending master tickets using
    priority-weighted greedy insertion with 2-opt search, benchmarked against FIFO baseline.
    """
    tickets = db.get_master_tickets(status="OPEN", city=city)
    if not tickets:
        tickets = db.get_master_tickets(city=city)[:8]

    if department:
        tickets = [t for t in tickets if department.lower() in t.get("department", "").lower()]

    result = dispatch_optimizer.optimize_route((lat, lon), tickets)
    return result
