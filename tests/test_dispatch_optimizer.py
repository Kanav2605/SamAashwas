import pytest
from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.core.dispatch_optimizer import dispatch_optimizer

client = TestClient(app)

def test_dispatch_optimizer_computation():
    start_pos = (12.9716, 77.6412) # Indiranagar
    sample_tickets = [
        {"master_ticket_id": "T1", "lat": 12.9720, "lon": 77.6415, "urgency": "Medium", "sla_hours_remaining": 36},
        {"master_ticket_id": "T2", "lat": 12.9850, "lon": 77.6500, "urgency": "Critical", "sla_hours_remaining": 6},
        {"master_ticket_id": "T3", "lat": 12.9718, "lon": 77.6413, "urgency": "High", "sla_hours_remaining": 12},
        {"master_ticket_id": "T4", "lat": 12.9900, "lon": 77.6600, "urgency": "Low", "sla_hours_remaining": 48}
    ]

    result = dispatch_optimizer.optimize_route(start_pos, sample_tickets)
    assert len(result["optimized_sequence"]) == 4
    assert result["optimized_distance_km"] > 0
    assert result["fifo_distance_km"] >= result["optimized_distance_km"]
    assert "pct_distance_reduction" in result
    assert "fuel_saved_liters" in result

def test_dispatch_optimize_api_endpoint():
    resp = client.post("/api/v1/dispatch/optimize?lat=12.9716&lon=77.6412")
    assert resp.status_code == 200
    data = resp.json()
    assert "optimized_sequence" in data
    assert "fifo_sequence" in data
    assert "km_saved" in data
    assert "pct_distance_reduction" in data
