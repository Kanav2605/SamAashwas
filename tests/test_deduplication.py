import pytest
from backend.app.core.deduplication import deduplicator
from backend.app.models.domain import ComplaintRecord, MasterTicketRecord

def test_deduplication_clusters_within_radius():
    # Active master ticket in Koramangala
    master = MasterTicketRecord(
        department="Water Supply & Sewage",
        title="Sewer Line Overflow near Sharma General Store",
        issue_type="Sewer Line Overflow",
        ward_id="WARD-02",
        ward_name="Koramangala 4th Block",
        lat=12.935200,
        lon=77.624500
    )

    # New complaint 50 meters away about the same sewer overflow
    new_complaint = ComplaintRecord(
        raw_text="Ward 2 gali mein sewer overflow ho raha hai, gutter ganda paani near Sharma General Store",
        department="Water Supply & Sewage",
        issue_type="Sewer Line Overflow",
        urgency="High",
        location_landmark="Sharma General Store",
        ward_extracted="Ward 2",
        language_detected="Hinglish",
        lat=12.935400, # ~25 meters away
        lon=77.624550
    )

    matched, dist, sim = deduplicator.find_matching_master_ticket(
        new_complaint,
        [master]
    )

    assert matched is not None
    assert matched.master_ticket_id == master.master_ticket_id
    assert dist < 300.0
    assert sim >= 0.70

def test_deduplication_rejects_distant_complaint():
    # Master ticket in Koramangala
    master = MasterTicketRecord(
        department="Water Supply & Sewage",
        title="Sewer Line Overflow near Sharma General Store",
        issue_type="Sewer Line Overflow",
        ward_id="WARD-02",
        ward_name="Koramangala 4th Block",
        lat=12.935200,
        lon=77.624500
    )

    # Same complaint text but in Indiranagar (4 km away)
    new_complaint = ComplaintRecord(
        raw_text="Sewer line overflow near Sharma store",
        department="Water Supply & Sewage",
        issue_type="Sewer Line Overflow",
        urgency="High",
        location_landmark="Sharma store",
        ward_extracted="Ward 1",
        language_detected="English",
        lat=12.971600, # Indiranagar (~5km away)
        lon=77.641200
    )

    matched, dist, sim = deduplicator.find_matching_master_ticket(
        new_complaint,
        [master]
    )

    assert matched is None # Outside 300m geographic gate
    assert dist > 300.0
