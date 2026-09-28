import random
import json
import os
from typing import List, Dict, Any
from ..models.schemas import ComplaintCreateRequest, ChannelEnum
from .database import db

# Realistic Hinglish and English templates across departments
TEMPLATES = [
    # Water Supply & Sewage
    {
        "dept": "Water Supply & Sewage",
        "cluster_root": "Ward 2 gali mein sewer overflow ho raha hai, badbu se rehna mushkil ho gaya",
        "variations": [
            "Bhaiya sewer ka ganda paani sadak pe beh raha hai near Sharma General Store",
            "Sewer line block ho gayi hai, dirty black water overflowing on road Ward 2",
            "Urgent: Sewage drain chocked and stinking badly opposite Sharma store",
            "Gutter overflow ho raha hai, please jaldi safai karwao accident ho sakta hai",
            "Main sewer pipeline leakage in ward 2 near general store, road flooded with sewage"
        ],
        "base_lat": 12.9352,
        "base_lon": 77.6245,
        "ward": "Koramangala 4th Block"
    },
    # Electrical & Streetlighting
    {
        "dept": "Electrical & Streetlighting",
        "cluster_root": "Street light 4 din se band hai near metro pillar 108, pura andhera hai",
        "variations": [
            "Road light khamba not working since 4 days near pillar 108 Indiranagar",
            "Bhaiya streetlights are off at night, very dark and unsafe near metro pillar",
            "No light on 100 feet road near pillar 108, please repair bulb quickly",
            "Dark spot due to dead streetlight bulb near pillar 108 Indiranagar",
            "Streetlight pole sparking and turned completely off near metro line"
        ],
        "base_lat": 12.9716,
        "base_lon": 77.6412,
        "ward": "Indiranagar Central"
    },
    # Roads & Traffic Infrastructure
    {
        "dept": "Roads & Traffic Infrastructure",
        "cluster_root": "Main road par huge pothole hai accident hone ka chance hai, 27th Main HSR",
        "variations": [
            "Dangerous deep pothole on 27th main HSR layout, bikes slipping daily",
            "Bada gaddha ban gaya hai road pe, two-wheeler girte girte bacha",
            "Road damaged with massive crater near HSR petrol pump, please patch",
            "Asphalt washed away, giant pothole causing major traffic slowdown 27th main",
            "Very deep gaddha on main road sector 7, repair urgently"
        ],
        "base_lat": 12.9121,
        "base_lon": 77.6446,
        "ward": "HSR Layout Sector 7"
    },
    # Sanitation & Solid Waste
    {
        "dept": "Sanitation & Solid Waste",
        "cluster_root": "Kachra gadi nahi aayi 3 din se, community bin overflowing with waste",
        "variations": [
            "Garbage dump not cleared for 3 days near Bellandur lake junction, dog menace",
            "Bohot kachra jama ho gaya hai corner pe, flies and mosquitoes everywhere",
            "Waste collection truck missing since 3 days, garbage piling up",
            "Safai karmachari nahi aa rahe, huge garbage heap on main corner Bellandur",
            "Rotting solid waste lying open on street, terrible smell please clear"
        ],
        "base_lat": 12.9304,
        "base_lon": 77.6784,
        "ward": "Bellandur Outer Ring"
    },
    # Health & Vector Control
    {
        "dept": "Health & Vector Control",
        "cluster_root": "Stagnant waterlogging after rain, mosquito breeding heavy near 8th cross park",
        "variations": [
            "Paani bhara hua hai park ke paas, bohot macchar ho rahe hain dengue risk",
            "Need immediate anti-larval fogging, water accumulated on empty plot 8th cross",
            "Heavy mosquito swarm due to open stagnant water pond near Malleshwaram park",
            "Please send fogging team, high risk of malaria in our lane 8th cross",
            "Waterlogged plot creating huge mosquito menace for all residents"
        ],
        "base_lat": 13.0067,
        "base_lon": 77.5694,
        "ward": "Malleshwaram 8th Cross"
    }
]

CITIZEN_NAMES = [
    "Rahul Sharma", "Pooja Verma", "Amit Patel", "Deepa Rao", "Vikram Singh",
    "Sneha Reddy", "Arun Kumar", "Ananya Iyer", "Karthik Nair", "Sunita Gupta",
    "Mohammed Zeeshan", "Meenakshi Sundaram", "Ramesh Joshi", "Priyanka Das"
]

def generate_synthetic_dataset(total_count: int = 1000) -> List[Dict[str, Any]]:
    """
    Generate 1,000+ realistic code-mixed municipal grievances with natural spatial clusters.
    """
    dataset = []
    
    # 60% of complaints belong to 5 major municipal incident clusters (simulating duplicate flooding)
    # 40% are distributed unique complaints across the city
    
    for i in range(total_count):
        cluster_idx = i % len(TEMPLATES)
        cluster = TEMPLATES[cluster_idx]
        
        is_cluster_duplicate = (random.random() < 0.65)
        
        if is_cluster_duplicate:
            text = random.choice([cluster["cluster_root"]] + cluster["variations"])
            # Slight GPS noise within 200 meters (~0.0018 degrees)
            lat = cluster["base_lat"] + random.uniform(-0.0012, 0.0012)
            lon = cluster["base_lon"] + random.uniform(-0.0012, 0.0012)
        else:
            # Independent grievance
            text = random.choice(cluster["variations"]) + f" (Ward {random.randint(1, 15)})"
            lat = cluster["base_lat"] + random.uniform(-0.02, 0.02)
            lon = cluster["base_lon"] + random.uniform(-0.02, 0.02)

        phone = f"98{random.randint(10000000, 99999999)}"
        name = random.choice(CITIZEN_NAMES)
        channel = random.choice([ChannelEnum.WHATSAPP, ChannelEnum.WEB_PORTAL, ChannelEnum.MOBILE_APP])

        dataset.append({
            "id": f"SYN-{i+1:04d}",
            "raw_text": text,
            "lat": round(lat, 6),
            "lon": round(lon, 6),
            "citizen_name": name,
            "citizen_phone": phone,
            "channel": channel.value,
            "ward_hint": cluster["ward"]
        })

    return dataset

def seed_database_and_export():
    """
    Generate the 1,000 complaints dataset, save to data/synthetic_complaints_1000.json,
    and seed the initial database with a representative sample for fast startup.
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    data_file = os.path.join(base_dir, "data", "synthetic_complaints_1000.json")

    if os.path.exists(data_file):
        try:
            with open(data_file, "r", encoding="utf-8") as f:
                dataset = json.load(f)
        except Exception:
            dataset = generate_synthetic_dataset(1000)
            with open(data_file, "w", encoding="utf-8") as f:
                json.dump(dataset, f, indent=2, ensure_ascii=False)
    else:
        dataset = generate_synthetic_dataset(1000)
        os.makedirs(os.path.dirname(data_file), exist_ok=True)
        with open(data_file, "w", encoding="utf-8") as f:
            json.dump(dataset, f, indent=2, ensure_ascii=False)

    print(f"Loaded {len(dataset)} synthetic complaints from {data_file}")

    # Seed the in-memory database with the first 45 complaints to illustrate clustering
    for item in dataset[:45]:
        req = ComplaintCreateRequest(
            raw_text=item["raw_text"],
            lat=item["lat"],
            lon=item["lon"],
            citizen_name=item["citizen_name"],
            citizen_phone=item["citizen_phone"],
            channel=ChannelEnum(item["channel"]),
            ward_hint=item.get("ward_hint")
        )
        db.submit_complaint(req)

    print(f"Seeded active database with {len(db.complaints)} complaints across {len(db.master_tickets)} master tickets.")
