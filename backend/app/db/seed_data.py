import random
import json
import os
from typing import List, Dict, Any
from ..models.schemas import ComplaintCreateRequest, ChannelEnum
from .database import db

# Realistic Hinglish, Indic and English templates across departments and all 8 major Indian metros
TEMPLATES = [
    # 1. Bengaluru (BBMP)
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
    # 2. Delhi (MCD)
    {
        "dept": "Water Supply & Sewage",
        "cluster_root": "Karol Bagh main market sewer pipeline leakage and black water on road",
        "variations": [
            "Karol Bagh Rajendra Nagar road flooded with sewer drainage water near metro",
            "Ganda paani drain block ho gaya hai near Karol Bagh metro station",
            "Main sewer overflow at Karol Bagh market, terrible smell please clear",
            "Drainage pipeline leakage opposite Karol Bagh shopping complex"
        ],
        "base_lat": 28.6514,
        "base_lon": 77.1907,
        "ward": "Karol Bagh - Rajendra Nagar"
    },
    {
        "dept": "Water Supply & Sewage",
        "cluster_root": "Civil Lines low-lying zone Yamuna waterlogging risk after rain near Kashmiri Gate",
        "variations": [
            "Severe waterlogging near Kashmiri gate bus depot Civil Lines",
            "Road flooded 2 feet deep near Civil Lines police post, sumps not working",
            "Drainage backflow hazard in Civil Lines residential lane near Yamuna bank"
        ],
        "base_lat": 28.6814,
        "base_lon": 77.2228,
        "ward": "Civil Lines - Kashmiri Gate"
    },
    {
        "dept": "Sanitation & Solid Waste",
        "cluster_root": "Rohini Sector 15 community garbage bin overflowing with rotting waste and dog menace",
        "variations": [
            "Kachra dump not cleared since 3 days in Rohini Sector 15 market",
            "Open garbage heap attracting stray cattle and dogs near Prashant Vihar",
            "Dhalao overflow near Rohini park, please send municipal tipper immediately"
        ],
        "base_lat": 28.7166,
        "base_lon": 77.1189,
        "ward": "Rohini Sector 15 - Prashant Vihar"
    },
    # 3. Mumbai (BMC)
    {
        "dept": "Sanitation & Solid Waste",
        "cluster_root": "Pali Hill corner open garbage heap blocking footpath and stinking Bandra West",
        "variations": [
            "Bandra West garbage collection vehicle not arrived for 2 days near Pali Hill",
            "Municipal waste bins overflowing on Pali Hill road Bandra",
            "Foul smell from uncollected solid waste near Bandra residential junction"
        ],
        "base_lat": 19.0596,
        "base_lon": 72.8295,
        "ward": "Bandra West - Pali Hill"
    },
    {
        "dept": "Roads & Traffic Infrastructure",
        "cluster_root": "Dangerous crater and pothole cluster on Andheri-Kurla road near MIDC signal",
        "variations": [
            "Andheri East main road damaged with massive potholes slowing traffic",
            "Road cave-in near MIDC signal Andheri, bikes slipping in rain",
            "Urgent asphalt repair needed on Andheri arterial industrial road"
        ],
        "base_lat": 19.1136,
        "base_lon": 72.8697,
        "ward": "Andheri East - MIDC"
    },
    {
        "dept": "Water Supply & Sewage",
        "cluster_root": "BMC main drinking water pipeline burst near Shivaji Park Dadar West clean water wasting",
        "variations": [
            "Lakhs of liters of clean water wasting from cracked pipeline near Dadar",
            "Drinking water gushing out on Shivaji Park road, no pressure in taps",
            "Urgent: Water supply line ruptured near Dadar West municipal garden"
        ],
        "base_lat": 19.0178,
        "base_lon": 72.8478,
        "ward": "Dadar West - Shivaji Park"
    },
    # 4. Pune (PMC)
    {
        "dept": "Water Supply & Sewage",
        "cluster_root": "Shivajinagar FC Road nullah blocked with debris causing dirty water pooling",
        "variations": [
            "Mutha river tributary drain choked near FC road Shivajinagar",
            "Storm drain blocked near Ferguson College gate, foul smell",
            "Gutter line choke in Shivajinagar lane, immediate desilting required"
        ],
        "base_lat": 18.5314,
        "base_lon": 73.8446,
        "ward": "Shivajinagar - FC Road"
    },
    {
        "dept": "Roads & Traffic Infrastructure",
        "cluster_root": "Severe road subsidence and crater on Paud road Kothrud near corner",
        "variations": [
            "Dangerous pothole cluster on Kothrud main junction, accidents risk",
            "Paud road asphalt stripped off, two wheelers skidding daily",
            "Deep gaddha on Kothrud arterial road, repair urgently"
        ],
        "base_lat": 18.5074,
        "base_lon": 73.8077,
        "ward": "Kothrud Central"
    },
    # 5. Chennai (GCC)
    {
        "dept": "Water Supply & Sewage",
        "cluster_root": "Stormwater drain desilting choked opposite Panagal Park T. Nagar wastewater pooling",
        "variations": [
            "T. Nagar Usman road drain overflowing with black stagnant water near shopping area",
            "Severe sewage blockage in Panagal park shopping corridor GCC ward",
            "Wastewater stagnation causing huge mosquito menace in T. Nagar"
        ],
        "base_lat": 13.0418,
        "base_lon": 80.2341,
        "ward": "T. Nagar - Panagal Park"
    },
    {
        "dept": "Electrical & Streetlighting",
        "cluster_root": "Streetlight pole sparking and dark spot near Besant Nagar beach Adyar",
        "variations": [
            "Adyar Besant Nagar road lights not working, complete darkness",
            "Dangerous exposed wire on lamppost near Adyar bus depot",
            "Dark spot due to blown LED street fixtures along beach stretch"
        ],
        "base_lat": 13.0012,
        "base_lon": 80.2565,
        "ward": "Adyar - Besant Nagar"
    },
    # 6. Hyderabad (GHMC)
    {
        "dept": "Water Supply & Sewage",
        "cluster_root": "Jubilee Hills Road 36 nala overflow risk due to canal debris and silt",
        "variations": [
            "Strategic nala channel choked near Jubilee Hills checkpost",
            "Waterlogging and drain blockage in Jubilee Hills commercial road",
            "Heavy sewage smell and overflowing storm canal Jubilee Hills"
        ],
        "base_lat": 17.4319,
        "base_lon": 78.4073,
        "ward": "Jubilee Hills - Road 36"
    },
    {
        "dept": "Roads & Traffic Infrastructure",
        "cluster_root": "Cyber towers junction deep pothole damaging vehicles during rush hour Hitec City",
        "variations": [
            "Hitec City main road craters causing massive IT corridor gridlock",
            "Asphalt washed away near Cyber Gateway, deep hazardous trench",
            "Immediate pothole repair needed on Hitec City flyover ramp"
        ],
        "base_lat": 17.4474,
        "base_lon": 78.3762,
        "ward": "Hitec City - Cyber Towers"
    },
    # 7. Lucknow (LMC)
    {
        "dept": "Electrical & Streetlighting",
        "cluster_root": "Hazratganj market heritage walkway ornamental lamp broken and dark spot",
        "variations": [
            "Hazratganj heritage lamps not functioning since 3 nights",
            "Dark spot in main shopping arcade Hazratganj due to bulb failure",
            "Exposed electrical cable on Lucknow heritage lamppost"
        ],
        "base_lat": 26.8536,
        "base_lon": 80.9452,
        "ward": "Hazratganj Heritage"
    },
    {
        "dept": "Sanitation & Solid Waste",
        "cluster_root": "Vibhuti Khand Gomti Nagar open drain overflowing on road near commercial complex",
        "variations": [
            "Gomti riverfront drain choke causing wastewater accumulation",
            "Open garbage and drain blockage in Vibhuti Khand Gomti Nagar",
            "Foul smell from uncleaned municipal nala Gomti Nagar"
        ],
        "base_lat": 26.8568,
        "base_lon": 81.0028,
        "ward": "Gomti Nagar - Vibhuti Khand"
    },
    # 8. Kolkata (KMC)
    {
        "dept": "Water Supply & Sewage",
        "cluster_root": "Park Street storm drain dewatering pump tripping water accumulation warning",
        "variations": [
            "Park Street Camac street crossing waterlogged after morning showers",
            "KEIIP drainage sump not operating at full speed Park Street",
            "Underground drainage line choked with silt on Park Street"
        ],
        "base_lat": 22.5513,
        "base_lon": 88.3526,
        "ward": "Park Street - Camac Street"
    },
    {
        "dept": "Roads & Traffic Infrastructure",
        "cluster_root": "Salt Lake Sector V IT hub main artery major asphalt potholes near techno junction",
        "variations": [
            "Dangerous deep craters near Sector V metro station Salt Lake",
            "Asphalt disintegrated on Kolkata IT hub arterial connector",
            "Heavy traffic slowdown due to damaged road surface Sector V"
        ],
        "base_lat": 22.5867,
        "base_lon": 88.4178,
        "ward": "Salt Lake Sector V"
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

REPRESENTATIVE_MULTI_CITY_COMPLAINTS = [
    # 1. Bengaluru (BBMP) - preserves SYN-0001, SYN-0002, SYN-0003
    {
        "id": "SYN-0001",
        "raw_text": "Urgent: Sewage drain chocked and stinking badly opposite Sharma store (Ward 2)",
        "lat": 12.9352,
        "lon": 77.6245,
        "citizen_name": "Ramesh Joshi",
        "citizen_phone": "9886786961",
        "channel": "web_portal",
        "ward_hint": "Koramangala 4th Block"
    },
    {
        "id": "SYN-0002",
        "raw_text": "Road light khamba not working since 4 days near pillar 108 Indiranagar (Ward 1)",
        "lat": 12.9716,
        "lon": 77.6412,
        "citizen_name": "Deepa Rao",
        "citizen_phone": "9813174267",
        "channel": "mobile_app",
        "ward_hint": "Indiranagar Central"
    },
    {
        "id": "SYN-0003",
        "raw_text": "Very deep gaddha on main road sector 7, repair urgently",
        "lat": 12.912761,
        "lon": 77.643728,
        "citizen_name": "Amit Patel",
        "citizen_phone": "9879106960",
        "channel": "mobile_app",
        "ward_hint": "HSR Layout Sector 7"
    },
    {
        "id": "SYN-BLR-04",
        "raw_text": "Bhaiya streetlights are completely off at night near metro pillar 108 Indiranagar",
        "lat": 12.9718,
        "lon": 77.6414,
        "citizen_name": "Karthik Nair",
        "citizen_phone": "9845012345",
        "channel": "whatsapp",
        "ward_hint": "Indiranagar Central"
    },
    # 2. Delhi (MCD)
    {
        "id": "SYN-DEL-01",
        "raw_text": "Karol Bagh main market sewer pipeline leakage and black water on road",
        "lat": 28.6514,
        "lon": 77.1907,
        "citizen_name": "Suresh Gupta",
        "citizen_phone": "9811023456",
        "channel": "web_portal",
        "ward_hint": "Karol Bagh - Rajendra Nagar"
    },
    {
        "id": "SYN-DEL-02",
        "raw_text": "Karol Bagh Rajendra Nagar road flooded with sewer drainage water near metro",
        "lat": 28.6516,
        "lon": 77.1909,
        "citizen_name": "Pooja Verma",
        "citizen_phone": "9811056789",
        "channel": "whatsapp",
        "ward_hint": "Karol Bagh - Rajendra Nagar"
    },
    {
        "id": "SYN-DEL-03",
        "raw_text": "Civil Lines low-lying area waterlogging danger near Yamuna ring road Kashmiri Gate",
        "lat": 28.6814,
        "lon": 77.2228,
        "citizen_name": "Devendra Tyagi",
        "citizen_phone": "9811099889",
        "channel": "web_portal",
        "ward_hint": "Civil Lines - Kashmiri Gate"
    },
    {
        "id": "SYN-DEL-04",
        "raw_text": "Rohini Sector 15 community garbage bin overflowing with rotting waste and dog menace",
        "lat": 28.7166,
        "lon": 77.1189,
        "citizen_name": "Pravesh Sharma",
        "citizen_phone": "9811044332",
        "channel": "mobile_app",
        "ward_hint": "Rohini Sector 15 - Prashant Vihar"
    },
    # 3. Mumbai (BMC)
    {
        "id": "SYN-MUM-01",
        "raw_text": "Pali Hill corner open garbage heap blocking footpath and stinking Bandra West",
        "lat": 19.0596,
        "lon": 72.8295,
        "citizen_name": "Farhan Merchant",
        "citizen_phone": "9820011223",
        "channel": "whatsapp",
        "ward_hint": "Bandra West - Pali Hill"
    },
    {
        "id": "SYN-MUM-02",
        "raw_text": "Bandra West municipal waste bins overflowing near Pali Hill junction",
        "lat": 19.0598,
        "lon": 72.8297,
        "citizen_name": "Zoya Akhtar",
        "citizen_phone": "9820044556",
        "channel": "web_portal",
        "ward_hint": "Bandra West - Pali Hill"
    },
    {
        "id": "SYN-MUM-03",
        "raw_text": "Dangerous crater and pothole cluster on Andheri-Kurla road near MIDC signal",
        "lat": 19.1136,
        "lon": 72.8697,
        "citizen_name": "Rohan Deshmukh",
        "citizen_phone": "9820077889",
        "channel": "mobile_app",
        "ward_hint": "Andheri East - MIDC"
    },
    {
        "id": "SYN-MUM-04",
        "raw_text": "BMC main drinking water pipeline burst near Shivaji Park Dadar West clean water wasting",
        "lat": 19.0178,
        "lon": 72.8478,
        "citizen_name": "Milind Vaidya",
        "citizen_phone": "9820099001",
        "channel": "web_portal",
        "ward_hint": "Dadar West - Shivaji Park"
    },
    # 4. Pune (PMC)
    {
        "id": "SYN-PUN-01",
        "raw_text": "Shivajinagar FC Road nullah blocked with debris causing dirty water pooling",
        "lat": 18.5314,
        "lon": 73.8446,
        "citizen_name": "Omkar Kulkarni",
        "citizen_phone": "9822011224",
        "channel": "web_portal",
        "ward_hint": "Shivajinagar - FC Road"
    },
    {
        "id": "SYN-PUN-02",
        "raw_text": "Severe road subsidence and crater on Paud road Kothrud near corner",
        "lat": 18.5074,
        "lon": 73.8077,
        "citizen_name": "Madhuri Patil",
        "citizen_phone": "9822033445",
        "channel": "mobile_app",
        "ward_hint": "Kothrud Central"
    },
    {
        "id": "SYN-PUN-03",
        "raw_text": "Smart LED streetlights completely off on Symbiosis road Viman Nagar pitch dark",
        "lat": 18.5679,
        "lon": 73.9143,
        "citizen_name": "Aditya Shinde",
        "citizen_phone": "9822055667",
        "channel": "whatsapp",
        "ward_hint": "Viman Nagar - Aeromall"
    },
    # 5. Chennai (GCC)
    {
        "id": "SYN-CHE-01",
        "raw_text": "Stormwater drain desilting choked opposite Panagal Park T. Nagar wastewater pooling",
        "lat": 13.0418,
        "lon": 80.2341,
        "citizen_name": "Senthil Nathan",
        "citizen_phone": "9840011225",
        "channel": "web_portal",
        "ward_hint": "T. Nagar - Panagal Park"
    },
    {
        "id": "SYN-CHE-02",
        "raw_text": "T. Nagar Usman road drain overflowing with black stagnant water near shopping area",
        "lat": 13.0420,
        "lon": 80.2343,
        "citizen_name": "Kavitha Raman",
        "citizen_phone": "9840033446",
        "channel": "whatsapp",
        "ward_hint": "T. Nagar - Panagal Park"
    },
    {
        "id": "SYN-CHE-03",
        "raw_text": "Drinking water supply pipeline leakage near Kapaleeshwarar temple tank Mylapore",
        "lat": 13.0339,
        "lon": 80.2676,
        "citizen_name": "Meenakshi Sundaram",
        "citizen_phone": "9840055667",
        "channel": "mobile_app",
        "ward_hint": "Mylapore - Kapaleeshwarar"
    },
    # 6. Hyderabad (GHMC)
    {
        "id": "SYN-HYD-01",
        "raw_text": "Jubilee Hills Road 36 nala overflow risk due to canal debris and silt",
        "lat": 17.4319,
        "lon": 78.4073,
        "citizen_name": "Venkatesh Rao",
        "citizen_phone": "9849011226",
        "channel": "web_portal",
        "ward_hint": "Jubilee Hills - Road 36"
    },
    {
        "id": "SYN-HYD-02",
        "raw_text": "Cyber towers junction deep pothole damaging vehicles during rush hour Hitec City",
        "lat": 17.4474,
        "lon": 78.3762,
        "citizen_name": "Srikanth Reddy",
        "citizen_phone": "9849033447",
        "channel": "mobile_app",
        "ward_hint": "Hitec City - Cyber Towers"
    },
    {
        "id": "SYN-HYD-03",
        "raw_text": "Charminar market lane secondary garbage accumulation needs urgent dumper tipper",
        "lat": 17.3616,
        "lon": 78.4747,
        "citizen_name": "Mohammed Zeeshan",
        "citizen_phone": "9849055668",
        "channel": "whatsapp",
        "ward_hint": "Charminar Old City"
    },
    # 7. Lucknow (LMC)
    {
        "id": "SYN-LKO-01",
        "raw_text": "Hazratganj market heritage walkway ornamental lamp broken and dark spot",
        "lat": 26.8536,
        "lon": 80.9452,
        "citizen_name": "Anurag Shukla",
        "citizen_phone": "9839011227",
        "channel": "web_portal",
        "ward_hint": "Hazratganj Heritage"
    },
    {
        "id": "SYN-LKO-02",
        "raw_text": "Vibhuti Khand Gomti Nagar open drain overflowing on road near commercial complex",
        "lat": 26.8568,
        "lon": 81.0028,
        "citizen_name": "Pradeep Tripathi",
        "citizen_phone": "9839033448",
        "channel": "whatsapp",
        "ward_hint": "Gomti Nagar - Vibhuti Khand"
    },
    {
        "id": "SYN-LKO-03",
        "raw_text": "Alambagh vegetable market waste piled up on corner unhygienic condition",
        "lat": 26.8184,
        "lon": 80.9082,
        "citizen_name": "Rajeshwar Yadav",
        "citizen_phone": "9839055669",
        "channel": "mobile_app",
        "ward_hint": "Alambagh Commercial"
    },
    # 8. Kolkata (KMC)
    {
        "id": "SYN-KOL-01",
        "raw_text": "Park Street storm drain dewatering pump tripping water accumulation warning",
        "lat": 22.5513,
        "lon": 88.3526,
        "citizen_name": "Debabrata Banerjee",
        "citizen_phone": "9830011228",
        "channel": "web_portal",
        "ward_hint": "Park Street - Camac Street"
    },
    {
        "id": "SYN-KOL-02",
        "raw_text": "Salt Lake Sector V IT hub main artery major asphalt potholes near techno junction",
        "lat": 22.5867,
        "lon": 88.4178,
        "citizen_name": "Subhashish Roy",
        "citizen_phone": "9830033449",
        "channel": "mobile_app",
        "ward_hint": "Salt Lake Sector V"
    },
    {
        "id": "SYN-KOL-03",
        "raw_text": "Posta Burrabazar narrow commercial lane sewer line burst and heavy stench",
        "lat": 22.5847,
        "lon": 88.3582,
        "citizen_name": "Gopal Agarwal",
        "citizen_phone": "9830055660",
        "channel": "whatsapp",
        "ward_hint": "Burrabazar Posta"
    }
]

def seed_database_and_export():
    """
    Generate or load the 1,000 complaints dataset, save to data/synthetic_complaints_1000.json,
    and seed the initial database with a representative Pan-India sample across all 8 major metros.
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    data_file = os.path.join(base_dir, "data", "synthetic_complaints_1000.json")

    dataset = []
    if os.path.exists(data_file):
        try:
            with open(data_file, "r", encoding="utf-8") as f:
                dataset = json.load(f)
        except Exception:
            dataset = []

    if not dataset or len(dataset) < 100:
        dataset = generate_synthetic_dataset(1000)
        os.makedirs(os.path.dirname(data_file), exist_ok=True)
        with open(data_file, "w", encoding="utf-8") as f:
            json.dump(dataset, f, indent=2, ensure_ascii=False)

    print(f"Loaded {len(dataset)} synthetic complaints from {data_file}")

    # Seed the in-memory database with representative complaints across all 8 major metros
    for item in REPRESENTATIVE_MULTI_CITY_COMPLAINTS:
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

    print(f"Seeded active database with {len(db.complaints)} complaints across {len(db.master_tickets)} master tickets in 8 metros.")
