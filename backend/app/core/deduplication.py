import math
import re
import logging
from typing import List, Tuple, Optional, Dict, Any
from datetime import datetime, timezone, timedelta
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from ..models.domain import ComplaintRecord, MasterTicketRecord
from ..utils.geo_utils import haversine_distance_meters
from ..config import settings

logger = logging.getLogger(__name__)

# Category-aware spatial gating radii in meters (A6)
CATEGORY_RADII_METERS: Dict[str, float] = {
    "Roads & Traffic Infrastructure": 40.0,
    "Electrical & Streetlighting": 50.0,
    "Sanitation & Solid Waste": 80.0,
    "Water Supply & Sewage": 150.0,
    "Encroachment & Town Planning": 200.0,
    "Health & Vector Control": 200.0,
    "Disaster & Flood Management": 400.0,
    "default": 100.0
}

STOP_WORDS = {
    'bhaiya', 'hai', 'ho', 'raha', 'rahi', 'gaya', 'gayi', 'mein', 'par', 'pe', 'se', 'yeh', 'woh', 
    'ko', 'ka', 'ki', 'ke', 'the', 'is', 'a', 'an', 'in', 'on', 'at', 'for', 'of', 'to', 'and', 
    'since', 'been', 'it', 'this', 'that', 'are', 'am', 'was', 'were', 'near', 'neer', 'local', 'vicinity',
    'kripya', 'please', 'sir', 'madam'
}

SYNONYMS = {
    'dead': 'band', 'broken': 'band', 'closed': 'band', 'kharab': 'band', 'phuta': 'burst', 'phat': 'burst',
    'days': 'din', 'day': 'din',
    'sewer': 'gutter', 'sewage': 'gutter', 'drain': 'gutter', 'drainage': 'gutter', 'nali': 'gutter',
    'road': 'sadak', 'street': 'sadak', 'rasta': 'sadak', 'salai': 'sadak',
    'kachra': 'garbage', 'kuda': 'garbage', 'waste': 'garbage', 'trash': 'garbage', 'kuppai': 'garbage',
    'paani': 'water', 'pipe': 'pipeline', 'overflowing': 'overflow', 'neeru': 'water', 'thanneer': 'water',
    'potholes': 'pothole', 'gaddha': 'pothole', 'gaddhe': 'pothole', 'crater': 'pothole', 'khadda': 'pothole', 'gunta': 'pothole',
    'skidding': 'slipping', 'bikes': 'bike', 'motorcycle': 'bike', 'scooter': 'bike'
}

def _normalize_tokens(text: str) -> List[str]:
    words = re.findall(r'[a-zA-Z0-9]+', text.lower())
    return [SYNONYMS.get(w, w) for w in words if w not in STOP_WORDS]

class SemanticDeduplicator:
    """
    Spatio-Temporal Deduplication Engine v2 (A6).
    Combines category-aware radii (30m-400m), cluster diameter capping (2x radius),
    recurrence detection for false closures, and sub-word n-gram similarity.
    """

    def __init__(
        self,
        radius_meters: float = settings.DEDUPLICATION_RADIUS_METERS,
        similarity_threshold: float = settings.DEDUPLICATION_SIMILARITY_THRESHOLD
    ):
        self.radius_meters = radius_meters
        self.similarity_threshold = similarity_threshold

    def get_category_radius(self, department: Optional[str]) -> float:
        """
        Returns the category-specific spatial gating radius.
        """
        if not department:
            return CATEGORY_RADII_METERS["default"]
        return CATEGORY_RADII_METERS.get(department, CATEGORY_RADII_METERS["default"])

    def compute_text_similarity(self, text1: str, text2: str) -> float:
        """
        Compute semantic similarity score between two complaint descriptions using
        sub-word character n-gram embeddings and token containment (robust to Hinglish spelling variations).
        """
        if not text1 or not text2:
            return 0.0

        if text1.strip().lower() == text2.strip().lower():
            return 1.0

        norm1 = _normalize_tokens(text1)
        norm2 = _normalize_tokens(text2)
        s1, s2 = set(norm1), set(norm2)
        if not s1 or not s2:
            return 0.0

        inter = s1.intersection(s2)
        containment = len(inter) / min(len(s1), len(s2))
        jaccard = len(inter) / len(s1.union(s2))

        txt1 = ' '.join(norm1)
        txt2 = ' '.join(norm2)
        cg1 = set(txt1[i:i+3] for i in range(len(txt1)-2))
        cg2 = set(txt2[i:i+3] for i in range(len(txt2)-2))
        cg_overlap = len(cg1.intersection(cg2)) / max(1, min(len(cg1), len(cg2))) if (cg1 and cg2) else 0.0

        score = 0.50 * containment + 0.35 * cg_overlap + 0.15 * jaccard
        return round(score, 3)

    def check_cluster_diameter_cap(
        self,
        master: MasterTicketRecord,
        new_complaint: ComplaintRecord,
        category_radius: float
    ) -> bool:
        """
        Enforce cluster diameter cap of 2 * category_radius to prevent chaining drift.
        Returns True if adding this complaint keeps all pairwise distances within bounds.
        """
        max_allowed = 2.0 * category_radius
        for report in getattr(master, "citizen_reports", []):
            r_lat = report.get("lat")
            r_lon = report.get("lon")
            if r_lat is not None and r_lon is not None:
                dist = haversine_distance_meters(new_complaint.lat, new_complaint.lon, r_lat, r_lon)
                if dist > max_allowed:
                    return False
        return True

    def find_matching_master_ticket(
        self,
        new_complaint: ComplaintRecord,
        active_master_tickets: List[MasterTicketRecord]
    ) -> Tuple[Optional[MasterTicketRecord], float, float]:
        """
        Searches active master tickets for a matching incident using category-aware radii and cluster cap.
        Returns: (matching_master_ticket, distance_meters, similarity_score)
        """
        best_match = None
        best_sim = 0.0
        min_dist = float("inf")

        effective_radius = self.get_category_radius(new_complaint.department)

        for master in active_master_tickets:
            # Only compare tickets within the same department
            if master.department != new_complaint.department:
                continue

            # Only compare open or in-progress tickets
            if master.status in ["RESOLVED", "REJECTED"]:
                continue

            # 1. Geographic Gate Check using Category-Aware Radius
            dist_meters = haversine_distance_meters(
                new_complaint.lat,
                new_complaint.lon,
                master.lat,
                master.lon
            )

            if dist_meters <= effective_radius:
                # 2. Enforce Cluster Diameter Cap (A6)
                if not self.check_cluster_diameter_cap(master, new_complaint, effective_radius):
                    continue

                # 3. Semantic Similarity Check against the master ticket title and existing reports
                sim = self.compute_text_similarity(new_complaint.raw_text, master.title)

                # Compare against previous citizen reports attached to this master
                for report in getattr(master, "citizen_reports", [])[:5]:
                    report_sim = self.compute_text_similarity(new_complaint.raw_text, report.get("raw_text", ""))
                    if report_sim > sim:
                        sim = report_sim

                # If same issue type or landmark match, boost confidence within radius
                issue1 = getattr(new_complaint, "issue_type", None)
                issue2 = getattr(master, "issue_type", None)
                if issue1 and issue2 and issue1.lower() == issue2.lower():
                    sim = min(1.0, sim + 0.12)

                landmark = getattr(new_complaint, "location_landmark", None)
                if (
                    landmark 
                    and landmark.lower() != "local vicinity"
                    and landmark.lower() in master.title.lower()
                ):
                    sim = min(1.0, sim + 0.10)

                # Proximity boost
                if dist_meters <= (effective_radius * 0.4):
                    sim = min(1.0, sim + 0.12)

                # If exceeds similarity threshold and is better match
                if sim >= self.similarity_threshold:
                    if sim > best_sim:
                        best_sim = sim
                        min_dist = dist_meters
                        best_match = master

        return best_match, min_dist, best_sim

    def find_recurrent_issue(
        self,
        new_complaint: ComplaintRecord,
        resolved_master_tickets: List[MasterTicketRecord],
        max_days: int = 30
    ) -> Optional[Tuple[MasterTicketRecord, float]]:
        """
        Check if a complaint appears near a recently resolved master ticket within 30 days.
        Flags potential false-closure / recurrence (A6).
        """
        effective_radius = self.get_category_radius(new_complaint.department)
        now = datetime.now(timezone.utc)

        for master in resolved_master_tickets:
            if master.department != new_complaint.department:
                continue

            # Verify resolution recency
            resolved_at_str = getattr(master, "resolved_at", None) or getattr(master, "updated_at", None)
            if resolved_at_str:
                try:
                    resolved_dt = datetime.fromisoformat(resolved_at_str.replace("Z", "+00:00"))
                    if (now - resolved_dt).days > max_days:
                        continue
                except Exception:
                    pass

            dist = haversine_distance_meters(new_complaint.lat, new_complaint.lon, master.lat, master.lon)
            if dist <= effective_radius:
                return master, dist

        return None

# Global deduplicator instance
deduplicator = SemanticDeduplicator()
