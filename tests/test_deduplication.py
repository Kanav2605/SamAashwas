import pytest
from datetime import datetime, timezone
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

    # New complaint 50 meters away about the same sewer overflow (Water radius is 150m)
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
    assert dist < 150.0
    assert sim >= 0.70

def test_deduplication_category_aware_radius_roads():
    # Potholes category radius is 40m
    master = MasterTicketRecord(
        department="Roads & Traffic Infrastructure",
        title="Pothole near 27th Main cross",
        issue_type="Potholes",
        ward_id="WARD-01",
        ward_name="Indiranagar",
        lat=12.971600,
        lon=77.641200
    )

    # Complaint 60 meters away (outside 40m road radius)
    complaint_far = ComplaintRecord(
        raw_text="Huge pothole on road near 27th Main",
        department="Roads & Traffic Infrastructure",
        issue_type="Potholes",
        urgency="Critical",
        location_landmark="27th Main",
        ward_extracted="Ward 1",
        language_detected="English",
        lat=12.972150, # ~62 meters away
        lon=77.641200
    )

    matched_far, dist_far, _ = deduplicator.find_matching_master_ticket(
        complaint_far,
        [master]
    )
    assert matched_far is None # Rejected because distance > 40m road radius

    # Complaint 20 meters away (within 40m road radius)
    complaint_near = ComplaintRecord(
        raw_text="Huge pothole on road near 27th Main",
        department="Roads & Traffic Infrastructure",
        issue_type="Potholes",
        urgency="Critical",
        location_landmark="27th Main",
        ward_extracted="Ward 1",
        language_detected="English",
        lat=12.971750, # ~17 meters away
        lon=77.641200
    )

    matched_near, dist_near, _ = deduplicator.find_matching_master_ticket(
        complaint_near,
        [master]
    )
    assert matched_near is not None
    assert dist_near <= 40.0

def test_deduplication_cluster_diameter_cap():
    # Road radius = 40m, Cap = 2 * 40 = 80m
    master = MasterTicketRecord(
        department="Roads & Traffic Infrastructure",
        title="Pothole cluster on Main Road",
        issue_type="Potholes",
        ward_id="WARD-01",
        ward_name="Indiranagar",
        lat=12.971600,
        lon=77.641200
    )
    # Master ticket has a report at south edge: ~35m south
    master.citizen_reports.append({
        "lat": 12.971300,
        "lon": 77.641200,
        "raw_text": "Pothole at south intersection"
    })

    # New complaint is ~35m north of master center, meaning distance from south report is ~70m (within 80m cap)
    new_within = ComplaintRecord(
        raw_text="Pothole on Main Road near center",
        department="Roads & Traffic Infrastructure",
        issue_type="Potholes",
        urgency="High",
        location_landmark="Main Road",
        ward_extracted="Ward 1",
        language_detected="English",
        lat=12.971800,
        lon=77.641200
    )
    assert deduplicator.check_cluster_diameter_cap(master, new_within, 40.0) is True

    # New complaint that would make pairwise distance > 80m from the south report
    new_exceeds = ComplaintRecord(
        raw_text="Pothole on Main Road far north",
        department="Roads & Traffic Infrastructure",
        issue_type="Potholes",
        urgency="High",
        location_landmark="Main Road",
        ward_extracted="Ward 1",
        language_detected="English",
        lat=12.972300, # ~110m north of south report
        lon=77.641200
    )
    assert deduplicator.check_cluster_diameter_cap(master, new_exceeds, 40.0) is False

def test_recurrence_and_false_closure_detection():
    resolved_master = MasterTicketRecord(
        department="Sanitation & Solid Waste",
        title="Garbage Dump near Market",
        issue_type="Garbage Dump",
        ward_id="WARD-03",
        ward_name="Karol Bagh",
        lat=28.6514,
        lon=77.1907
    )
    resolved_master.status = "RESOLVED"
    resolved_master.resolved_at = datetime.now(timezone.utc).isoformat()

    new_complaint = ComplaintRecord(
        raw_text="Garbage pile accumulated again at same market spot",
        department="Sanitation & Solid Waste",
        issue_type="Garbage Dump",
        urgency="High",
        location_landmark="Market",
        ward_extracted="Ward 3",
        language_detected="English",
        lat=28.6515, # ~20m away
        lon=77.1908
    )

    result = deduplicator.find_recurrent_issue(new_complaint, [resolved_master], max_days=30)
    assert result is not None
    matched_master, dist = result
    assert matched_master.master_ticket_id == resolved_master.master_ticket_id
    assert dist <= 80.0
