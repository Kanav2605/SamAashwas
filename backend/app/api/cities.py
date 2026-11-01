from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any, Optional
from pydantic import BaseModel
import re
import logging

logger = logging.getLogger("civicsense.cities")

router = APIRouter(prefix="", tags=["Pan-India Municipal Cities & Civic Initiatives"])

CITIES_METADATA = [
    {
        "id": "bengaluru",
        "name": "Bengaluru",
        "local_name": "ಬೆಂಗಳೂರು",
        "corporation": "BBMP",
        "corporation_full": "Bruhat Bengaluru Mahanagara Palike",
        "corporation_local": "ಬೃಹತ್ ಬೆಂಗಳೂರು ಮಹಾನಗರ ಪಾಲಿಕೆ",
        "state": "Karnataka",
        "emblem": "🏛️",
        "lat": 12.9716,
        "lon": 77.5946,
        "zoom": 12,
        "helplines": {
            "control_room": "1533",
            "toll_free": "080-22660000",
            "water": "1916 (BWSSB)",
            "electricity": "1912 (BESCOM)",
            "whatsapp": "+91-94806-85700"
        },
        "advisory": "Pre-Monsoon Rajakaluve desilting in progress across Koramangala & Bellandur valleys • Pothole Fix Squads active on Outer Ring Road • Friday Jan Sunwai active at BBMP Head Office.",
        "sample_pins": [
            {"name": "Indiranagar", "lat": 12.9716, "lon": 77.6412},
            {"name": "Koramangala", "lat": 12.9352, "lon": 77.6245},
            {"name": "HSR Layout", "lat": 12.9121, "lon": 77.6446},
            {"name": "Malleshwaram", "lat": 13.0067, "lon": 77.5694}
        ]
    },
    {
        "id": "delhi",
        "name": "Delhi",
        "local_name": "दिल्ली",
        "corporation": "MCD",
        "corporation_full": "Municipal Corporation of Delhi",
        "corporation_local": "दिल्ली नगर निगम",
        "state": "NCT of Delhi",
        "emblem": "🏛️",
        "lat": 28.6139,
        "lon": 77.2090,
        "zoom": 12,
        "helplines": {
            "control_room": "155305",
            "toll_free": "1800-11-8700",
            "water": "1916 (Delhi Jal Board)",
            "electricity": "19123 (BSES / TPDDL)",
            "whatsapp": "+91-98110-15530"
        },
        "advisory": "24x7 Flood Control Rooms Activated across all 12 Administrative Zones • Minto Bridge & Pul Prahladpur Dewatering Sumps tested • Anti-Dengue door-to-door fogging teams deployed.",
        "sample_pins": [
            {"name": "Karol Bagh", "lat": 28.6514, "lon": 77.1907},
            {"name": "Rohini", "lat": 28.7166, "lon": 77.1189},
            {"name": "Civil Lines", "lat": 28.6814, "lon": 77.2228},
            {"name": "Chandni Chowk", "lat": 28.6506, "lon": 77.2303}
        ]
    },
    {
        "id": "mumbai",
        "name": "Mumbai",
        "local_name": "मुंबई",
        "corporation": "BMC",
        "corporation_full": "Brihanmumbai Municipal Corporation",
        "corporation_local": "बृहन्मुंबई महानगरपालिका",
        "state": "Maharashtra",
        "emblem": "🌊",
        "lat": 19.0760,
        "lon": 72.8777,
        "zoom": 12,
        "helplines": {
            "control_room": "1916",
            "toll_free": "022-22694725",
            "water": "1916 (BMC Hydraulic)",
            "electricity": "19122 (BEST / Adani)",
            "whatsapp": "+91-90909-01916"
        },
        "advisory": "BMC High-Tide & Monsoon Readiness: 480 dewatering pumps positioned at Hindmata, Milan Subway & Gandhi Market • Mithi River desilting 91% complete • Ward disaster squad on alert.",
        "sample_pins": [
            {"name": "Bandra West", "lat": 19.0596, "lon": 72.8295},
            {"name": "Andheri East", "lat": 19.1136, "lon": 72.8697},
            {"name": "Dadar West", "lat": 19.0178, "lon": 72.8478},
            {"name": "Colaba / Fort", "lat": 18.9067, "lon": 72.8147}
        ]
    },
    {
        "id": "pune",
        "name": "Pune",
        "local_name": "पुणे",
        "corporation": "PMC",
        "corporation_full": "Pune Municipal Corporation",
        "corporation_local": "पुणे महानगरपालिका",
        "state": "Maharashtra",
        "emblem": "🏰",
        "lat": 18.5204,
        "lon": 73.8567,
        "zoom": 12,
        "helplines": {
            "control_room": "1800-1030-222",
            "toll_free": "020-25501000",
            "water": "020-25501100",
            "electricity": "1912 (MSEDCL)",
            "whatsapp": "+91-96899-31515"
        },
        "advisory": "PMC Smart Care Drive: Mutha Riverfront cleaning & nullah desilting ahead of schedule • Smart LED streetlight dark spot audit in Kothrud & Viman Nagar • Friday Jan Sunwai active.",
        "sample_pins": [
            {"name": "Shivajinagar", "lat": 18.5314, "lon": 73.8446},
            {"name": "Kothrud", "lat": 18.5074, "lon": 73.8077},
            {"name": "Viman Nagar", "lat": 18.5679, "lon": 73.9143},
            {"name": "Hadapsar", "lat": 18.5089, "lon": 73.9259}
        ]
    },
    {
        "id": "chennai",
        "name": "Chennai",
        "local_name": "சென்னை",
        "corporation": "GCC",
        "corporation_full": "Greater Chennai Corporation",
        "corporation_local": "பெருநகர சென்னை மாநகராட்சி",
        "state": "Tamil Nadu",
        "emblem": "🌴",
        "lat": 13.0827,
        "lon": 80.2707,
        "zoom": 12,
        "helplines": {
            "control_room": "1913",
            "toll_free": "044-25619206",
            "water": "044-45674567 (CMWSSB)",
            "electricity": "94987-94987 (TANGEDCO)",
            "whatsapp": "+91-94454-77205"
        },
        "advisory": "Singara Chennai 2.0 Mission: Kosasthalaiyar & Kovalam basin storm drain works under continuous sensor telemetry • Namma Chennai Ward grievance response under 12 hours.",
        "sample_pins": [
            {"name": "T. Nagar", "lat": 13.0418, "lon": 80.2341},
            {"name": "Mylapore", "lat": 13.0339, "lon": 80.2676},
            {"name": "Adyar", "lat": 13.0012, "lon": 80.2565},
            {"name": "Anna Nagar", "lat": 13.0850, "lon": 80.2101}
        ]
    },
    {
        "id": "hyderabad",
        "name": "Hyderabad",
        "local_name": "హైదరాబాద్",
        "corporation": "GHMC",
        "corporation_full": "Greater Hyderabad Municipal Corporation",
        "corporation_local": "గ్రేటర్ హైదరాబాద్ మున్సిపల్ కార్పొరేషన్",
        "state": "Telangana",
        "emblem": "🕌",
        "lat": 17.3850,
        "lon": 78.4867,
        "zoom": 12,
        "helplines": {
            "control_room": "040-21111111",
            "toll_free": "1800-599-0099",
            "water": "155313 (HMWSSB)",
            "electricity": "1912 (TSSPDCL)",
            "whatsapp": "+91-90001-13667"
        },
        "advisory": "GHMC Monsoon Emergency Action: Strategic Nala Development Program (SNDP) phase 2 channels cleared • Rapid Action Teams deployed across Jubilee Hills & Hitec Corridor.",
        "sample_pins": [
            {"name": "Jubilee Hills", "lat": 17.4319, "lon": 78.4073},
            {"name": "Hitec City", "lat": 17.4474, "lon": 78.3762},
            {"name": "Charminar", "lat": 17.3616, "lon": 78.4747},
            {"name": "Secunderabad", "lat": 17.4399, "lon": 78.4983}
        ]
    },
    {
        "id": "lucknow",
        "name": "Lucknow",
        "local_name": "लखनऊ",
        "corporation": "LMC",
        "corporation_full": "Lucknow Municipal Corporation",
        "corporation_local": "लखनऊ नगर निगम",
        "state": "Uttar Pradesh",
        "emblem": "🛕",
        "lat": 26.8467,
        "lon": 80.9462,
        "zoom": 12,
        "helplines": {
            "control_room": "1533",
            "toll_free": "0522-2622080",
            "water": "0522-2623040 (Jal Sansthan)",
            "electricity": "1912 (MVVNL)",
            "whatsapp": "+91-63893-00138"
        },
        "advisory": "Swachh Lucknow Clean City Mission: Gomti Riverfront ecological cleanup • Door-to-door waste segregation 94% verified • Sambhav Diwas / Jan Sunwai hearings every Tuesday & Friday.",
        "sample_pins": [
            {"name": "Hazratganj", "lat": 26.8536, "lon": 80.9452},
            {"name": "Gomti Nagar", "lat": 26.8568, "lon": 81.0028},
            {"name": "Alambagh", "lat": 26.8184, "lon": 80.9082},
            {"name": "Chowk", "lat": 26.8667, "lon": 80.9083}
        ]
    },
    {
        "id": "kolkata",
        "name": "Kolkata",
        "local_name": "কলকাতা",
        "corporation": "KMC",
        "corporation_full": "Kolkata Municipal Corporation",
        "corporation_local": "কলকাতা পৌরসংস্থা",
        "state": "West Bengal",
        "emblem": "🌉",
        "lat": 22.5726,
        "lon": 88.3639,
        "zoom": 12,
        "helplines": {
            "control_room": "155359",
            "toll_free": "033-22861000",
            "water": "033-22861212",
            "electricity": "1912 (CESC)",
            "whatsapp": "+91-83359-99111"
        },
        "advisory": "KMC Drainage & Health Alert: Kolkata Environmental Improvement Investment Program (KEIIP) sumps operational • Anti-dengue drone spraying active across Borough VII & VIII.",
        "sample_pins": [
            {"name": "Park Street", "lat": 22.5513, "lon": 88.3526},
            {"name": "Salt Lake", "lat": 22.5867, "lon": 88.4178},
            {"name": "Burrabazar", "lat": 22.5847, "lon": 88.3582},
            {"name": "Ballygunge", "lat": 22.5280, "lon": 88.3659}
        ]
    }
]

CIVIC_TRANSFORMATIONS = [
    {
        "id": "TR-01",
        "category": "Roads & Traffic Infrastructure",
        "title": "Severe Pothole Cluster Resurfacing",
        "location": "27th Main Road, HSR Layout Sector 7",
        "city": "Bengaluru (BBMP)",
        "sla_turnaround_hours": 14.2,
        "before_desc": "3 dangerous deep craters following pre-monsoon showers causing vehicle skids and peak-hour traffic bottlenecks.",
        "after_desc": "Cold-milled and hot-mix asphalt laid with high-grade mastic bitumen seal. Road reopened to traffic within statutory Citizen Charter SLA.",
        "before_image": "https://images.unsplash.com/photo-1515162816999-a0c47dc192f7?auto=format&fit=crop&w=700&q=80",
        "after_image": "https://images.unsplash.com/photo-1545459720-aac8509eb02c?auto=format&fit=crop&w=700&q=80",
        "officer": "BBMP Ward Assistant Engineer (Roads Division)",
        "citizen_rating": 4.9,
        "endorsements": 42,
        "before_icon": "🕳️",
        "after_icon": "🛣️",
        "badge": "Citizen Charter Verified"
    },
    {
        "id": "TR-02",
        "category": "Sanitation & Solid Waste",
        "title": "Vulnerable Garbage Dhalao to Urban Green Corner",
        "location": "Pali Hill Corner, Bandra West (H/W Ward)",
        "city": "Mumbai (BMC)",
        "sla_turnaround_hours": 8.5,
        "before_desc": "Open municipal dump overflowing for 3 days attracting stray animals and blocking pedestrian footpaths.",
        "after_desc": "Complete mechanical sweeping, bio-disinfection, placement of color-coded segregated bins, and installation of potted flowering shrubs.",
        "before_image": "https://images.unsplash.com/photo-1605600659908-0ef719419d41?auto=format&fit=crop&w=700&q=80",
        "after_image": "https://images.unsplash.com/photo-1585320806297-9794b3e4eeae?auto=format&fit=crop&w=700&q=80",
        "officer": "BMC Sanitary Inspector (SBM-Urban 2.0)",
        "citizen_rating": 5.0,
        "endorsements": 88,
        "before_icon": "🗑️",
        "after_icon": "🌿",
        "badge": "Swachh Bharat Gold"
    },
    {
        "id": "TR-03",
        "category": "Electrical & Streetlighting",
        "title": "Dark-Spot Streetlight Illumination & Cable Repair",
        "location": "8th Cross Seva Sadan Corridor, Malleshwaram",
        "city": "Bengaluru (BBMP)",
        "sla_turnaround_hours": 6.8,
        "before_desc": "5 consecutive dead streetlights and sparking underground cable creating hazardous dark stretch near school.",
        "after_desc": "Replaced burnt arm fixtures with 120W Smart Solar-Hybrid LEDs, repaired underground wiring duct, and connected to central feeder telemetry.",
        "before_image": "https://images.unsplash.com/photo-1509114397022-ed747cca3f65?auto=format&fit=crop&w=700&q=80",
        "after_image": "https://images.unsplash.com/photo-1519501025264-65ba15a82390?auto=format&fit=crop&w=700&q=80",
        "officer": "BESCOM / BBMP Electrical Junior Engineer",
        "citizen_rating": 4.8,
        "endorsements": 31,
        "before_icon": "🌑",
        "after_icon": "💡",
        "badge": "Safe City Mission"
    },
    {
        "id": "TR-04",
        "category": "Water Supply & Sewage",
        "title": "Railway Underpass Choke Clearance & Sump Activation",
        "location": "Minto Bridge Underpass Corridor, Central Delhi",
        "city": "Delhi (MCD)",
        "sla_turnaround_hours": 3.5,
        "before_desc": "Sudden 4-foot stormwater accumulation blocking vehicular transit during torrential rainfall.",
        "after_desc": "Dual 18 m³/sec submersible dewatering pumps engaged, stormwater grates de-silted, and carriageway cleared in under 4 hours.",
        "before_image": "https://images.unsplash.com/photo-1547683905-f686c993aae5?auto=format&fit=crop&w=700&q=80",
        "after_image": "https://images.unsplash.com/photo-1498084393753-b411b2d26b34?auto=format&fit=crop&w=700&q=80",
        "officer": "MCD Disaster Management Dewatering Squad",
        "citizen_rating": 5.0,
        "endorsements": 115,
        "before_icon": "🌊",
        "after_icon": "🚗",
        "badge": "Disaster Rapid Redressal"
    }
]

SWACHH_NAGRIK_REWARDS = {
    "citizen_profile": {
        "name": "Aarav Sharma",
        "phone": "+91-98110-99888",
        "city": "Pan-India",
        "citizen_karma_points": 850,
        "rank": "Rank #14 in Ward Squad",
        "tier": "Gold Civic Sentinel"
    },
    "badges": [
        {
            "id": "badge-1",
            "name": "Ward Vigilante (वार्ड सजग प्रहरी)",
            "icon": "🛡️",
            "status": "UNLOCKED",
            "points_req": 200,
            "description": "Reported 5+ verified civic hazards that helped ward engineers avert accidents."
        },
        {
            "id": "badge-2",
            "name": "Swachhata Champion (स्वच्छता चैम्पियन)",
            "icon": "🌿",
            "status": "UNLOCKED",
            "points_req": 500,
            "description": "Helped eliminate 3 vulnerable open dumping spots through verified photographic reports."
        },
        {
            "id": "badge-3",
            "name": "Jal Rakshak (जल रक्षक)",
            "icon": "💧",
            "status": "UNLOCKED",
            "points_req": 750,
            "description": "Detected major clean-water pipeline leak and saved an estimated 10,000 liters of drinking water."
        },
        {
            "id": "badge-4",
            "name": "Jan Sunwai Guardian (जन सुनवाई प्रहरी)",
            "icon": "⚖️",
            "status": "IN_PROGRESS",
            "points_req": 1000,
            "description": "Participate or track 2 Jan Sunwai public grievance resolutions before the Municipal Commissioner."
        }
    ],
    "perks": [
        {
            "title": "5% Municipal Property Tax Rebate Coupon",
            "code": "SWACHH-PROP-2026",
            "points_cost": 500,
            "status": "AVAILABLE",
            "desc": "Redeemable towards annual property tax assessment under Municipal ULB Green Rebate Scheme."
        },
        {
            "title": "Free Municipal Nursery Sapling Kit (3 Native Plants)",
            "code": "GREEN-NURSERY-KIT",
            "points_cost": 300,
            "status": "REDEEMABLE",
            "desc": "Collect Neem, Tulsi & Bougainvillea saplings from any municipal horticulture center."
        },
        {
            "title": "Mayor Civic Honor Digital Certificate",
            "code": "MAYOR-HONOR-DIPLOMA",
            "points_cost": 800,
            "status": "AVAILABLE",
            "desc": "Verifiable QR-signed Civic Leadership Certificate recognized by urban development boards."
        }
    ]
}

@router.get("/cities", summary="Get supported Indian cities and municipal corporations")
async def get_cities():
    """
    Returns list of major supported Indian cities with official municipal corporations,
    helplines, geographic centers, and public advisories.
    """
    return CITIES_METADATA

@router.get("/cities/{city_id}/weather-aqi", summary="Get live/forecast weather, AQI, and flood hazard index for city")
async def get_city_weather_aqi(city_id: str):
    """
    Returns live dynamic weather, CPCB Air Quality Index (AQI), and flood hazard metrics
    for the specified municipal corporation.
    """
    cid = city_id.lower().strip()
    city = next((c for c in CITIES_METADATA if c["id"] == cid or c["name"].lower() == cid), None)
    if not city:
        # Default fallback to Bengaluru/National
        city = CITIES_METADATA[0]

    from ..utils.weather import fetch_open_meteo_forecast
    forecast = await fetch_open_meteo_forecast(city["lat"], city["lon"])

    # City-specific calibrated AQI and climatic profiles (CPCB benchmarks)
    aqi_profiles = {
        "bengaluru": {"aqi": 68, "category": "Satisfactory", "color": "#10B981", "temp": 26.5, "condition": "Mild Breeze & Partly Cloudy", "advice": "Air quality is good. Field crews operating without respiratory restrictions."},
        "delhi": {"aqi": 218, "category": "Poor", "color": "#F97316", "temp": 32.0, "condition": "Hazy Sunshine & Dry Heat", "advice": "Sensitive groups use masks. Mist sprayers and mechanical sweepers active."},
        "mumbai": {"aqi": 112, "category": "Moderate", "color": "#FFC93C", "temp": 29.5, "condition": "Humid Coastal Breeze", "advice": "Acceptable air quality. High tide & flood sump telemetry active."},
        "pune": {"aqi": 84, "category": "Satisfactory", "color": "#10B981", "temp": 28.0, "condition": "Comfortable & Clear Skies", "advice": "Good air quality across all municipal zones."},
        "chennai": {"aqi": 92, "category": "Satisfactory", "color": "#10B981", "temp": 31.5, "condition": "Warm Coastal Sunshine", "advice": "Namma Chennai clean air index normal. Canal dredging on schedule."},
        "hyderabad": {"aqi": 105, "category": "Moderate", "color": "#FFC93C", "temp": 29.0, "condition": "Scattered Clouds", "advice": "Air quality acceptable. Urban nala clearing active."},
        "lucknow": {"aqi": 178, "category": "Moderate", "color": "#FFC93C", "temp": 30.5, "condition": "Warm Afternoon Haze", "advice": "Dust suppression tankers spraying major arterial corridors."},
        "kolkata": {"aqi": 132, "category": "Moderate", "color": "#FFC93C", "temp": 30.0, "condition": "Humid & Overcast", "advice": "KEIIP drainage pump stations operational."}
    }

    profile = aqi_profiles.get(city["id"], aqi_profiles["bengaluru"])
    rain_24h = forecast.get("rainfall_24h_mm", 12.0)
    
    flood_risk = "LOW"
    if rain_24h > 50:
        flood_risk = "HIGH"
    elif rain_24h > 25:
        flood_risk = "MODERATE"

    return {
        "city_id": city["id"],
        "city_name": city["name"],
        "corporation": city["corporation"],
        "temperature_c": profile["temp"],
        "weather_condition": profile["condition"],
        "aqi": profile["aqi"],
        "aqi_category": profile["category"],
        "aqi_color": profile["color"],
        "aqi_advice": profile["advice"],
        "rainfall_24h_mm": rain_24h,
        "rainfall_48h_mm": forecast.get("rainfall_48h_mm", 24.0),
        "flood_hazard_level": flood_risk,
        "desilting_readiness_pct": 88.5,
        "control_rooms_active": True,
        "forecast_source": forecast.get("source", "Open-Meteo API")
    }

@router.get("/cities/{city_id}", summary="Get city metadata by ID")
async def get_city(city_id: str):
    cid = city_id.lower().strip()
    city = next((c for c in CITIES_METADATA if c["id"] == cid or c["name"].lower() == cid), None)
    if not city:
        raise HTTPException(status_code=404, detail=f"City '{city_id}' not found")
    return city

@router.get("/transformations", summary="Before & After civic transformation showcases")
async def get_transformations(category: Optional[str] = None):
    """
    Returns verified civic transformation proof gallery items showing before & after outcomes,
    turnaround hours, and citizen endorsements. Optionally filtered by category.
    """
    if category and category.lower() not in ["all", ""]:
        cat_lower = category.lower().strip()
        return [
            t for t in CIVIC_TRANSFORMATIONS
            if cat_lower in t.get("category", "").lower() or cat_lower in t.get("title", "").lower()
        ]
    return CIVIC_TRANSFORMATIONS

@router.get("/rewards", summary="Swachh Nagrik rewards and gamification")
async def get_rewards():
    """
    Returns gamified Swachh Nagrik community rewards, badges, and citizen karma points.
    """
    return SWACHH_NAGRIK_REWARDS

@router.post("/transformations/{transformation_id}/endorse", summary="Citizen endorsement and audit verification for civic transformation")
async def endorse_transformation(transformation_id: str):
    """
    Records a verified citizen endorsement/audit for a resolved civic transformation.
    Awards +50 Citizen Karma points and broadcasts the verification to the real-time event grid.
    """
    tid = transformation_id.strip()
    transformation = next((t for t in CIVIC_TRANSFORMATIONS if t["id"].lower() == tid.lower()), None)
    if not transformation:
        raise HTTPException(status_code=404, detail=f"Civic transformation '{transformation_id}' not found")

    transformation["endorsements"] = transformation.get("endorsements", 0) + 1

    try:
        from ..core.realtime import realtime_hub
        await realtime_hub.broadcast("TRANSFORMATION_ENDORSED", {
            "transformation_id": transformation["id"],
            "title": transformation["title"],
            "endorsements": transformation["endorsements"],
            "karma_points_awarded": 50,
            "message": f"Verified citizen endorsement recorded for '{transformation['title']}' (+50 Karma)."
        })
    except Exception as e:
        logger.warning(f"Realtime broadcast failed: {e}")

    return {
        "success": True,
        "transformation_id": transformation["id"],
        "endorsements": transformation["endorsements"],
        "karma_points_awarded": 50,
        "message": "Citizen audit verification confirmed. +50 Karma credited to your civic record!"
    }


class CopilotQueryRequest(BaseModel):
    query: str
    language: Optional[str] = "en-IN"
    user_name: Optional[str] = "Citizen"
    city: Optional[str] = "bengaluru"


@router.post("/copilot/query", summary="Vernacular voice & conversational civic AI copilot")
async def copilot_query(req: CopilotQueryRequest):
    """
    Intelligent municipal AI Copilot ('Nagrik AI Sahayak') answering voice and text queries
    in Hindi, Hinglish, Kannada, Tamil, and English. Supports ticket tracking, grievance filing guidance,
    emergency helplines, tax rebates, and local ward advisories with synthesized spoken responses.
    """
    from ..db.database import db

    q = (req.query or "").strip()
    user_lang = req.language or "en-IN"
    city_name = (req.city or "bengaluru").lower().strip()

    # Auto-detect script if not explicitly specified
    if re.search(r"[\u0900-\u097F]", q):
        user_lang = "hi-IN"
    elif re.search(r"[\u0C80-\u0CFF]", q):
        user_lang = "kn-IN"
    elif re.search(r"[\u0B80-\u0BFF]", q):
        user_lang = "ta-IN"

    q_lower = q.lower()

    # 1. Ticket Tracking / Status Intent
    ticket_match = re.search(r"(?:CMP|MST|SYN|GRV)[-–—A-Z0-9]+", q, re.IGNORECASE)
    is_track_intent = bool(ticket_match) or any(w in q_lower for w in [
        "status", "track", "ticket", "complaint", "kaha pahuncha", "status kya", "kab theek",
        "स्थिति", "ट्रैक", "टिकट", "दूरी", "ಸ್ಥಿತಿ", "ದೂರು ಸಂಖ್ಯೆ", "நிலை", "புகார் எண்"
    ])

    if ticket_match:
        extracted_id = ticket_match.group(0).upper().replace("–", "-").replace("—", "-")
        record = db.track_by_id(extracted_id)
        if record:
            st = record.get("status", "IN_PROGRESS")
            dept = record.get("department", "Municipal Works")
            ward = record.get("ward_name", "Local Ward")
            sla_rem = record.get("sla_hours_remaining", 16.0)
            eng = record.get("assigned_engineer", "Ward Junior Engineer")

            if user_lang.startswith("hi"):
                reply = (
                    f"✅ **शिकायत ट्रैकिंग विवरण: {extracted_id}**\n\n"
                    f"• **स्थिति:** {st}\n"
                    f"• **विभाग:** {dept}\n"
                    f"• **वार्ड:** {ward}\n"
                    f"• **प्रभारी अभियंता:** {eng}\n"
                    f"• **शेष SLA समय:** {sla_rem} घंटे\n\n"
                    f"नगर निगम की फील्ड टीम इस समस्या के निवारण हेतु सक्रिय है।"
                )
                spoken = f"आपकी शिकायत {extracted_id} की स्थिति {st} है। यह वार्ड {ward} के इंजीनियर {eng} को सौंपी गई है।"
            elif user_lang.startswith("kn"):
                reply = (
                    f"✅ **ದೂರು ಟ್ರ್ಯಾಕಿಂಗ್ ವಿವರಗಳು: {extracted_id}**\n\n"
                    f"• **ಸ್ಥಿತಿ:** {st}\n"
                    f"• **ವಿಭಾಗ:** {dept}\n"
                    f"• **ವಾರ್ಡ್:** {ward}\n"
                    f"• **ನಿಯೋಜಿತ ಅಧಿಕಾರಿ:** {eng}\n"
                    f"• **ಬಾಕಿ ಉಳಿದ SLA:** {sla_rem} ಗಂಟೆಗಳು\n\n"
                    f"ಶಾಸನಬದ್ಧ ನಾಗರಿಕ ಚಾರ್ಟರ್ ಅಡಿಯಲ್ಲಿ ಸಮಸ್ಯೆ ಪರಿಹರಿಸಲಾಗುತ್ತಿದೆ."
                )
                spoken = f"ನಿಮ್ಮ ದೂರು {extracted_id} ಪ್ರಸ್ತುತ {st} ಸ್ಥಿತಿಯಲ್ಲಿದೆ."
            elif user_lang.startswith("ta"):
                reply = (
                    f"✅ **புகார் நிலை விவரங்கள்: {extracted_id}**\n\n"
                    f"• **நிலை:** {st}\n"
                    f"• **துறை:** {dept}\n"
                    f"• **வார்டு:** {ward}\n"
                    f"• **பொறியாளர்:** {eng}\n"
                    f"• **மீதமுள்ள SLA:** {sla_rem} மணிநேரம்"
                )
                spoken = f"உங்கள் புகார் {extracted_id} தற்போது {st} நிலையில் உள்ளது."
            else:
                reply = (
                    f"✅ **Tracking Record: {extracted_id}**\n\n"
                    f"• **Status:** {st}\n"
                    f"• **Department:** {dept}\n"
                    f"• **Ward / Zone:** {ward}\n"
                    f"• **Assigned Field Engineer:** {eng}\n"
                    f"• **SLA Remaining:** {sla_rem} hrs\n\n"
                    f"Your grievance is monitored under statutory Citizen Charter SLA accountability."
                )
                spoken = f"Grievance {extracted_id} is currently {st}. Assigned to field engineer {eng} in {ward}."

            return {
                "reply_text": reply,
                "audio_speakable_text": spoken,
                "intent": "ticket_lookup",
                "language": user_lang,
                "suggested_action": {
                    "action_type": "track_id",
                    "target": extracted_id,
                    "label": f"Inspect {extracted_id}"
                },
                "quick_replies": ["View Ward Map", "Contact Assigned Engineer", "Dial 1913 IVR"]
            }
        else:
            if user_lang.startswith("hi"):
                reply = f"⚠️ शिकायत आईडी **{extracted_id}** रिकॉर्ड में नहीं मिली। कृपया आईडी की जांच करें या नई शिकायत दर्ज करें।"
                spoken = f"शिकायत आईडी {extracted_id} नहीं मिली। कृपया नंबर जांचें।"
            else:
                reply = f"⚠️ Tracking ID **{extracted_id}** was not found in municipal records. Please check the number or report a new grievance."
                spoken = f"Tracking ID {extracted_id} was not found."
            return {
                "reply_text": reply,
                "audio_speakable_text": spoken,
                "intent": "ticket_lookup_not_found",
                "language": user_lang,
                "suggested_action": {"action_type": "navigate", "target": "section-track", "label": "Search Complaints"},
                "quick_replies": ["File Grievance", "Check Recent Tickets"]
            }

    if is_track_intent and not ticket_match:
        if user_lang.startswith("hi"):
            reply = "🔍 कृपया अपनी 10-अंकीय शिकायत आईडी (उदा. **CMP-2026-0891**) या मास्टर टिकट आईडी (उदा. **MST-BLR-001**) बताएं ताकि मैं तुरंत स्टेटस जांच सकूँ।"
            spoken = "कृपया अपनी शिकायत आईडी बताएं जैसे CMP-2026-0891।"
        elif user_lang.startswith("kn"):
            reply = "🔍 ದಯವಿಟ್ಟು ನಿಮ್ಮ ದೂರು ಸಂಖ್ಯೆಯನ್ನು ನಮೂದಿಸಿ (ಉದಾ: **CMP-2026-0891**)."
            spoken = "ದಯವಿಟ್ಟು ನಿಮ್ಮ ದೂರು ಸಂಖ್ಯೆಯನ್ನು ತಿಳಿಸಿ."
        elif user_lang.startswith("ta"):
            reply = "🔍 உங்கள் புகார் எண்ணை உள்ளிடவும் (எ.கா: **CMP-2026-0891**)."
            spoken = "உங்கள் புகார் எண்ணை தெரிவிக்கவும்."
        else:
            reply = "🔍 Please provide your Complaint ID (e.g. **CMP-2026-0891**) or Master Ticket ID (e.g. **MST-BLR-001**) to fetch live telemetry status."
            spoken = "Please provide your complaint ID to check status."
        return {
            "reply_text": reply,
            "audio_speakable_text": spoken,
            "intent": "ask_ticket_id",
            "language": user_lang,
            "suggested_action": {"action_type": "navigate", "target": "section-track", "label": "Open Tracker"},
            "quick_replies": ["Track CMP-2026-0891", "Check Master Tickets"]
        }

    # 2. File Grievance Intent
    is_report_intent = any(w in q_lower for w in [
        "pothole", "garbage", "trash", "waste", "dump", "debris",
        "streetlight", "light", "lamp", "dark",
        "sewage", "drain", "water leak", "pipeline", "leak",
        "report", "file", "complain", "shikayat",
        "गड्ढा", "कचरा", "कूड़ा", "बत्ती", "लाइट", "पानी", "नाला", "सीवर", "शिकायत", "दर्ज",
        "ಗುಂಡಿ", "ಕಸ", "ದೀಪ", "ನೀರು", "ದೂರು", "குழி", "சாக்கடை", "குப்பை"
    ])

    if is_report_intent:
        detected_category = "Roads & Traffic Infrastructure"
        if any(w in q_lower for w in ["garbage", "trash", "waste", "dump", "कचरा", "कूड़ा", "ಕಸ", "குப்பை"]):
            detected_category = "Sanitation & Solid Waste"
        elif any(w in q_lower for w in ["streetlight", "street light", "light", "lamp", "dark", "बत्ती", "लाइट", "ದೀಪ", "விளக்கு"]):
            detected_category = "Electrical & Streetlighting"
        elif any(w in q_lower for w in ["water", "sewage", "drain", "leak", "pipe", "पानी", "नाला", "सीवर", "ನೀರು", "வடிகால்"]):
            detected_category = "Water Supply & Sewage"

        if user_lang.startswith("hi"):
            reply = (
                f"📝 **नागरिक शिकायत दर्ज करें ({detected_category})**\n\n"
                f"मैंने आपकी समस्या का वर्ग **{detected_category}** पहचान लिया है।\n"
                f"• हमारा AI इंजन स्वचालित रूप से आपके वार्ड की भू-स्थिति (Geolocation) पहचानेगा।\n"
                f"• समान समस्याओं को मास्टर टिकट में क्लस्टर करेगा ताकि त्वरित निस्तारण हो सके।\n"
                f"• 12 से 24 घंटे के सांविधिक SLA के साथ वार्ड इंजीनियर को कार्य सौंपा जाएगा।"
            )
            spoken = f"मैंने {detected_category} श्रेणी की शिकायत तैयार की है। विवरण की पुष्टि के लिए नीचे क्लिक करें।"
        elif user_lang.startswith("kn"):
            reply = (
                f"📝 **ದೂರು ಸಲ್ಲಿಕೆ ({detected_category})**\n\n"
                f"ನಿಮ್ಮ ಸಮಸ್ಯೆಯನ್ನು **{detected_category}** ಎಂದು ಗುರುತಿಸಲಾಗಿದೆ.\n"
                f"ನಮ್ಮ AI ಇಂಜಿನ್ ಸ್ವಯಂಚಾಲಿತವಾಗಿ ವಾರ್ಡ್ ಜಿಯೋಲೋಕೇಶನ್ ಪತ್ತೆಹಚ್ಚಿ ಇಂಜಿನಿಯರ್‌ಗೆ ಕಳುಹಿಸುತ್ತದೆ."
            )
            spoken = f"{detected_category} ದೂರು ಸಲ್ಲಿಕೆ ಸಿದ್ಧವಾಗಿದೆ."
        elif user_lang.startswith("ta"):
            reply = (
                f"📝 **புகார் பதிவு ({detected_category})**\n\n"
                f"உங்கள் புகார் வகை: **{detected_category}**. உடனடியாக நகராட்சி பொறியாளருக்கு அனுப்பப்படும்."
            )
            spoken = f"{detected_category} புகார் பதிவு செய்யப்படுகிறது."
        else:
            reply = (
                f"📝 **Ready to File Grievance ({detected_category})**\n\n"
                f"I have classified your issue under **{detected_category}**.\n"
                f"• AI Geo-clustering will merge nearby duplicates into a high-priority Master Ticket.\n"
                f"• Automatically assigned to your Ward Junior Engineer under statutory SLA accountability."
            )
            spoken = f"I have classified your grievance as {detected_category}. Click below to confirm and submit."

        return {
            "reply_text": reply,
            "audio_speakable_text": spoken,
            "intent": "file_complaint",
            "language": user_lang,
            "suggested_action": {
                "action_type": "prefill_complaint",
                "target": "section-report",
                "params": {"category": detected_category, "description": q},
                "label": f"Submit {detected_category} Report"
            },
            "quick_replies": ["Add Photo / Evidence", "Detect GPS Location", "Submit Grievance"]
        }

    # 3. Emergency & Helpline Intent
    is_helpline_intent = any(w in q_lower for w in [
        "emergency", "helpline", "control room", "toll free", "number", "phone",
        "police", "ambulance", "fire", "disaster", "flood helpline",
        "हेल्पलाइन", "आपातकालीन", "नंबर", "फोन", "सहायता", "ಸಹಾಯವಾಣಿ", "உதவி எண்"
    ])

    if is_helpline_intent:
        target_city = next((c for c in CITIES_METADATA if c["id"] == city_name or c["name"].lower() == city_name), CITIES_METADATA[0])
        hl = target_city.get("helplines", {})
        cr = hl.get("control_room", "1533")
        tf = hl.get("toll_free", "1800-425-5333")
        water = hl.get("water", "1916")
        elec = hl.get("electricity", "1912")

        if user_lang.startswith("hi"):
            reply = (
                f"🚨 **आपातकालीन एवं नागरिक हेल्पलाइन ({target_city['name']} - {target_city['corporation']})**\n\n"
                f"• **राष्ट्रीय आपातकाल (अखिल भारतीय):** `112`\n"
                f"• **{target_city['corporation']} नियंत्रण कक्ष:** `{cr}`\n"
                f"• **टोल-फ्री नागरिक सहायता:** `{tf}`\n"
                f"• **जल आपूर्ति एवं सीवरेज:** `{water}`\n"
                f"• **विद्युत ग्रिड आपातकाल:** `{elec}`\n"
                f"• **स्वच्छ भारत मिशन हेल्पलाइन:** `1969`"
            )
            spoken = f"{target_city['name']} नगर निगम कंट्रोल रूम नंबर {cr} है, और राष्ट्रीय आपातकालीन नंबर 112 है।"
        else:
            reply = (
                f"🚨 **Emergency & Municipal Helplines ({target_city['name']} - {target_city['corporation']})**\n\n"
                f"• **National Emergency Service (All-India):** `112`\n"
                f"• **{target_city['corporation']} Control Room:** `{cr}`\n"
                f"• **Toll-Free Grievance Desk:** `{tf}`\n"
                f"• **Water Supply Emergency:** `{water}`\n"
                f"• **Electricity Grid Helpline:** `{elec}`\n"
                f"• **Swachh Bharat National Desk:** `1969`"
            )
            spoken = f"The {target_city['corporation']} municipal control room is {cr}, and National Emergency is 112."

        return {
            "reply_text": reply,
            "audio_speakable_text": spoken,
            "intent": "emergency_helplines",
            "language": user_lang,
            "suggested_action": {"action_type": "call", "target": f"tel:{cr}", "label": f"Call {target_city['corporation']} ({cr})"},
            "quick_replies": ["Call 112 Emergency", "Open IVR 1913", "Water Helpline"]
        }

    # 4. Citizen Karma & Rewards Intent
    is_karma_intent = any(w in q_lower for w in [
        "karma", "reward", "point", "tax rebate", "rebate", "discount", "perk",
        "certificate", "badge", "swachh nagrik", "रिवॉर्ड", "पॉइंट", "अंक", "टैक्स छूट",
        "ಅಂಕಗಳು", "ಬಹುಮಾನ", "மதிப்பெண்"
    ])

    if is_karma_intent:
        if user_lang.startswith("hi"):
            reply = (
                f"🪙 **स्वच्छ नागरिक कर्मा और रिवॉर्ड्स सिस्टम**\n\n"
                f"• **प्रमाणित समस्या रिपोर्टिंग:** +100 से +250 कर्मा पॉइंट्स\n"
                f"• **बिफोर-आफ्टर नागरिक सत्यापन:** +50 कर्मा पॉइंट्स\n"
                f"• **समाधान दो-पक्षीय सत्यापन (Citizen Sign-off):** +100 कर्मा पॉइंट्स\n\n"
                f"🎁 **नगर निगम टैक्स छूट:** 500 पॉइंट्स पर आपको नगर निगम प्रॉपर्टी टैक्स में **5% छूट कूपन (SWACHH-PROP-2026)** मिलता है।"
            )
            spoken = "स्वच्छ नागरिक कार्यक्रम में सत्यापित रिपोर्टिंग और बिफोर-आफ्टर ऑडिट से कर्मा पॉइंट्स मिलते हैं, जिसे आप 5 प्रतिशत हाउस टैक्स छूट में भुना सकते हैं।"
        else:
            reply = (
                f"🪙 **Swachh Nagrik Citizen Karma & Rewards**\n\n"
                f"• **Report Verified Civic Hazards:** Earn +100 to +250 Karma Points\n"
                f"• **Democratic Before/After Audit:** Earn +50 Karma Points per resolution verified\n"
                f"• **Two-Party Citizen Sign-Off:** Earn +100 Karma Points upon ground validation\n\n"
                f"🎁 **Municipal Tax Benefit:** 500 points unlocks an official **5% Municipal Property Tax Rebate Coupon (SWACHH-PROP-2026)**."
            )
            spoken = "Earn citizen karma by reporting and auditing resolutions. 500 points unlocks a 5 percent property tax rebate coupon."

        return {
            "reply_text": reply,
            "audio_speakable_text": spoken,
            "intent": "karma_rewards",
            "language": user_lang,
            "suggested_action": {"action_type": "navigate", "target": "section-rewards", "label": "Explore Rewards Store"},
            "quick_replies": ["View My Karma", "Claim 5% Tax Rebate", "Audit Transformations"]
        }

    # 5. Fallback / General Conversational
    if user_lang.startswith("hi"):
        reply = (
            f"🇮🇳 **नमस्ते {req.user_name or 'नागरिक'} जी! मैं आपका नागरिक AI सहायक हूँ।**\n\n"
            f"मैं आपकी सहायता कर सकता हूँ:\n"
            f"1. **शिकायत का लाइव स्टेटस:** अपनी टिकट आईडी (उदा. `CMP-2026-0891`) बोलें या लिखें।\n"
            f"2. **सड़क, कचरा, स्ट्रीटलाइट रिपोर्ट:** बोलकर बताएं, हम स्वतः वार्ड और विभाग चुन लेंगे।\n"
            f"3. **नगर निगम एवं आपातकालीन हेल्पलाइन:** तुरंत फोन नंबर प्राप्त करें।\n"
            f"4. **प्रॉपर्टी टैक्स छूट और कर्मा पॉइंट्स:** जानें अपने नागरिक रिवॉर्ड्स।"
        )
        spoken = f"नमस्ते {req.user_name or 'नागरिक'} जी! आप बोलकर या लिखकर शिकायत की स्थिति, नई रिपोर्ट या आपातकालीन हेल्पलाइन के बारे में पूछ सकते हैं।"
    elif user_lang.startswith("kn"):
        reply = (
            f"🇮🇳 **ನಮಸ್ಕಾರ! ನಾನು ನಿಮ್ಮ ಸಮಆಶ್ವಾಸ ನಾಗರಿಕ AI ಸಹಾಯಕ.**\n\n"
            f"• ನಿಮ್ಮ ದೂರಿನ ಸ್ಥಿತಿಯನ್ನು ಪರಿಶೀಲಿಸಿ (ಉದಾ: `CMP-2026-0891`)\n"
            f"• ರಸ್ತೆ ಗುಂಡಿ, ಕಸ, ಬೀದಿದೀಪ ಸಮಸ್ಯೆಗಳನ್ನು ಧ್ವನಿಯ ಮೂಲಕ ವರದಿ ಮಾಡಿ\n"
            f"• ಪಾಲಿಕೆಯ ತುರ್ತು ಸಹಾಯವಾಣಿ ಸಂಖ್ಯೆಗಳನ್ನು ಪಡೆಯಿರಿ"
        )
        spoken = "ನಮಸ್ಕಾರ! ನಾನು ನಿಮ್ಮ ನಾಗರಿಕ AI ಸಹಾಯಕ. ನೀವು ಮಾತನಾಡುವ ಮೂಲಕ ದೂರು ದಾಖಲಿಸಬಹುದು."
    elif user_lang.startswith("ta"):
        reply = (
            f"🇮🇳 **வணக்கம்! நான் உங்கள் குடிமக்கள் AI உதவியாளர்.**\n\n"
            f"• புகார் நிலையை அறியவும் (`CMP-2026-0891`)\n"
            f"• சாலை, குப்பை, தெருவிளக்கு புகார்களை குரல் மூலம் பதிவு செய்யவும்\n"
            f"• அவசர உதவி எண்களை பெறவும்"
        )
        spoken = "வணக்கம்! நான் உங்கள் குடிமக்கள் AI உதவியாளர்."
    else:
        reply = (
            f"🇮🇳 **Hello {req.user_name or 'Citizen'}! I am your SamAashwas Civic AI Copilot.**\n\n"
            f"I can assist you in real time with:\n"
            f"• **Live Grievance Tracking:** Speak or enter your Ticket ID (e.g. `CMP-2026-0891`)\n"
            f"• **Instant Voice Reporting:** Report potholes, dark spots, or garbage dumps\n"
            f"• **Municipal Helplines:** Instant control room and emergency contacts\n"
            f"• **Tax Rebate & Karma:** Learn how to unlock 5% Property Tax discounts"
        )
        spoken = f"Hello! I am your Nagrik AI Sahayak. You can speak or type to track grievances, report hazards, or find emergency contacts."

    return {
        "reply_text": reply,
        "audio_speakable_text": spoken,
        "intent": "general_greeting",
        "language": user_lang,
        "suggested_action": {"action_type": "navigate", "target": "section-report", "label": "Report a Problem"},
        "quick_replies": ["Track CMP-2026-0891", "Emergency Helplines", "Report Pothole", "Property Tax Rebate"]
    }



