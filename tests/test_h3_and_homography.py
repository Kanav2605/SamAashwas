import pytest
from backend.app.core.h3_indexer import h3_indexer, H3SpatialIndexer
from backend.app.core.homography_verifier import homography_verifier, HomographyVisualVerifier

def test_h3_spatial_indexer_token_format():
    token = h3_indexer.lat_lon_to_h3(12.9716, 77.5946, resolution=9)
    assert isinstance(token, str)
    assert token.startswith("899")
    assert len(token) == 15

def test_h3_spatial_indexer_boundary_vertices():
    boundary = h3_indexer.h3_to_boundary(12.9716, 77.5946)
    assert len(boundary) == 6
    for lat, lon in boundary:
        assert isinstance(lat, float)
        assert isinstance(lon, float)
        assert abs(lat - 12.9716) < 0.001
        assert abs(lon - 77.5946) < 0.001

def test_h3_spatial_indexer_k_ring_neighbors():
    neighbors = h3_indexer.get_k_ring_neighbors(12.9716, 77.5946, k=1)
    assert len(neighbors) >= 6
    for token in neighbors:
        assert token.startswith("89")

def test_homography_verifier_genuine():
    res = homography_verifier.verify_resolution_proof(
        complaint_id="CMP-TEST-001",
        original_image_tag="sample_pothole",
        resolution_image_tag="sample_repaired_asphalt",
        original_coords={"lat": 12.9716, "lon": 77.5946},
        resolution_coords={"lat": 12.9716, "lon": 77.5946},
        resolution_notes="Repaired with bituminous hot mix"
    )
    assert res["is_authentic_resolution"] is True
    assert res["homography_match_score"] >= 0.70
    assert res["spatial_gate_passed"] is True
    assert res["status_verdict"] == "VERIFIED_GENUINE_REPAIR"
    assert res["contractor_accountability"]["penalty_levied_inr"] == 0
    assert len(res["landmark_alignment_points"]) == 4

def test_homography_verifier_shoes_or_desk_fraud():
    res = homography_verifier.verify_resolution_proof(
        complaint_id="CMP-TEST-002",
        original_image_tag="sample_pothole",
        resolution_image_tag="sample_shoes_desk",
        original_coords={"lat": 12.9716, "lon": 77.5946},
        resolution_coords={"lat": 12.9716, "lon": 77.5946},
        resolution_notes="Fake photo of shoes"
    )
    assert res["is_authentic_resolution"] is False
    assert res["status_verdict"] == "FALSE_CLOSURE_PREVENTED"
    assert res["contractor_accountability"]["penalty_levied_inr"] == 50000
    assert "Clause 14B" in res["contractor_accountability"]["statutory_clause"]
    assert len(res["landmark_alignment_points"]) == 0

def test_homography_verifier_excessive_spatial_delta():
    # 250m away from reported grievance site
    res = homography_verifier.verify_resolution_proof(
        complaint_id="CMP-TEST-003",
        original_image_tag="sample_pothole",
        resolution_image_tag="sample_repaired_asphalt",
        original_coords={"lat": 12.9716, "lon": 77.5946},
        resolution_coords={"lat": 12.9740, "lon": 77.5946},
        resolution_notes="Repair at different location"
    )
    assert res["is_authentic_resolution"] is False
    assert res["spatial_gate_passed"] is False
    assert res["status_verdict"] == "FALSE_CLOSURE_PREVENTED"
    assert res["contractor_accountability"]["penalty_levied_inr"] == 50000
