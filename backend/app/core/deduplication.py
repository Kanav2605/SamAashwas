import math
import re
import logging
from typing import List, Tuple, Optional, Dict, Any
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from ..models.domain import ComplaintRecord, MasterTicketRecord
from ..utils.geo_utils import haversine_distance_meters
from ..config import settings

logger = logging.getLogger(__name__)

STOP_WORDS = {
    'bhaiya', 'hai', 'ho', 'raha', 'rahi', 'gaya', 'gayi', 'mein', 'par', 'pe', 'se', 'yeh', 'woh', 
    'ko', 'ka', 'ki', 'ke', 'the', 'is', 'a', 'an', 'in', 'on', 'at', 'for', 'of', 'to', 'and', 
    'since', 'been', 'it', 'this', 'that', 'are', 'am', 'was', 'were', 'near', 'neer', 'local', 'vicinity'
}

SYNONYMS = {
    'dead': 'band', 'broken': 'band', 'closed': 'band', 'kharab': 'band', 'phuta': 'burst', 'phat': 'burst',
    'days': 'din', 'day': 'din',
    'sewer': 'gutter', 'sewage': 'gutter', 'drain': 'gutter', 'drainage': 'gutter', 'nali': 'gutter',
    'road': 'sadak', 'street': 'sadak', 'rasta': 'sadak',
    'kachra': 'garbage', 'kuda': 'garbage', 'waste': 'garbage', 'trash': 'garbage',
    'paani': 'water', 'pipe': 'pipeline', 'overflowing': 'overflow', 'potholes': 'pothole', 'gaddha': 'pothole', 'gaddhe': 'pothole'
}

def _normalize_tokens(text: str) -> List[str]:
    words = re.findall(r'[a-zA-Z0-9]+', text.lower())
    return [SYNONYMS.get(w, w) for w in words if w not in STOP_WORDS]

class SemanticDeduplicator:
    """
    Spatio-Temporal Deduplication Engine.
    Combines geographic distance gating (default 300m) with semantic text cosine
    similarity to cluster redundant grievances into Master Incidents.
    """

    def __init__(
        self,
        radius_meters: float = settings.DEDUPLICATION_RADIUS_METERS,
        similarity_threshold: float = settings.DEDUPLICATION_SIMILARITY_THRESHOLD
    ):
        self.radius_meters = radius_meters
        self.similarity_threshold = similarity_threshold

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

    def find_matching_master_ticket(
        self,
        new_complaint: ComplaintRecord,
        active_master_tickets: List[MasterTicketRecord]
    ) -> Tuple[Optional[MasterTicketRecord], float, float]:
        """
        Searches active master tickets for a matching incident.
        Returns: (matching_master_ticket, distance_meters, similarity_score)
        """
        best_match = None
        best_sim = 0.0
        min_dist = float("inf")

        for master in active_master_tickets:
            # Only compare tickets within the same department
            if master.department != new_complaint.department:
                continue

            # Only compare open or in-progress tickets
            if master.status in ["RESOLVED", "REJECTED"]:
                continue

            # 1. Geographic Gate Check
            dist_meters = haversine_distance_meters(
                new_complaint.lat,
                new_complaint.lon,
                master.lat,
                master.lon
            )

            if dist_meters <= self.radius_meters:
                # 2. Semantic Similarity Check against the master ticket title and existing reports
                sim = self.compute_text_similarity(new_complaint.raw_text, master.title)

                # Compare against any previous citizen reports attached to this master
                for report in master.citizen_reports[:5]:
                    report_sim = self.compute_text_similarity(new_complaint.raw_text, report.get("raw_text", ""))
                    if report_sim > sim:
                        sim = report_sim

                # If same issue type or landmark match, boost confidence within the 300m radius
                if new_complaint.issue_type and master.issue_type and new_complaint.issue_type.lower() == master.issue_type.lower():
                    sim = min(1.0, sim + 0.10)
                if (
                    new_complaint.location_landmark 
                    and new_complaint.location_landmark.lower() != "local vicinity"
                    and new_complaint.location_landmark.lower() in master.title.lower()
                ):
                    sim = min(1.0, sim + 0.10)

                # If exceeds similarity threshold and closer or better match
                if sim >= self.similarity_threshold:
                    if sim > best_sim:
                        best_sim = sim
                        min_dist = dist_meters
                        best_match = master

        return best_match, min_dist, best_sim

# Global deduplicator instance
deduplicator = SemanticDeduplicator()
