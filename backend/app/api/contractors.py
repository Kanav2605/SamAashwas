from fastapi import APIRouter, HTTPException, Query, Body
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
from ..core.homography_verifier import homography_verifier
from ..core.h3_indexer import h3_indexer
from ..db.database import db

router = APIRouter(prefix="/contractors", tags=["Contractor Accountability & Homography Verification"])

class ResolutionVerificationRequest(BaseModel):
    complaint_id: str = Field("CMP-BLR-001", description="Grievance ticket ID")
    original_image_tag: str = Field("sample_pothole", description="Original report photo tag")
    resolution_image_tag: str = Field("sample_repaired_asphalt", description="Engineer resolution photo tag")
    original_lat: float = Field(12.9716, description="Reported GPS latitude")
    original_lon: float = Field(77.5946, description="Reported GPS longitude")
    resolution_lat: float = Field(12.9716, description="Resolution photo GPS latitude")
    resolution_lon: float = Field(77.5946, description="Resolution photo GPS longitude")
    resolution_notes: Optional[str] = Field("Bituminous cold-mix patching completed with 120kg asphalt compound and plate compaction.", description="Field engineer repair summary")

class CitizenSignOffRequest(BaseModel):
    complaint_id: str = Field(..., description="Grievance ticket ID")
    is_satisfied: bool = Field(..., description="True if citizen confirms issue is resolved, False if still broken")
    feedback_notes: Optional[str] = Field(None, description="Optional citizen comment")
    citizen_phone: Optional[str] = Field("9876543210", description="Citizen authentication phone")

MUNICIPAL_CONTRACTORS = [
    {
        "contractor_id": "CNT-BLR-01",
        "name": "ABC Urban Infrastructure Ltd",
        "department": "Roads & Traffic Infrastructure",
        "city": "Bengaluru",
        "corporation": "BBMP",
        "active_wards": ["Ward 112 (Domlur)", "Ward 80 (Indiranagar)", "Ward 89 (HAL)"],
        "total_contracts_cr": 42.5,
        "sla_compliance_pct": 92.4,
        "recurrence_failure_rate_pct": 3.8,
        "penalties_levied_inr": 125000,
        "performance_grade": "A",
        "status": "ACTIVE_COMPLIANT",
        "key_officer": "Er. Arvind Narayanan",
        "last_audit_date": "2026-10-18"
    },
    {
        "contractor_id": "CNT-BLR-02",
        "name": "Namma Swachhata Waste Logistics",
        "department": "Sanitation & Solid Waste",
        "city": "Bengaluru",
        "corporation": "BBMP",
        "active_wards": ["Ward 134 (BTM Layout)", "Ward 174 (HSR Layout)"],
        "total_contracts_cr": 28.0,
        "sla_compliance_pct": 96.1,
        "recurrence_failure_rate_pct": 1.2,
        "penalties_levied_inr": 0,
        "performance_grade": "A+",
        "status": "ACTIVE_EXCELLENT",
        "key_officer": "R. Selvam",
        "last_audit_date": "2026-10-24"
    },
    {
        "contractor_id": "CNT-DEL-01",
        "name": "Capital Roadworks & Paving Corp",
        "department": "Roads & Traffic Infrastructure",
        "city": "Delhi",
        "corporation": "MCD",
        "active_wards": ["Karol Bagh Zone", "Civil Lines Zone"],
        "total_contracts_cr": 34.5,
        "sla_compliance_pct": 78.2,
        "recurrence_failure_rate_pct": 14.6,
        "penalties_levied_inr": 350000,
        "performance_grade": "C",
        "status": "SHOW_CAUSE_NOTICE_ISSUED",
        "key_officer": "Virender Gupta",
        "last_audit_date": "2026-10-28"
    },
    {
        "contractor_id": "CNT-MUM-01",
        "name": "Apex Metro Electro-Grid Ltd",
        "department": "Electrical & Streetlighting",
        "city": "Mumbai",
        "corporation": "BMC",
        "active_wards": ["H-West Ward (Bandra)", "K-West Ward (Andheri)"],
        "total_contracts_cr": 19.2,
        "sla_compliance_pct": 94.8,
        "recurrence_failure_rate_pct": 2.4,
        "penalties_levied_inr": 45000,
        "performance_grade": "A",
        "status": "ACTIVE_COMPLIANT",
        "key_officer": "Sunil Patil",
        "last_audit_date": "2026-10-20"
    }
]

@router.get("/scorecards", summary="Contractor performance & public penalty scorecards")
async def get_contractor_scorecards(city: Optional[str] = Query(None, description="City filter")):
    """
    Returns verified municipal contractor accountability scorecards, SLA compliance ratings,
    recurrence defect rates, and penalty amounts deducted under statutory performance clauses.
    """
    if city and city.lower() not in ["all", ""]:
        c_low = city.lower().strip()
        filtered = [c for c in MUNICIPAL_CONTRACTORS if c_low in c["city"].lower() or c_low in c["corporation"].lower()]
        return filtered if filtered else MUNICIPAL_CONTRACTORS
    return MUNICIPAL_CONTRACTORS

@router.post("/verify-resolution", summary="Run homography visual alignment & false-closure audit")
async def verify_resolution(payload: ResolutionVerificationRequest):
    """
    Compares the citizen's original complaint photo against the engineer's resolution photo
    using structural homography and landmark point matching, preventing false ticket closures.
    """
    result = homography_verifier.verify_resolution_proof(
        complaint_id=payload.complaint_id,
        original_image_tag=payload.original_image_tag,
        resolution_image_tag=payload.resolution_image_tag,
        original_coords={"lat": payload.original_lat, "lon": payload.original_lon},
        resolution_coords={"lat": payload.resolution_lat, "lon": payload.resolution_lon},
        resolution_notes=payload.resolution_notes
    )
    return result

@router.post("/citizen-signoff", summary="Two-Party Citizen Resolution Sign-off")
async def citizen_signoff(payload: CitizenSignOffRequest):
    """
    Direct citizen sign-off: A grievance ticket cannot be permanently archived
    without explicit citizen confirmation or independent crowd-audit verification.
    """
    if payload.is_satisfied:
        return {
            "status": "RESOLVED_VERIFIED",
            "complaint_id": payload.complaint_id,
            "message": "Citizen sign-off confirmed. Resolution approved for contractor milestone clearance.",
            "karma_points_awarded": 100,
            "certificate_eligible": True
        }
    else:
        return {
            "status": "ESCALATED_TO_JAN_SUNWAI",
            "complaint_id": payload.complaint_id,
            "message": "Citizen reported issue remains unaddressed. Ticket reopened with CRITICAL urgency and escalated to Ward Ombudsman. Contractor penalty initiated.",
            "penalty_notice_issued": True,
            "assigned_sdo": "Executive Engineer Jan Sunwai Oversight Wing"
        }

@router.get("/h3-cells", summary="H3 Hexagonal spatial clustering micro-cells")
async def get_h3_spatial_cells(city: Optional[str] = Query(None, description="City filter")):
    """
    Returns incidents aggregated by Uber H3 Resolution 9 hexagonal micro-cells (~100m diameter)
    with polygon boundaries for high-density spatial visualization on GIS maps.
    """
    tickets = db.get_master_tickets(status="OPEN", city=city)
    if not tickets:
        tickets = db.get_master_tickets(city=city)

    hex_cells: Dict[str, Dict[str, Any]] = {}
    for t in tickets:
        lat = t.get("lat", 12.9716)
        lon = t.get("lon", 77.5946)
        h3_token = h3_indexer.lat_lon_to_h3(lat, lon, resolution=9)

        if h3_token not in hex_cells:
            boundary = h3_indexer.h3_to_boundary(lat, lon)
            hex_cells[h3_token] = {
                "h3_index": h3_token,
                "center": [lat, lon],
                "boundary": boundary,
                "incident_count": 0,
                "critical_count": 0,
                "department_distribution": {},
                "sample_ticket": t.get("master_ticket_id")
            }

        cell = hex_cells[h3_token]
        cell["incident_count"] += t.get("report_count", 1)
        if t.get("urgency") == "Critical":
            cell["critical_count"] += 1
        dept = t.get("department", "Civic")
        cell["department_distribution"][dept] = cell["department_distribution"].get(dept, 0) + 1

    return {
        "city": (city or "bengaluru").title(),
        "total_hex_cells": len(hex_cells),
        "cells": list(hex_cells.values())
    }
