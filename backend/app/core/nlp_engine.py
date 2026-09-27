import re
import json
import logging
from typing import Dict, Any, Tuple
from ..models.schemas import ExtractedNLPData, UrgencyEnum
from ..config import settings

logger = logging.getLogger(__name__)

# Department definitions & keywords (English + Hinglish + Hindi Romanized)
CIVIC_TAXONOMY = {
    "Electrical & Streetlighting": {
        "keywords": [
            "street light", "streetlight", "light", "bulb", "pole", "khamba", "bijli", "transformer", 
            "wire", "sparking", "short circuit", "current", "fuse", "andhera", "dark", "no light",
            "band hai", "chalu nahi", "broken light", "streetlamp", "meter", "power cut",
            "स्ट्रीट लाइट", "बिजली", "खंभा", "बल्ब", "तार", "करंट", "शॉर्ट सर्किट", "अंधेरा"
        ],
        "default_issue": "Non-functional streetlight / Electrical issue"
    },
    "Sanitation & Solid Waste": {
        "keywords": [
            "kachra", "garbage", "trash", "waste", "dustbin", "kuda", "kude", "safai", "sweeper", 
            "cleaning", "smell", "badbu", "dhalao", "dump", "plastic", "kachra gadi", "filth", 
            "litter", "animal dead", "debris", "malba",
            "कचरा", "कूड़ा", "सफाई", "डस्टबिन", "बदबू", "कूड़ेदान", "कचरे", "सफाईकर्मी"
        ],
        "default_issue": "Garbage dump / Uncleared solid waste"
    },
    "Water Supply & Sewage": {
        "keywords": [
            "paani", "water", "pipeline", "pipe", "burst", "leak", "sewer", "sewage", "gutter", 
            "drain", "nali", "manhole", "overflow", "drainage", "clogged", "choked", "dirty water", 
            "ganda paani", "no water", "supply", "borewell", "motor", "water main",
            "सीवर", "गटर", "पानी", "पाइपलाइन", "नाला", "नाली", "गंदा पानी", "मैनहोल", "जलभराव"
        ],
        "default_issue": "Sewage overflow / Water pipeline rupture"
    },
    "Roads & Traffic Infrastructure": {
        "keywords": [
            "pothole", "gaddha", "gaddhe", "road", "sadak", "pavement", "footpath", "tar", "divider", 
            "speed breaker", "broken road", "asphalt", "crater", "signal", "traffic light", "zebra crossing",
            "dhas gayi", "sinkhole", "road repair",
            "सड़क", "गड्ढा", "गड्ढे", "खड्डा", "फुटपाथ", "रोड", "डिवाइडर"
        ],
        "default_issue": "Potholes / Broken road pavement"
    },
    "Encroachment & Town Planning": {
        "keywords": [
            "illegal", "encroachment", "thela", "hawker", "illegal construction", "footpath blocked", 
            "kabza", "illegal parking", "unauthorized", "shop extended", "dukandar",
            "कब्जा", "अतिक्रमण", "ठेला", "अवैध निर्माण", "अवैध पार्किंग"
        ],
        "default_issue": "Unauthorized footpath encroachment"
    },
    "Health & Vector Control": {
        "keywords": [
            "mosquito", "macchar", "fogging", "dengue", "malaria", "stagnant water", "waterlogging", 
            "insect", "spraying", "larvae", "fever outbreak",
            "मच्छर", "डेंगू", "मलेरिया", "दवा का छिड़काव", "फॉगिंग", "कीटनाशक"
        ],
        "default_issue": "Stagnant water mosquito breeding / Fogging required"
    }
}

URGENCY_KEYWORDS = {
    UrgencyEnum.CRITICAL: [
        "accident", "sparking", "fire", "danger", "dangerous", "emergency", "current lag raha", 
        "khatra", "open manhole", "deep crater", "pipeline burst", "flooded inside home"
    ],
    UrgencyEnum.HIGH: [
        "urgent", "immediately", "jaldi", "severe", "overflowing badly", "4 din se", "5 din se", 
        "week", "hafta", "choked", "bad smell", "impassable", "main road", "traffic jam"
    ],
    UrgencyEnum.MEDIUM: [
        "kal se", "yesterday", "2 din se", "repair", "band hai", "kachra", "pothole", "problem", "issue"
    ],
    UrgencyEnum.LOW: [
        "minor", "request", "please paint", "suggestion", "dim light"
    ]
}

def detect_language(text: str) -> str:
    """
    Classify whether input is English, Hindi (Devanagari), or Hinglish (Romanized Hindi-English).
    """
    devanagari_count = len(re.findall(r'[\u0900-\u097F]', text))
    if devanagari_count > 4:
        return "Hindi (Devanagari)"

    hinglish_markers = [
        "hai", "ho", "raha", "rahi", "gaya", "mein", "pe", "par", "bhaiya", "yeh", "woh", 
        "nahi", "aayi", "aaya", "kripya", "jaldi", "bohot", "bada", "gaddha", "paani", 
        "sadak", "kachra", "kuda", "safai", "wali", "wala", "chalu", "band"
    ]
    words = [w.lower() for w in re.findall(r'\b[a-zA-Z]+\b', text)]
    match_count = sum(1 for w in words if w in hinglish_markers)

    if match_count >= 1:
        return "Hinglish"
    return "English"

HINDI_DIGITS = {'०': '0', '१': '1', '२': '2', '३': '3', '४': '4', '५': '5', '६': '6', '७': '7', '८': '8', '९': '9'}

def extract_ward(text: str) -> str:
    """
    Extract ward number or identifier from complaint text in English or Hindi.
    E.g., 'Ward 7', 'ward no. 12', 'ward #3', 'W-04', 'वार्ड 5', 'प्रभाग १२'
    """
    ward_patterns = [
        r'(?:ward|wrd|prabhag|वार्ड|प्रभाग)\s*(?:no\.?|number|संख्या|#)?\s*([0-9०-९]{1,3}[A-Za-z]?)',
        r'\bW-?([0-9]{1,3})\b',
        r'\bsector\s*([0-9]{1,3})\b'
    ]
    for pattern in ward_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            raw_val = match.group(1)
            for h, d in HINDI_DIGITS.items():
                raw_val = raw_val.replace(h, d)
            return f"Ward {raw_val.upper()}"
    return "Unassigned Ward (Auto-Geo)"

def extract_landmark(text: str) -> str:
    """
    Extract location landmarks such as 'near Sharma General Store', 'opposite metro station',
    'Gandhi Chowk ke paas', '27th Main'.
    """
    # 1. Explicit prepositional phrases: near, opposite, behind, beside, in front of, etc.
    prep_pattern = r'\b(?:near|opp\.?|opposite|behind|in front of|front of|beside|across|close to|next to)\s+([A-Za-z0-9\s\.\-]{3,40}?)(?=(?:,|\.|\bward\b|\bphone\b|\burgent\b|$))'
    match = re.search(prep_pattern, text, re.IGNORECASE)
    if match:
        landmark = match.group(1).strip()
        if len(landmark) > 3:
            return landmark.title()

    # 2. Hindi post-position phrases: [Landmark] ke paas / nazdeek / ke samne
    post_pattern = r'([A-Za-z0-9\s\.\-]{3,30}?)\s+(?:ke paas|nazdeek|ke samne|ke peeche)\b'
    match_post = re.search(post_pattern, text, re.IGNORECASE)
    if match_post:
        cand = match_post.group(1).strip()
        cand = re.sub(r'^(?:bhaiya|yeh|woh|sadak|road|mein|par|pe|pada|giri|hua|hai)\s+', '', cand, flags=re.IGNORECASE).strip()
        if len(cand) > 3:
            return cand.title()

    # 3. Specific named intersections / roads: e.g., '27th Main', 'Gandhi Chowk'
    named_pattern = r'\b([0-9A-Za-z\s]{2,25}?\s+(?:chowk|circle|cross|main|layout|colony|nagar|marg))\b'
    match2 = re.search(named_pattern, text, re.IGNORECASE)
    if match2:
        cand2 = match2.group(1).strip()
        cand2 = re.sub(r'^(?:bhaiya|yeh|woh|sadak|road|mein|par|pe|pada)\s+', '', cand2, flags=re.IGNORECASE).strip()
        if len(cand2) > 3:
            return cand2.title()

    return "Local Vicinity"

def extract_department_and_issue(text: str) -> Tuple[str, str, float]:
    """
    Determine the responsible municipal department and specific issue using keyword scoring.
    """
    lower_text = text.lower()
    scores = {}
    
    for dept, data in CIVIC_TAXONOMY.items():
        score = 0
        for kw in data["keywords"]:
            if kw in lower_text:
                score += (3 if " " in kw else 1) # Higher weight for multi-word match
        scores[dept] = score

    best_dept = max(scores, key=scores.get)
    max_score = scores[best_dept]

    if max_score == 0:
        return "Sanitation & Solid Waste", "General Civic Grievance", 0.50

    confidence = min(0.98, 0.65 + (max_score * 0.08))
    default_issue = CIVIC_TAXONOMY[best_dept]["default_issue"]

    # Finer issue extraction based on prominent keywords
    if "pothole" in lower_text or "gaddha" in lower_text:
        issue_type = "Severe Potholes / Road Surface Breakdown"
    elif "street light" in lower_text or "khamba" in lower_text or "light band" in lower_text:
        issue_type = "Non-functional Streetlight / Dark Spot"
    elif "sewer" in lower_text or "gutter" in lower_text or "overflow" in lower_text:
        issue_type = "Sewer Line Overflow & Blockage"
    elif "pipeline" in lower_text or "pipe" in lower_text or "paani" in lower_text:
        issue_type = "Potable Water Pipeline Rupture / Leak"
    elif "kachra" in lower_text or "garbage" in lower_text or "kuda" in lower_text:
        issue_type = "Garbage Pile-up / Waste Clearance"
    elif "thela" in lower_text or "encroachment" in lower_text or "kabza" in lower_text:
        issue_type = "Illegal Footpath & Road Encroachment"
    else:
        issue_type = default_issue

    return best_dept, issue_type, round(confidence, 2)

def extract_urgency(text: str) -> UrgencyEnum:
    """
    Evaluate urgency level based on safety hazards, duration, and keywords.
    """
    lower_text = text.lower()
    for level, keywords in URGENCY_KEYWORDS.items():
        for kw in keywords:
            if kw in lower_text:
                return level
    return UrgencyEnum.MEDIUM

class CivicNLPEngine:
    """
    Core NLP Engine capable of zero-shot parsing, entity extraction,
    and Hinglish/Hindi classification for municipal grievances.
    """
    def __init__(self):
        self.backend = settings.NLP_MODEL_BACKEND

    def analyze(self, raw_text: str) -> ExtractedNLPData:
        lang = detect_language(raw_text)
        dept, issue, conf = extract_department_and_issue(raw_text)
        ward = extract_ward(raw_text)
        landmark = extract_landmark(raw_text)
        urgency = extract_urgency(raw_text)

        return ExtractedNLPData(
            department=dept,
            issue_type=issue,
            urgency=urgency,
            location_landmark=landmark,
            ward_extracted=ward,
            language_detected=lang,
            confidence=conf
        )

# Global engine singleton
nlp_engine = CivicNLPEngine()
