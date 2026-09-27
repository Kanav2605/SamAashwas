import pytest
from backend.app.core.predictive_engine import predictive_engine

def test_ward_vulnerability_calculation_low_lying():
    ward_data = {
        "ward_id": "WARD-02",
        "ward_name": "Koramangala 4th Block",
        "center_lat": 12.9352,
        "center_lon": 77.6245,
        "low_lying_zone": True,
        "drainage_coverage_pct": 60
    }

    # Severe rainfall: 80mm in 48h
    risk = predictive_engine.calculate_ward_risk(
        ward_data=ward_data,
        active_complaint_count=12,
        rainfall_24h_mm=50.0,
        rainfall_48h_mm=80.0
    )

    assert risk.ward_id == "WARD-02"
    assert risk.risk_score >= 70.0
    assert risk.risk_level in ["HIGH", "CRITICAL"]
    assert "pump" in risk.recommendation.lower() or "desilting" in risk.recommendation.lower()

def test_asset_failure_probability():
    asset = {
        "asset_id": "DRAIN-01",
        "type": "Primary Stormwater Drain",
        "ward_id": "WARD-02",
        "lat": 12.9348,
        "lon": 77.6251,
        "installed_year": 2010,
        "structural_health_score": 40,
        "vulnerability_flag": "HIGH_SILT_ACCUMULATION"
    }

    pred = predictive_engine.assess_asset_failure(asset, rainfall_48h_mm=75.0)
    assert pred.failure_probability >= 50.0
    assert pred.structural_health_score == 40.0
