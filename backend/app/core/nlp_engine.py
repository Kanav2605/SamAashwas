import re
import json
import logging
from typing import Dict, Any, Tuple
from ..models.schemas import ExtractedNLPData, UrgencyEnum
from ..config import settings

logger = logging.getLogger(__name__)

# Department definitions & keywords (English + Hinglish + Hindi + Kannada + Tamil)
CIVIC_TAXONOMY = {
    "Electrical & Streetlighting": {
        "keywords": [
            "street light", "streetlight", "light", "bulb", "pole", "khamba", "bijli", "transformer", 
            "wire", "sparking", "short circuit", "current", "fuse", "andhera", "dark", "no light",
            "band hai", "chalu nahi", "broken light", "streetlamp", "meter", "power cut",
            # Hindi
            "स्ट्रीट लाइट", "बिजली", "खंभा", "बल्ब", "तार", "करंट", "शॉर्ट सर्किट", "अंधेरा", "बिजली गुल",
            # Kannada
            "ಬೀದಿ ದೀಪ", "ದೀಪ", "ಕಂಬ", "ವಿದ್ಯುತ್", "ಕತ್ತಲೆ", "ಬೆಳಕು", "beedi deepa", "current illa", "kambha", "kattale",
            # Tamil
            "தெரு விளக்கு", "மின்சாரம்", "மின் கம்பம்", "இருட்டு", "விளக்கு", "theru vilakku", "current illai", "iruttu"
        ],
        "default_issue": "Non-functional streetlight / Electrical issue"
    },
    "Sanitation & Solid Waste": {
        "keywords": [
            "kachra", "garbage", "trash", "waste", "dustbin", "kuda", "kude", "safai", "sweeper", 
            "cleaning", "smell", "badbu", "dhalao", "dump", "plastic", "kachra gadi", "filth", 
            "litter", "animal dead", "debris", "malba",
            # Hindi
            "कचरा", "कूड़ा", "सफाई", "डस्टबिन", "बदबू", "कूड़ेदान", "कचरे", "सफाईकर्मी", "स्वच्छ भारत",
            # Kannada
            "ಕಸ", "ಕಸದ ಗಾಡಿ", "ಸ್ವಚ್ಛತೆ", "ದುರ್ವಾಸನೆ", "ತಿಪ್ಪೆ", "kasa", "kachra", "swachhata",
            # Tamil
            "குப்பை", "துப்புரவு", "நாற்றம்", "குப்பைத்தொட்டி", "kuppai", "kuppaikoodai", "natram", "sugatharam"
        ],
        "default_issue": "Garbage dump / Uncleared solid waste"
    },
    "Water Supply & Sewage": {
        "keywords": [
            "paani", "water", "pipeline", "pipe", "burst", "leak", "sewer", "sewage", "gutter", 
            "drain", "nali", "manhole", "overflow", "drainage", "clogged", "choked", "dirty water", 
            "ganda paani", "no water", "supply", "borewell", "motor", "water main",
            # Hindi
            "सीवर", "गटर", "पानी", "पाइपलाइन", "नाला", "नाली", "गंदा पानी", "मैनहोल", "जलभराव", "जल जीवन",
            # Kannada
            "ನೀರು", "ಒಳಚರಂಡಿ", "ಚರಂಡಿ", "ಕೊಳವೆ", "ನೀರು ಸರಬರಾಜು", "neeru", "charandi", "sewerage", "kandaka",
            # Tamil
            "சாக்கடை நீர்", "சாக்கடை", "கழிவுநீர்", "தண்ணீர்", "குடிநீர்", "குழாய்", "குழாய் வெடிப்பு", "thanneer", "kudineer", "saakadai", "kuzhai"
        ],
        "default_issue": "Sewage overflow / Water pipeline rupture"
    },
    "Roads & Traffic Infrastructure": {
        "keywords": [
            "pothole", "gaddha", "gaddhe", "road", "sadak", "pavement", "footpath", "tar", "divider", 
            "speed breaker", "broken road", "asphalt", "crater", "signal", "traffic light", "zebra crossing",
            "dhas gayi", "sinkhole", "road repair",
            # Hindi
            "सड़क", "गड्ढा", "गड्ढे", "खड्डा", "फुटपाथ", "रोड", "डिवाइडर", "खराब सड़क",
            # Kannada
            "ರಸ್ತೆ", "ಗುಂಡಿ", "ಹಳ್ಳ", "ಡಾಂಬರು", "ರಸ್ತೆ ಗುಂಡಿ", "rasty", "gundi", "halla", "dambaru",
            # Tamil
            "சாலை", "குழி", "பள்ளம்", "தார் சாலை", "விபத்து", "salai", "kuzhi", "pallam"
        ],
        "default_issue": "Potholes / Broken road pavement"
    },
    "Encroachment & Town Planning": {
        "keywords": [
            "illegal", "encroachment", "thela", "hawker", "illegal construction", "footpath blocked", 
            "kabza", "illegal parking", "unauthorized", "shop extended", "dukandar",
            # Hindi
            "कब्जा", "अतिक्रमण", "ठेला", "अवैध निर्माण", "अवैध पार्किंग",
            # Kannada
            "ಅತಿಕ್ರಮಣ", "ಫುಟ್‌ಪಾತ್", "ಕಬ್ಜ", "anikramana",
            # Tamil
            "ஆக்கிரமிப்பு", "நடைபாதை", "aakkiramippu", "nadaipaathai"
        ],
        "default_issue": "Unauthorized footpath encroachment"
    },
    "Health & Vector Control": {
        "keywords": [
            "mosquito", "macchar", "fogging", "dengue", "malaria", "stagnant water", "waterlogging", 
            "insect", "spraying", "larvae", "fever outbreak",
            # Hindi
            "मच्छर", "डेंगू", "मलेरिया", "दवा का छिड़काव", "फॉगिंग", "कीटनाशक",
            # Kannada
            "ಸೊಳ್ಳೆ", "ಡೆಂಗ್ಯೂ", "ಮಲೇರಿಯಾ", "ಔಷಧಿ ಸಿಂಪಡಣೆ", "solle", "dengue",
            # Tamil
            "கொசு", "டெங்கு", "மருந்து தெளிப்பு", "kosu", "marundhu thelippu"
        ],
        "default_issue": "Stagnant water mosquito breeding / Fogging required"
    }
}

URGENCY_KEYWORDS = {
    UrgencyEnum.CRITICAL: [
        "accident", "sparking", "fire", "danger", "dangerous", "emergency", "current lag raha", 
        "khatra", "open manhole", "deep crater", "pipeline burst", "flooded inside home",
        "ಅಪಘಾತ", "ತುರ್ತು", "ವಿದ್ಯುತ್ ಆಘಾತ", "ಪ್ರಾಣಾಪಾಯ", "விபத்து", "அவசரம்", "உயிர்க்கொல்லி"
    ],
    UrgencyEnum.HIGH: [
        "urgent", "immediately", "jaldi", "severe", "overflowing badly", "4 din se", "5 din se", 
        "week", "hafta", "choked", "bad smell", "impassable", "main road", "traffic jam",
        "ಬೇಗ", "ತಕ್ಷಣ", "ದುರ್ವಾಸನೆ", "உடனடியாக", "விரைவாக", "கடுமையான"
    ],
    UrgencyEnum.MEDIUM: [
        "kal se", "yesterday", "2 din se", "repair", "band hai", "kachra", "pothole", "problem", "issue",
        "ಸಮಸ್ಯೆ", "ಸರಿಮಾಡಿ", "பிரச்சனை", "பழுது"
    ],
    UrgencyEnum.LOW: [
        "minor", "request", "please paint", "suggestion", "dim light", "ಕಡಿಮೆ", "கோரிக்கை"
    ]
}

def detect_language(text: str) -> str:
    """
    Classify whether input is English, Hindi (Devanagari), Kannada, Tamil, or Hinglish.
    """
    # 1. Kannada script: \u0C80 - \u0CFF
    kannada_count = len(re.findall(r'[\u0C80-\u0CFF]', text))
    if kannada_count > 3:
        return "Kannada"

    # 2. Tamil script: \u0B80 - \u0BFF
    tamil_count = len(re.findall(r'[\u0B80-\u0BFF]', text))
    if tamil_count > 3:
        return "Tamil"

    # 3. Devanagari script: \u0900 - \u097F
    devanagari_count = len(re.findall(r'[\u0900-\u097F]', text))
    if devanagari_count > 3:
        return "Hindi (Devanagari)"

    # 4. Hinglish detection via romanized markers
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
KANNADA_DIGITS = {'೦': '0', '೧': '1', '೨': '2', '೩': '3', '೪': '4', '೫': '5', '೬': '6', '೭': '7', '೮': '8', '೯': '9'}
TAMIL_DIGITS = {'௦': '0', '௧': '1', '௨': '2', '௩': '3', '௪': '4', '௫': '5', '௬': '6', '௭': '7', '௮': '8', '௯': '9'}

def extract_ward(text: str) -> str:
    """
    Extract ward number or identifier from complaint text in English, Hindi, Kannada, or Tamil.
    E.g., 'Ward 7', 'ward no. 12', 'ward #3', 'W-04', 'वार्ड 5', 'ಪ್ರಭಾಗ ೧೨', 'வார்டு 4'
    """
    ward_patterns = [
        r'(?:ward|wrd|prabhag|ವಾರ್ಡ್|ಪ್ರಭಾಗ|வார்டு|வட்டம்|वार्ड|प्रभाग)\s*(?:no\.?|number|संख्या|ಸಂಖ್ಯೆ|எண்|#)?\s*([0-9०-९೦-೯௦-௯]{1,3}[A-Za-z]?)',
        r'\bW-?([0-9]{1,3})\b',
        r'\bsector\s*([0-9]{1,3})\b'
    ]
    for pattern in ward_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            raw_val = match.group(1)
            for h, d in HINDI_DIGITS.items():
                raw_val = raw_val.replace(h, d)
            for k, d in KANNADA_DIGITS.items():
                raw_val = raw_val.replace(k, d)
            for t, d in TAMIL_DIGITS.items():
                raw_val = raw_val.replace(t, d)
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

    # 2. Hindi/Vernacular post-position phrases: [Landmark] ke paas / nazdeek / ke samne / hattira / arugil
    post_pattern = r'([A-Za-z0-9\s\.\-]{3,30}?)\s+(?:ke paas|nazdeek|ke samne|ke peeche|hattira|arugil)\b'
    match_post = re.search(post_pattern, text, re.IGNORECASE)
    if match_post:
        cand = match_post.group(1).strip()
        cand = re.sub(r'^(?:bhaiya|yeh|woh|sadak|road|mein|par|pe|pada|giri|hua|hai)\s+', '', cand, flags=re.IGNORECASE).strip()
        if len(cand) > 3:
            return cand.title()

    # 3. Specific named intersections / roads: e.g., '27th Main', 'Gandhi Chowk'
    named_pattern = r'\b([0-9A-Za-z\s]{2,25}?\s+(?:chowk|circle|cross|main|layout|colony|nagar|marg|bhavan|temple|masjid|church))\b'
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
            if kw.lower() in lower_text:
                score += (3 if " " in kw else 1) # Higher weight for multi-word match
        scores[dept] = score

    best_dept = max(scores, key=scores.get)
    max_score = scores[best_dept]

    if max_score == 0:
        return "Sanitation & Solid Waste", "General Civic Grievance", 0.50

    confidence = min(0.98, 0.65 + (max_score * 0.08))
    default_issue = CIVIC_TAXONOMY[best_dept]["default_issue"]

    # Finer issue extraction based on prominent keywords across languages
    if any(k in lower_text for k in ["pothole", "gaddha", "gaddhe", "ಗುಂಡಿ", "குழி", "halla", "pallam"]):
        issue_type = "Severe Potholes / Road Surface Breakdown"
    elif any(k in lower_text for k in ["street light", "khamba", "light band", "ದೀಪ", "ಕಂಬ", "விளக்கு", "மின்கம்பம்"]):
        issue_type = "Non-functional Streetlight / Dark Spot"
    elif any(k in lower_text for k in ["sewer", "gutter", "overflow", "ಗಟರ್", "ಚರಂಡಿ", "சாக்கடை"]):
        issue_type = "Sewer Line Overflow & Blockage"
    elif any(k in lower_text for k in ["pipeline", "pipe", "paani", "ನೀರು", "தண்ணீர்", "குடிநீர்"]):
        issue_type = "Potable Water Pipeline Rupture / Leak"
    elif any(k in lower_text for k in ["kachra", "garbage", "kuda", "ಕಸ", "குப்பை"]):
        issue_type = "Garbage Pile-up / Waste Clearance"
    elif any(k in lower_text for k in ["thela", "encroachment", "kabza", "ಅತಿಕ್ರಮಣ", "ஆக்கிரமிப்பு"]):
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
            if kw.lower() in lower_text:
                return level
    return UrgencyEnum.MEDIUM

def get_national_mission_and_sla(department: str, urgency: UrgencyEnum) -> Tuple[str, int]:
    """
    Maps grievances to Flagship Indian Civic Missions and Citizen Charter SLA hours.
    """
    if department == "Sanitation & Solid Waste":
        return "Swachh Bharat Mission (SBM-Urban 2.0)", 24
    elif department == "Water Supply & Sewage":
        sla = 12 if urgency == UrgencyEnum.CRITICAL else (24 if urgency == UrgencyEnum.HIGH else 48)
        return "AMRUT 2.0 & Jal Jeevan Mission", sla
    elif department == "Electrical & Streetlighting":
        sla = 12 if urgency == UrgencyEnum.CRITICAL else 48
        return "Smart Cities Mission / National Street Lighting Program", sla
    elif department == "Roads & Traffic Infrastructure":
        sla = 24 if urgency == UrgencyEnum.CRITICAL else 72
        return "State PWD & Municipal Road Safety Program", sla
    elif department == "Health & Vector Control":
        return "National Vector Borne Disease Control / SBM Urban Health", 24
    else:
        return "Smart Cities Urban Land Modernization", 96

class CivicNLPEngine:
    """
    Core NLP Engine capable of zero-shot parsing, entity extraction,
    and Hindi / Hinglish / Kannada / Tamil / English classification for Indian municipal grievances.
    """
    def __init__(self):
        self.backend = settings.NLP_MODEL_BACKEND

    def analyze(self, raw_text: str) -> ExtractedNLPData:
        lang = detect_language(raw_text)
        dept, issue, conf = extract_department_and_issue(raw_text)
        ward = extract_ward(raw_text)
        landmark = extract_landmark(raw_text)
        urgency = extract_urgency(raw_text)
        mission, sla = get_national_mission_and_sla(dept, urgency)

        return ExtractedNLPData(
            department=dept,
            issue_type=issue,
            urgency=urgency,
            location_landmark=landmark,
            ward_extracted=ward,
            language_detected=lang,
            confidence=conf,
            national_mission=mission,
            citizen_charter_sla_hours=sla
        )

# Global engine singleton
nlp_engine = CivicNLPEngine()
