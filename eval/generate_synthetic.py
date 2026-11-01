import json
import random
import os
from typing import List, Dict, Any

random.seed(42)

LANGUAGES = ["English", "Hinglish", "Hindi", "Telugu", "Tamil", "Kannada", "Bengali", "Urdu"]

TEMPLATES_BY_DEPT = {
    "Electrical & Streetlighting": {
        "English": ["Streetlight pole broken and sparking near gate", "Dark spot on main cross streetlamp not working for 3 days"],
        "Hinglish": ["Bhaiya street light 4 din se band hai andhera ho raha hai", "Bijli ka khamba tut gaya hai wire latak rahi hai"],
        "Hindi": ["गली में स्ट्रीट लाइट बंद है रात को अंधेरा रहता है", "बिजली का खंभा झुक गया है तार लटक रहे हैं"],
        "Telugu": ["వీధి దీపం వెలగడం లేదు రాత్రి చీకటిగా ఉంది", "విద్యుత్ స్తంభం విరిగిపోయింది వైర్లు వేలాడుతున్నాయి"],
        "Tamil": ["தெரு விளக்கு எரியவில்லை இரவு முழுவதும் இருட்டாக உள்ளது", "மின் கம்பம் உடைந்து கம்பி தொங்குகிறது"],
        "Kannada": ["ಬೀದಿ ದೀಪ ಕೆಟ್ಟು ಹೋಗಿದೆ ರಾತ್ರಿ ಕತ್ತಲೆಯಾಗಿದೆ", "ವಿದ್ಯುತ್ ಕಂಬ ಮುರಿದು ತಂತಿ ಕೆಳಗೆ ಬಿದ್ದಿದೆ"],
        "Bengali": ["রাস্তার আলো জ্বলছে না রাতে অন্ধকার থাকে", "বিদ্যুতের খুঁটি ভেঙে গেছে তার ঝুলছে"],
        "Urdu": ["اسٹریٹ لائٹ بند ہے رات کو اندھیرا رہتا ہے", "بجلی کا کھمبا ٹوٹ گیا ہے تاریں لٹک رہی ہیں"]
    },
    "Sanitation & Solid Waste": {
        "English": ["Overflowing garbage dumpster and severe foul smell", "Plastic waste and trash pile not cleared for a week"],
        "Hinglish": ["Kachra gadi nahi aayi 4 din se sadak pe bada kude ka dher hai", "Safai nahi hui hai bohot gandi badbu aa rahi hai"],
        "Hindi": ["कूड़ेदान भर गया है कचरा सड़क पर फैल रहा है", "सफाई कर्मचारी तीन दिन से नहीं आया बहुत बदबू है"],
        "Telugu": ["చెత్త కుండీ నిండిపోయింది రోడ్డుపై చెత్త పేరుకుపోయింది", "పారిశుధ్య కార్మికుడు రావడం లేదు తీవ్ర దుర్వాసన వస్తోంది"],
        "Tamil": ["குப்பைத்தொட்டி நிரம்பி வழிகிறது துப்புரவு பணி செய்யப்படவில்லை", "தெருவில் குப்பைக் குவியல் நாற்றம் தாங்க முடியவில்லை"],
        "Kannada": ["ಕಸದ ಡಬ್ಬಿ ತುಂಬಿ ತುಳುಕುತ್ತಿದೆ ಸ್ವಚ್ಛತೆ ಮಾಡಿಲ್ಲ", "ರಸ್ತೆಯಲ್ಲಿ ಕಸದ ರಾಶಿ ಬಿದ್ದಿದೆ ವಿಪರೀತ ದುರ್ವಾಸನೆ"],
        "Bengali": ["ডাস্টবিন উপচে আবর্জনা রাস্তায় ছড়াচ্ছে", "ময়লার স্তূপ জমে আছে তীব্র দুর্গন্ধ ছড়াচ্ছে"],
        "Urdu": ["کوڑے دان سے کچرا باہر گر رہا ہے صفائی نہیں ہوئی", "گلی میں کچرے کے ڈھیر لگے ہیں سخت بدبو آ رہی ہے"]
    },
    "Water Supply & Sewage": {
        "English": ["Drinking water pipeline burst water flooding road", "Sewer line clogged and foul black sewage overflowing"],
        "Hinglish": ["Paani ki pipeline phat gayi hai peene ka paani beh raha hai", "Gali mein gutter overflow ho raha hai ganda paani bhara hai"],
        "Hindi": ["सीवर लाइन जाम हो गई है गटर का गंदा पानी सड़क पर बह रहा है", "पानी की मुख्य पाइपलाइन टूट गई है जलभराव हो गया है"],
        "Telugu": ["మంచినీటి పైప్‌లైన్ పగిలిపోయింది నీరు వృధాగా పోతోంది", "మురుగు కాలువ పొంగిపొర్లుతోంది రోడ్డుపై మురుగునీరు"],
        "Tamil": ["குடிநீர் குழாய் உடைந்து தண்ணீர் வீணாகிறது", "சாக்கடை நீர் நிரம்பி வழிகிறது தெருவில் துர்நாற்றம்"],
        "Kannada": ["ಕುಡಿಯುವ ನೀರಿನ ಕೊಳವೆ ಒಡೆದು ನೀರು ಪೋಲಾಗುತ್ತಿದೆ", "ಒಳಚರಂಡಿ ಕಟ್ಟಿಕೊಂಡು ಗಲೀಜು ನೀರು ರಸ್ತೆಗೆ ಹರಿಯುತ್ತಿದೆ"],
        "Bengali": ["পানের জলের পাইপ ফেটে গেছে রাস্তায় জল জমছে", "নর্দমা উপচে নোংরা জল রাস্তায় বইছে"],
        "Urdu": ["پینے کے پانی کی پائپ لائن پھٹ گئی ہے سڑک پر پانی جمع ہے", "سیوریج کا گٹر ابل رہا ہے گندا پانی گلی میں پھیل گیا"]
    },
    "Roads & Traffic Infrastructure": {
        "English": ["Deep dangerous pothole on main road causing bike skids", "Broken asphalt crater in front of bus stand"],
        "Hinglish": ["Sadak pe bada gaddha ho gaya hai bike gir sakti hai", "Road tut gayi hai crater ban gaya hai accident hone ka khatra hai"],
        "Hindi": ["सड़क पर गहरा गड्ढा है दोपहिया वाहन गिर रहे हैं", "रोड टूट गई है बड़ा गड्ढा बन गया है तुरंत मरम्मत करें"],
        "Telugu": ["రోడ్డుపై పెద్ద గుంత ఉంది బైకులు జారిపడుతున్నాయి", "రహదారి దెబ్బతింది ప్రమాదాలు జరుగుతున్నాయి వెంటనే బాగుచేయండి"],
        "Tamil": ["சாலையில் ஆழமான குழி உள்ளது இருசக்கர வாகனங்கள் விபத்துக்குள்ளாகின்றன", "தார் சாலை சேதமடைந்துள்ளது உடனடியாக செப்பனிடவும்"],
        "Kannada": ["ರಸ್ತೆಯಲ್ಲಿ ಆಳವಾದ ಗುಂಡಿ ಬಿದ್ದಿದೆ ಬೈಕ್‌ಗಳು ಜಾರಿ ಬೀಳುತ್ತಿವೆ", "ಡಾಂಬರು ರಸ್ತೆ ಕಿತ್ತುಹೋಗಿ ದೊಡ್ಡ ಹಳ್ಳ ಬಿದ್ದಿದೆ"],
        "Bengali": ["রাস্তায় গভীর গর্ত হয়েছে বাইক পিছলে পড়ে যাচ্ছে", "পিচ ঢালা রাস্তা ভেঙে গিয়ে বড় খানাখন্দ তৈরি হয়েছে"],
        "Urdu": ["سڑک پر گہرا گڑھا ہے حادثات کا خدشہ ہے", "روڈ ٹوٹ پھوٹ کا شکار ہے فوری مرمت کی ضرورت ہے"]
    },
    "Encroachment & Town Planning": {
        "English": ["Illegal hawkers have blocked the entire pedestrian footpath", "Shopkeeper has extended permanent concrete ramp on public road"],
        "Hinglish": ["Footpath par dukandar ne kabza kar liya hai chalne ki jagah nahi hai", "Illegal thela laga ke poora rasta block kar diya hai"],
        "Hindi": ["फुटपाथ पर अवैध कब्जा कर लिया गया है राहगीरों को परेशानी हो रही है", "सड़क पर दुकानदारों ने अतिक्रमण कर लिया है"],
        "Telugu": ["ఫుట్‌పాత్‌ను ఆక్రమించి దుకాణాలు పెట్టారు నడవడానికి దారి లేదు", "ప్రజా రహదారిపై అక్రమ నిర్మాణాలు చేపట్టారు"],
        "Tamil": ["நடைபாதையை ஆக்கிரமித்து கடைகள் வைக்கப்பட்டுள்ளன", "பொது சாலையில் சட்டவிரోத ஆக்கிரமிப்பு செய்யப்பட்டுள்ளது"],
        "Kannada": ["ಪಾದಚಾರಿ ಮಾರ್ಗವನ್ನು ಅತಿಕ್ರಮಣ ಮಾಡಿ ಅಂಗಡಿಗಳನ್ನು ಇಡಲಾಗಿದೆ", "ಸಾರ್ವजनिक ರಸ್ತೆಯನ್ನು ಒತ್ತುವರಿ ಮಾಡಿಕೊಂಡಿದ್ದಾರೆ"],
        "Bengali": ["ফুটপাথ দখল করে দোকান বসানো হয়েছে হাঁটার জায়গা নেই", "সরকারি রাস্তায় বেআইনি দখলদারি চলছে"],
        "Urdu": ["فٹ پاتھ پر غیر قانونی تجاوزات ہیں پیدل چلنا محال ہے", "دکانداروں نے سڑک پر قبضہ کر لیا ہے"]
    },
    "Health & Vector Control": {
        "English": ["Stagnant puddle mosquito breeding dengue fever outbreak in locality", "Urgent municipal fogging needed for malaria and mosquito control"],
        "Hinglish": ["Macchar bohot ho gaye hain dengue ka khatra hai fogging karwao", "Gande paani mein mosquito larvae panap rahe hain dawa chhidko"],
        "Hindi": ["इलाके में मच्छर बहुत बढ़ गए हैं डेंगू का प्रकोप है फॉगिंग करवाएं", "ठहरे हुए पानी में मच्छर पनप रहे हैं कीटनाशक का छिड़काव करें"],
        "Telugu": ["దోమలు తీవ్రంగా పెరిగిపోయాయి డెంగ్యూ వ్యాపిస్తోంది ఫాగింగ్ చేయించండి", "నిలిచిన నీటిలో దోమల ఉత్పత్తి జరుగుతోంది మందు చల్లించండి"],
        "Tamil": ["கொசுத் தொல்லை அதிகமாக உள்ளது டெங்கு பரவும் அபாயம் மருந்து தெளிக்கவும்", "தேங்கி நிற்கும் நீரில் கொசுக்கள் உற்பத்தியாகின்றன"],
        "Kannada": ["ಸೊಳ್ಳೆಗಳ ಕಾಟ ಹೆಚ್ಚಾಗಿದೆ ಡೆಂಗ್ಯೂ ಹರಡುವ ಭೀತಿ ಫಾಗಿಂಗ್ ಮಾಡಿಸಿ", "ನಿಂತ ನೀರಿನಲ್ಲಿ ಸೊಳ್ಳೆಗಳು ಉತ್ಪತ್ತಿಯಾಗುತ್ತಿವೆ ಔಷಧ ಸಿಂಪಡಿಸಿ"],
        "Bengali": ["মশার উপদ্রব খুব বেড়ে গেছে ডেঙ্গুর আতঙ্ক রয়েছে ফগিং দরকার", "জমা জলে মশার লার্ভা জন্মাচ্ছে কীটনাশক স্প্রে করুন"],
        "Urdu": ["علاقے میں مچھروں کی بھرمار ہے ڈینگی پھیل رہا ہے دوا کا چھڑکاؤ کریں", "کھڑے پانی میں مچھر پیدا ہو رہے ہیں فوری اقدامات کریں"]
    }
}

HARD_NEGATIVES = [
    # Explicit Negations (suppressed civic queries)
    {"text": "The road here is perfectly fine and there is no pothole at all", "expected_dept": "Triage & Verification Queue", "is_abstained": True, "trap": "negation"},
    {"text": "Kachra nahi hai yahan, safai achhi tarah se ho chuki hai", "expected_dept": "Triage & Verification Queue", "is_abstained": True, "trap": "negation"},
    {"text": "Street light has been fixed and is now working fine, no issue", "expected_dept": "Triage & Verification Queue", "is_abstained": True, "trap": "negation"},
    {"text": "There is no water leakage or pipeline rupture in our lane", "expected_dept": "Triage & Verification Queue", "is_abstained": True, "trap": "negation"},
    {"text": "No mosquito breeding here, fogging was done yesterday", "expected_dept": "Triage & Verification Queue", "is_abstained": True, "trap": "negation"},
    # Non-Civic Out-of-Domain Spams
    {"text": "Order one large pepperoni pizza with cheesy garlic bread", "expected_dept": "Triage & Verification Queue", "is_abstained": True, "trap": "spam"},
    {"text": "What is the latest score in the India vs Australia cricket match?", "expected_dept": "Triage & Verification Queue", "is_abstained": True, "trap": "spam"},
    {"text": "Please recharge my mobile number with 2GB daily data pack", "expected_dept": "Triage & Verification Queue", "is_abstained": True, "trap": "spam"},
    {"text": "Looking for 2BHK flat for rent near metro station", "expected_dept": "Triage & Verification Queue", "is_abstained": True, "trap": "spam"},
    {"text": "Can you book an Ola cab from airport to railway station?", "expected_dept": "Triage & Verification Queue", "is_abstained": True, "trap": "spam"},
    # Wrong Door Queries (Non-ULB jurisdictions)
    {"text": "Deep crater on NH-44 national highway near expressway toll plaza", "expected_dept": "Roads & Traffic Infrastructure", "is_wrong_door": True, "expected_jurisdiction": "NHAI (National Highways Authority of India)", "trap": "wrong_door"},
    {"text": "Massive water logging inside train station platform and railway track", "expected_dept": "Water Supply & Sewage", "is_wrong_door": True, "expected_jurisdiction": "Indian Railways", "trap": "wrong_door"},
    {"text": "132kv electrical grid substation failure total blackout across state transmission lines", "expected_dept": "Electrical & Streetlighting", "is_wrong_door": True, "expected_jurisdiction": "State Power Transmission Grid / DISCOM High Tension", "trap": "wrong_door"},
    {"text": "Road maintenance required inside Army Cantonment area military camp gate", "expected_dept": "Roads & Traffic Infrastructure", "is_wrong_door": True, "expected_jurisdiction": "Cantonment Board / Ministry of Defence", "trap": "wrong_door"}
]

def generate_benchmark_dataset(num_samples: int = 1000) -> List[Dict[str, Any]]:
    dataset = []
    
    # 1. Generate core multilingual complaints
    depts = list(TEMPLATES_BY_DEPT.keys())
    samples_per_dept = (num_samples - len(HARD_NEGATIVES) * 4) // len(depts)
    
    cluster_counter = 1
    sample_id = 1

    for dept in depts:
        base_lat = random.uniform(12.90, 13.05) # Bengaluru coordinates bounding box
        base_lon = random.uniform(77.55, 77.70)
        cluster_lang = random.choice(LANGUAGES)
        for i in range(samples_per_dept):
            is_dup = (i % 3 != 0)
            
            if is_dup:
                lang = cluster_lang
                templates = TEMPLATES_BY_DEPT[dept][lang]
                text = random.choice(templates)
                cluster_id = f"CLUSTER-{dept[:3].upper()}-{cluster_counter}"
                # Displace slightly within category radius (10-25m)
                d_lat = random.uniform(-0.00015, 0.00015)
                d_lon = random.uniform(-0.00015, 0.00015)
            else:
                cluster_counter += 1
                cluster_lang = random.choice(LANGUAGES)
                lang = cluster_lang
                templates = TEMPLATES_BY_DEPT[dept][lang]
                text = random.choice(templates)
                cluster_id = f"CLUSTER-{dept[:3].upper()}-{cluster_counter}"
                base_lat = random.uniform(12.90, 13.05)
                base_lon = random.uniform(77.55, 77.70)
                d_lat, d_lon = 0.0, 0.0

            dataset.append({
                "id": f"BENCH-{sample_id:04d}",
                "text": text,
                "expected_department": dept,
                "language": lang,
                "lat": round(base_lat + d_lat, 6),
                "lon": round(base_lon + d_lon, 6),
                "cluster_id": cluster_id,
                "is_duplicate": is_dup,
                "is_abstained": False,
                "is_wrong_door": False,
                "trap": "none"
            })
            sample_id += 1

    # 2. Add Hard Negatives multiple times
    for _ in range(4):
        for neg in HARD_NEGATIVES:
            dataset.append({
                "id": f"BENCH-{sample_id:04d}",
                "text": neg["text"],
                "expected_department": neg.get("expected_dept", "Triage & Verification Queue"),
                "language": "English" if "Kachra" not in neg["text"] else "Hinglish",
                "lat": 12.9716,
                "lon": 77.6412,
                "cluster_id": f"NEG-{sample_id}",
                "is_duplicate": False,
                "is_abstained": neg.get("is_abstained", False),
                "is_wrong_door": neg.get("is_wrong_door", False),
                "expected_jurisdiction": neg.get("expected_jurisdiction"),
                "trap": neg.get("trap", "negation")
            })
            sample_id += 1

    random.shuffle(dataset)
    return dataset

if __name__ == "__main__":
    os.makedirs("data", exist_ok=True)
    bench_data = generate_benchmark_dataset(1000)
    out_path = os.path.join("data", "benchmark_dataset.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(bench_data, f, indent=2, ensure_ascii=False)
    print(f"Generated {len(bench_data)} benchmark items to {out_path}")
