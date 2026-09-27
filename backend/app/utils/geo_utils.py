import math
from typing import Dict, Any, List, Optional

def haversine_distance_meters(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate the great circle distance between two points on Earth in meters.
    """
    R = 6371000.0  # Earth's radius in meters
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = (
        math.sin(delta_phi / 2.0) ** 2
        + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2.0) ** 2
    )
    c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
    return R * c

def is_within_radius(lat1: float, lon1: float, lat2: float, lon2: float, radius_meters: float = 300.0) -> bool:
    """
    Returns True if two points are within the given radius in meters.
    """
    return haversine_distance_meters(lat1, lon1, lat2, lon2) <= radius_meters

def find_closest_ward(lat: float, lon: float, wards: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Find the closest municipal ward to a given coordinate.
    """
    if not wards:
        return {"ward_id": "WARD-01", "ward_name": "General Municipal Ward"}

    closest_ward = wards[0]
    min_dist = float("inf")

    for w in wards:
        dist = haversine_distance_meters(lat, lon, w["center_lat"], w["center_lon"])
        if dist < min_dist:
            min_dist = dist
            closest_ward = w

    return closest_ward
