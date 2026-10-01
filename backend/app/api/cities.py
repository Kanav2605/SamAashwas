from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any, Optional
from pydantic import BaseModel

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
