import re
import json
import logging
from typing import Dict, Any, Tuple, List, Optional
from ..models.schemas import ExtractedNLPData, UrgencyEnum
from ..config import settings

logger = logging.getLogger(__name__)

# Comprehensive Civic Taxonomy across Tier-1 Indian Languages:
# English, Hinglish, Hindi, Kannada, Tamil, Telugu, Bengali, Urdu, Punjabi, Marathi
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
            "தெரு விளக்கு", "மின்சாரம்", "மின் கம்பம்", "இருட்டு", "விளக்கு", "theru vilakku", "current illai", "iruttu",
            # Telugu
            "వీధి దీపం", "దీపం", "స్తంభం", "విద్యుత్", "చీకటి", "veedhi deepam", "current ledu", "stambham",
            # Bengali
            "পথবাতি", "বিদ্যুৎ", "আলো", "অন্ধকার", "khamba", "light nei", "pothobati",
            # Urdu
            "اسٹریٹ لائٹ", "بجلی", "کھمبا", "اندھیرا", "bijli gul", "khamba tuta",
            # Punjabi
            "ਸਟ੍ਰੀਟ ਲਾਈਟ", "ਬਿਜਲੀ", "ਖੰਭਾ", "ਹਨੇਰਾ", "bijli khamba", "light band",
            # Marathi
            "पथदिवा", "लाईट", "खांब", "विद्युत", "अंधार"
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
            "குப்பை", "துப்புரவு", "நாற்றம்", "குப்பைத்தொட்டி", "kuppai", "kuppaikoodai", "natram", "sugatharam",
            # Telugu
            "చెత్త", "చెత్త బుట్ట", "పరిశుభ్రత", "దుర్వాసన", "chetta", "chetta gadi", "swachhata",
            # Bengali
            "আবর্জনা", "ময়লা", "নোংরা", "ডাস্টবিন", "moyla", "aborjona",
            # Urdu
            "کوڑا", "صفائی", "بدبو", "کچرا", "kuda karkat", "safai nahi",
            # Punjabi
            "ਕੂੜਾ", "ਸਫਾਈ", "ਬਦਬੂ", "kooda", "safai sewak", "gandagi",
            # Marathi
            "कचरा", "घाण", "स्वच्छता", "डस्टबिन", "कचराकुंडी"
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
            "சாக்கடை நீர்", "சாக்கடை", "கழிவுநீர்", "தண்ணீர்", "குடிநீர்", "குழாய்", "குழாய் வெடிப்பு", "thanneer", "kudineer", "saakadai", "kuzhai",
            # Telugu
            "నీరు", "మురుగునీరు", "పైప్ లైన్", "కాలువ", "neeru", "muruguneeru", "drainage overflow",
            # Bengali
            "জল", "নর্দমা", "ড্রেন", "পাইপ", "jol nei", "drain block", "sewer",
            # Urdu
            "سیوریج", "گٹر", "پانی", "نالہ", "gutter ubal raha", "pani nahi aa raha",
            # Punjabi
            "ਪਾਣੀ", "ਸੀਵਰੇਜ", "ਨਾਲਾ", "ਗਟਰ", "paani khada", "sewerage block",
            # Marathi
            "पाणी", "गटार", "सांडपाणी", "पाईपलाईन", "नाला", "घाण पाणी"
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
            "சாலை", "குழி", "பள்ளம்", "தார் சாலை", "விபத்து", "salai", "kuzhi", "pallam",
            # Telugu
            "రహదారి", "గుంత", "రోడ్డు", "పాదచారుల మార్గం", "gunta", "road guntalu", "road repair",
            # Bengali
            "রাস্তা", "গর্ত", "ভাঙা রাস্তা", "gorto", "broken road", "rasta",
            # Urdu
            "سڑک", "گڑھا", "خراب سڑک", "sadak tuti", "gaddhe",
            # Punjabi
            "ਸੜਕ", "ਟੋਆ", "ਟੋਏ", "sadak te toye", "khadde",
            # Marathi
            "रस्ता", "खड्डे", "खड्डा", "फुटपाथ", "रस्ता दुरुस्ती"
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
            "ஆக்கிரமிப்பு", "நடைபாதை", "aakkiramippu", "nadaipaathai",
            # Telugu
            "ఆక్రమణ", "ఫుట్‌పాత్ ఆక్రమణ", "aakramana",
            # Bengali
            "জবরদখল", "দোকান বাড়িয়ে নেওয়া", "jabor dokhol",
            # Urdu
            "تجاوزات", "قبضہ", "najayaz kabza",
            # Punjabi
            "ਨਾਜਾਇਜ਼ ਕਬਜ਼ਾ", "kabza", "illegal thela",
            # Marathi
            "अतिक्रमण", "बेकायदेशीर", "कब्जा"
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
            "கொசு", "டெங்கு", "மருந்து தெளிப்பு", "kosu", "marundhu thelippu",
            # Telugu
            "దోమలు", "డెంగ్యూ", "మలేరియా", "domalu", "fogging cheyandi",
            # Bengali
            "মশা", "ডেঙ্গু", "ম্যালেরিয়া", "mosha", "dengue",
            # Urdu
            "مچھر", "ڈینگی", "ملیریا", "machhar mar dawa",
            # Punjabi
            "ਮੱਛਰ", "ਡੈਂਗੂ", "ਮਲੇਰੀਆ", "machhar",
            # Marathi
            "डास", "डेंग्यू", "मलेरिया", "फवारणी"
        ],
        "default_issue": "Stagnant water mosquito breeding / Fogging required"
    }
}

URGENCY_KEYWORDS = {
    UrgencyEnum.CRITICAL: [
        "accident", "sparking", "fire", "danger", "dangerous", "emergency", "current lag raha", 
        "khatra", "open manhole", "deep crater", "pipeline burst", "flooded inside home",
        "ಅಪಘಾತ", "ತುರ್ತು", "ವಿದ್ಯುತ್ ಆಘಾತ", "ಪ್ರಾಣಾಪಾಯ", "விபத்து", "அவசரம்", "உயிர்க்கொல்லி",
        "ప్రమాదం", "ತುರ್ತು", "বিপদ", "জরুরি", "خطرا", "ਹਾਦਸਾ", "जीवघेणा"
    ],
    UrgencyEnum.HIGH: [
        "urgent", "immediately", "jaldi", "severe", "overflowing badly", "4 din se", "5 din se", 
        "week", "hafta", "choked", "bad smell", "impassable", "main road", "traffic jam",
        "ಬೇಗ", "ತಕ್ಷಣ", "ದುರ್ವಾಸನೆ", "உடனடியாக", "விரைவாக", "கடுமையான",
        "త్వరగా", "তাড়াতাড়ি", "جلد", "ਜਲਦੀ", "तात्काळ"
    ],
    UrgencyEnum.MEDIUM: [
        "kal se", "yesterday", "2 din se", "repair", "band hai", "kachra", "pothole", "problem", "issue",
        "ಸಮಸ್ಯೆ", "ಸರಿಮಾಡಿ", "பிரச்சனை", "பழுது", "సమస్య", "সমস্যা", "ਮਸਲਾ"
    ],
    UrgencyEnum.LOW: [
        "minor", "request", "please paint", "suggestion", "dim light", "ಕಡಿಮೆ", "கோரிக்கை", "విన్నపం"
    ]
}

# Negation tokens for context window suppression (±3 tokens)
NEGATION_TOKENS = {
    # English
    "not", "no", "never", "none", "neither", "isnt", "isn't", "arent", "aren't", "wont", "won't", "clear", "fixed", "clean",
    # Hindi / Hinglish / Urdu
    "nahi", "nahin", "na", "mat", "nhi", "thik", "theek", "sudhar", "solve", "hata", "dur", "saaf",
    # Kannada
    "illa", "alla", "sari",
    # Tamil
    "illai", "illadha", "sari",
    # Telugu
    "ledu", "kaadu", "ledu",
    # Bengali
    "na", "noy", "nei",
    # Punjabi
    "nahi", "ni", "theek",
    # Marathi
    "नाही", "नको", "झाले"
}

# Non-ULB "Wrong Door" Jurisdictions
WRONG_DOOR_PATTERNS = [
    {
        "jurisdiction": "NHAI (National Highways Authority of India)",
        "regex": r"\b(nh[- ]?\d+|national highway|toll plaza|expressway|nhai)\b",
        "advice": "This arterial highway falls under NHAI jurisdiction. Please report via the 'Rajmargyatra' app or NHAI 24x7 helpline 1033."
    },
    {
        "jurisdiction": "Indian Railways",
        "regex": r"\b(railway track|railway platform|train station|railway crossing|railway siding|irctc|railway bridge)\b",
        "advice": "This asset is within Indian Railways boundary. Please lodge directly on RailMadad (railmadad.indianrailways.gov.in or dial 139)."
    },
    {
        "jurisdiction": "State Power Transmission Grid / DISCOM High Tension",
        "regex": r"\b(high tension grid|132\s*kv|66\s*kv|grid substation|state grid blackout|power grid collapse)\b",
        "advice": "High-tension transmission lines and major substation grid collapses fall under State Power Transmission (DISCOM/Transco). Call DISCOM central helpline 1912."
    },
    {
        "jurisdiction": "Cantonment Board / Ministry of Defence",
        "regex": r"\b(cantonment|cantt|military camp|army area|defence estate)\b",
        "advice": "This location is within a Military Cantonment Board area. Please submit via Directorate General Defence Estates (DGDE) portal."
    }
]

def check_wrong_door_jurisdiction(text: str) -> Optional[Dict[str, str]]:
    """
    Detect if the grievance falls under external jurisdiction (NHAI, Railways, DISCOM, Cantonment).
    """
    for entry in WRONG_DOOR_PATTERNS:
        if re.search(entry["regex"], text, re.IGNORECASE):
            return {
                "jurisdiction": entry["jurisdiction"],
                "advice": entry["advice"]
            }
    return None

def detect_language(text: str) -> str:
    """
    Classify whether input is English, Hindi, Kannada, Tamil, Telugu, Bengali, Urdu, Punjabi, Marathi, or Hinglish.
    """
    telugu_count = len(re.findall(r'[\u0C00-\u0C7F]', text))
    bengali_count = len(re.findall(r'[\u0980-\u09FF]', text))
    urdu_count = len(re.findall(r'[\u0600-\u06FF]', text))
    punjabi_count = len(re.findall(r'[\u0A00-\u0A7F]', text))
    kannada_count = len(re.findall(r'[\u0C80-\u0CFF]', text))
    tamil_count = len(re.findall(r'[\u0B80-\u0BFF]', text))
    devanagari_count = len(re.findall(r'[\u0900-\u097F]', text))

    counts = {
        "Telugu": telugu_count,
        "Bengali": bengali_count,
        "Urdu": urdu_count,
        "Punjabi": punjabi_count,
        "Kannada": kannada_count,
        "Tamil": tamil_count,
        "Hindi (Devanagari)": devanagari_count
    }

    max_lang, max_c = max(counts.items(), key=lambda x: x[1])
    if max_c > 0:
        if max_lang == "Hindi (Devanagari)":
            # Check Marathi markers
            marathi_markers = ["आहे", "नाही", "रस्ता", "पाणी", "कचरा", "झाले", "झाला"]
            if any(m in text for m in marathi_markers):
                return "Marathi"
        return max_lang

    # Hinglish and Romanized Indic detection via markers
    hinglish_markers = [
        "hai", "ho", "raha", "rahi", "gaya", "mein", "pe", "par", "bhaiya", "yeh", "woh", 
        "nahi", "aayi", "aaya", "kripya", "jaldi", "bohot", "bada", "gaddha", "paani", 
        "sadak", "kachra", "kuda", "safai", "wali", "wala", "chalu", "band", "khamba",
        "bijli", "dost", "samasya", "thik", "karo", "khatra", "gande", "sharma"
    ]
    indic_roman_markers = [
        "beedi", "deepa", "kambha", "kattale", "kasa", "thumbide", "neeru", "charandi",
        "rasty", "gundi", "halla", "biddide", "theru", "vilakku", "iruttu", "kuppai",
        "thanneer", "saakadai", "kuzhi", "pallam", "salai", "chetta", "veedhi", "stambham",
        "rasta", "moyla", "aborjona", "kooda", "toye"
    ]
    words = [w.lower() for w in re.findall(r'\b[a-zA-Z]+\b', text)]
    match_count = sum(1 for w in words if w in hinglish_markers or w in indic_roman_markers)

    if match_count >= 1:
        return "Hinglish"
    return "English"

HINDI_DIGITS = {'०': '0', '१': '1', '२': '2', '३': '3', '४': '4', '५': '5', '६': '6', '७': '7', '८': '8', '९': '9'}
KANNADA_DIGITS = {'೦': '0', '೧': '1', '೨': '2', '೩': '3', '೪': '4', '೫': '5', '೬': '6', '೭': '7', '೮': '8', '೯': '9'}
TAMIL_DIGITS = {'௦': '0', '௧': '1', '௨': '2', '௩': '3', '௪': '4', '௫': '5', '௬': '6', '௭': '7', '௮': '8', '௯': '9'}
TELUGU_DIGITS = {'౦': '0', '౧': '1', '౨': '2', '౩': '3', '౪': '4', '౫': '5', '౬': '6', '౭': '7', '౮': '8', '౯': '9'}
BENGALI_DIGITS = {'০': '0', '১': '1', '২': '2', '৩': '3', '৪': '4', '৫': '5', '৬': '6', '৭': '7', '৮': '8', '৯': '9'}

def extract_ward(text: str) -> str:
    """
    Extract ward number or identifier from complaint text across Indian scripts.
    """
    ward_patterns = [
        r'(?:ward|wrd|w/no\.?|prabhag|ವಾರ್ಡ್|ಪ್ರಭಾಗ|வார்டு|வட்டம்|వార్డు|প্রভাগ|ਵਾਰਡ|वार्ड|प्रभाग)\s*[-:#/]?\s*(?:no\.?|number|संख्या|ಸಂಖ್ಯೆ|எண்|సంఖ్య|#)?\s*[-:#/]?\s*([0-9०-९೦-೯௦-௯౦-౯০-৯]{1,3}[A-Za-z]?)',
        r'\bW\s*[-:#/]?\s*([0-9०-९೦-೯௦-௯౦-౯০-৯]{1,3}[A-Za-z]?)\b',
        r'\bsector\s*[-:#/]?\s*([0-9०-९೦-೯௦-௯౦-౯০-৯]{1,3}[A-Za-z]?)\b'
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
            for te, d in TELUGU_DIGITS.items():
                raw_val = raw_val.replace(te, d)
            for b, d in BENGALI_DIGITS.items():
                raw_val = raw_val.replace(b, d)
            return f"Ward {raw_val.upper()}"
    return "Unassigned Ward (Auto-Geo)"

def extract_landmark(text: str) -> str:
    """
    Extract location landmarks such as 'near Sharma General Store', 'opposite metro station'.
    """
    prep_pattern = r'\b(?:near|opp\.?|opposite|behind|in front of|front of|beside|across|close to|next to)\s+([A-Za-z0-9\s\.\-]{3,40}?)(?=(?:,|\.|\bward\b|\bphone\b|\burgent\b|$))'
    match = re.search(prep_pattern, text, re.IGNORECASE)
    if match:
        landmark = match.group(1).strip()
        if len(landmark) > 3:
            return landmark.title()

    post_pattern = r'([A-Za-z0-9\s\.\-]{3,30}?)\s+(?:ke paas|nazdeek|ke samne|ke peeche|hattira|arugil|daggara|kache)\b'
    match_post = re.search(post_pattern, text, re.IGNORECASE)
    if match_post:
        cand = match_post.group(1).strip()
        cand = re.sub(r'^(?:bhaiya|yeh|woh|sadak|road|mein|par|pe|pada|giri|hua|hai)\s+', '', cand, flags=re.IGNORECASE).strip()
        if len(cand) > 3:
            return cand.title()

    named_pattern = r'\b([0-9A-Za-z\s]{2,25}?\s+(?:chowk|circle|cross|main|layout|colony|nagar|marg|bhavan|temple|masjid|church))\b'
    match2 = re.search(named_pattern, text, re.IGNORECASE)
    if match2:
        cand2 = match2.group(1).strip()
        cand2 = re.sub(r'^(?:bhaiya|yeh|woh|sadak|road|mein|par|pe|pada)\s+', '', cand2, flags=re.IGNORECASE).strip()
        if len(cand2) > 3:
            return cand2.title()

    return "Local Vicinity"

def is_match_negated(text_tokens: List[str], match_start_idx: int, match_end_idx: int, window: int = 5) -> bool:
    """
    Check if any negation token falls within a window of +/- 5 tokens around the matched keyword.
    """
    left_bound = max(0, match_start_idx - window)
    right_bound = min(len(text_tokens), match_end_idx + window + 1)
    surrounding = text_tokens[left_bound:right_bound]
    for token in surrounding:
        if token.lower() in NEGATION_TOKENS:
            return True
    return False

def extract_department_and_issue(text: str) -> Tuple[str, str, float, bool]:
    """
    Determine the responsible municipal department and specific issue using keyword scoring with
    negation suppression and confidence-gated abstention (tau_auto=0.80, tau_floor=0.45).
    Returns: (department, issue_type, confidence, is_abstained)
    """
    lower_text = text.lower()
    tokens = re.findall(r'[\w]+', lower_text)
    scores = {}
    
    for dept, data in CIVIC_TAXONOMY.items():
        score = 0
        for kw in data["keywords"]:
            kw_lower = kw.lower()
            if kw_lower in lower_text:
                kw_tokens = re.findall(r'[\w]+', kw_lower)
                # Find token position
                found_idx = -1
                for i in range(len(tokens) - len(kw_tokens) + 1):
                    if tokens[i:i+len(kw_tokens)] == kw_tokens:
                        found_idx = i
                        break
                
                # Check negation window
                if found_idx != -1 and is_match_negated(tokens, found_idx, found_idx + len(kw_tokens) - 1):
                    continue # Suppressed due to negation!
                
                score += (3 if " " in kw else 1)
        scores[dept] = score

    best_dept = max(scores, key=scores.get)
    max_score = scores[best_dept]

    # Abstention threshold check (A4)
    # If no civic keywords matched or score is 0, abstain and route to Triage
    if max_score == 0:
        return (
            "Triage & Verification Queue",
            "Unrecognized Civic Intent / Low Confidence",
            0.35,
            True # is_abstained
        )

    confidence = min(0.98, 0.65 + (max_score * 0.08))

    # Low-confidence floor check (< 0.45)
    if confidence < 0.45:
        return (
            "Triage & Verification Queue",
            "Low Confidence Civic Grievance",
            round(confidence, 2),
            True
        )

    default_issue = CIVIC_TAXONOMY[best_dept]["default_issue"]

    # Finer issue extraction
    if any(k in lower_text for k in ["pothole", "gaddha", "gaddhe", "ಗುಂಡಿ", "குழி", "gunta", "halla", "pallam", "gorto", "toye", "खड्डे"]):
        issue_type = "Severe Potholes / Road Surface Breakdown"
    elif any(k in lower_text for k in ["street light", "khamba", "light band", "ದೀಪ", "ಕಂಬ", "விளக்கு", "దీపం", "আলো", "পথবাति"]):
        issue_type = "Non-functional Streetlight / Dark Spot"
    elif any(k in lower_text for k in ["sewer", "gutter", "overflow", "ಗಟರ್", "ಚರಂಡಿ", "சாக்கடை", "మురుగునీరు", "নর্দমা", "ਗਟਰ"]):
        issue_type = "Sewer Line Overflow & Blockage"
    elif any(k in lower_text for k in ["pipeline", "pipe", "paani", "ನೀರು", "தண்ணீர்", "నీరు", "জল"]):
        issue_type = "Potable Water Pipeline Rupture / Leak"
    elif any(k in lower_text for k in ["kachra", "garbage", "kuda", "ಕಸ", "குப்பை", "చెత్త", "আবর্জনা", "ਕੂੜਾ"]):
        issue_type = "Garbage Pile-up / Waste Clearance"
    elif any(k in lower_text for k in ["thela", "encroachment", "kabza", "ಅತಿಕ್ರಮಣ", "ஆக்கிரமிப்பு", "ఆక్రమణ", "জবরদখল"]):
        issue_type = "Illegal Footpath & Road Encroachment"
    else:
        issue_type = default_issue

    return best_dept, issue_type, round(confidence, 2), False

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
    elif department == "Triage & Verification Queue":
        return "Municipal Citizen Redressal & Triage Desk", 24
    else:
        return "Smart Cities Urban Land Modernization", 96

class CivicNLPEngine:
    """
    Core Multilingual NLP Engine with Abstention and Wrong-Door Jurisdiction Detection.
    Supports English, Hinglish, Hindi, Kannada, Tamil, Telugu, Bengali, Urdu, Punjabi, Marathi.
    """
    def __init__(self):
        self.backend = settings.NLP_MODEL_BACKEND

    def analyze(self, raw_text: str) -> ExtractedNLPData:
        # 1. Jurisdiction / Wrong Door Check
        wrong_door = check_wrong_door_jurisdiction(raw_text)
        is_wrong_door = wrong_door is not None
        jurisdiction = wrong_door["jurisdiction"] if wrong_door else None
        wrong_door_advice = wrong_door["advice"] if wrong_door else None

        # 2. Language Detection
        lang = detect_language(raw_text)

        # 3. Department, Issue & Abstention Routing
        dept, issue, conf, is_abstained = extract_department_and_issue(raw_text)

        # 4. Ward & Landmark Extraction
        ward = extract_ward(raw_text)
        landmark = extract_landmark(raw_text)

        # 5. Urgency & SLA
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
            citizen_charter_sla_hours=sla,
            is_abstained=is_abstained,
            is_wrong_door=is_wrong_door,
            jurisdiction=jurisdiction,
            wrong_door_advice=wrong_door_advice
        )

# Global engine singleton
nlp_engine = CivicNLPEngine()
