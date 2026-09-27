// Multi-Lingual Vernacular Translation Dictionary for CivicSense AI (SamAashwas)
// Supports: English (en), हिन्दी (hi), Hinglish (hg), ಕನ್ನಡ (kn), தமிழ் (ta)

const I18N_TRANSLATIONS = {
  en: {
    brand_sub: "SamAashwas Municipal Intelligence Platform",
    ulb_badge: "ULB Live Command Center",
    tab_command_center: "Officer Command Center",
    tab_predictive_view: "Predictive Risk Index",
    tab_jan_sunwai: "Jan Sunwai & Ward Sabha",
    tab_citizen_portal: "Citizen Web Portal",
    tab_whatsapp_bot: "WhatsApp Bot Demo",
    
    kpi_total_reports: "Total Citizen Reports",
    kpi_total_sub: "Across WhatsApp, App & Portal",
    kpi_master_tickets: "Active Master Incidents",
    kpi_master_sub: "Auto-routed to Ward Engineers",
    kpi_dedup_rate: "Deduplication Rate",
    kpi_dedup_sub: "Redundant complaints clustered",
    kpi_high_risk: "High-Risk Wards",
    kpi_high_risk_sub: "Pre-monsoon action alerts",
    kpi_jan_sunwai: "Jan Sunwai Docket",
    kpi_jan_sunwai_sub: "Escalated for Public Hearing",

    queue_title: "Incident Master Queue",
    queue_subtitle: "Spatio-Temporal Aggregated Incidents",
    filter_all: "All Statuses",
    filter_open: "Open",
    filter_in_progress: "In Progress",
    filter_resolved: "Resolved",
    filter_jan_sunwai: "Jan Sunwai Escalated Only",

    map_legend_title: "Map Legend",
    map_legend_critical: "🔴 Critical Urgency (5+ Reports / Danger)",
    map_legend_high: "🟠 High Urgency (2-4 Reports)",
    map_legend_med: "🟡 Moderate Urgency (1 Report)",
    map_legend_gate: "🔵 300m Spatial Clustering Gate Perimeter",

    predictive_title: "Predictive Municipal Risk & Asset Vulnerability Index",
    predictive_sub: "Proactive pre-monsoon failure likelihood based on Open-Meteo rainfall forecasts, elevation topography, and drainage health.",
    refresh_forecast: "🔄 Refresh Forecast",
    critical_infra_title: "Critical Municipal Infrastructure Failure Risk",

    portal_title: "Citizen Grievance Submission",
    portal_sub: "Report municipal issues in Hindi, Hinglish, Kannada, Tamil, or English. Our AI automatically extracts department, verifies photos, and merges neighborhood complaints.",
    voice_record_btn: "🎙️ Bolkar Batayein / Record Voice Grievance",
    voice_record_stop: "⏹️ Stop Recording",
    voice_quick_samples: "Quick Vernacular Sample Voice Inputs:",
    label_describe: "Describe the Grievance (Text or Vernacular Audio)",
    placeholder_describe: "e.g. Bhaiya road par street light 4 din se band hai, near Sharma General Store, Ward 7",
    label_lat: "Latitude",
    label_lon: "Longitude",
    btn_gps: "📍 Auto-Detect GPS Location (Simulate Ward Pin)",
    label_photo: "Upload Photo (Vision Verification)",
    photo_none: "No Image",
    photo_pothole: "Photo: Pothole / Broken Road",
    photo_sewage: "Photo: Sewer Overflow / Drain Block",
    photo_garbage: "Photo: Garbage Dump / Trash Pile",
    photo_streetlight: "Photo: Broken Streetlight",
    photo_spam: "Photo: Random Selfie / Meme (Spam Test)",
    label_name: "Your Name",
    label_phone: "Phone Number",
    btn_submit_portal: "Submit Grievance to Municipal ULB",

    wa_title: "CivicSense Municipal Bot",
    wa_sub: "Official WhatsApp Grievance Helpline",
    wa_welcome: "Namaste! 🙏 Welcome to CivicSense Municipal Grievance Helpline.\nAap apni samasya (Hinglish/Hindi/Kannada/Tamil/English) yahan type karein ya photo/voice note bhejein.",
    wa_placeholder: "Type a message in Hinglish / Hindi / ಕನ್ನಡ / தமிழ்...",
    wa_voice_btn: "🎙️ Voice",
    quick_road: "🚧 Sadak Gaddha",
    quick_light: "💡 Streetlight Kharab",
    quick_garbage: "🧹 Kachra Dump",
    quick_water: "💧 Paani / Sewer Leak",

    jan_sunwai_title: "Jan Sunwai & Democratic Ward Sabha Dashboard",
    jan_sunwai_desc: "Track Friday Jan Sunwai (Public Grievance Day) dockets, Corporator & MLA accountability, Ward Sabha dates, and Pre-Monsoon Desilting readiness.",
    col_ward: "Ward & Representatives",
    col_corporator: "Corporator (Parshad)",
    col_mla: "MLA & Assembly",
    col_ward_sabha: "Ward Sabha Schedule",
    col_desilting: "Desilting Readiness",
    col_jan_sunwai_cases: "Jan Sunwai Docketed Incidents",

    btn_sunlight: "☀️ Outdoor Sunlight Mode",
    btn_lite_mode: "📶 2G Lite Data"
  },

  hi: {
    brand_sub: "समाश Centro - नगर निगम खुफिया एवं शिकायत निवारण मंच",
    ulb_badge: "यूएलबी लाइव कमांड सेंटर",
    tab_command_center: "अधिकारी नियंत्रण कक्ष",
    tab_predictive_view: "पूर्वानुमान जोखिम सूचकांक",
    tab_jan_sunwai: "जन सुनवाई व वार्ड सभा",
    tab_citizen_portal: "नागरिक सेवा पोर्टल",
    tab_whatsapp_bot: "व्हाट्सएप बॉट डेमो",

    kpi_total_reports: "कुल नागरिक शिकायतें",
    kpi_total_sub: "व्हाट्सएप, ऐप एवं पोर्टल द्वारा",
    kpi_master_tickets: "सक्रिय मास्टर शिकायतें",
    kpi_master_sub: "वार्ड इंजीनियरों को स्वतः प्रेषित",
    kpi_dedup_rate: "डुप्लीकेशन निवारण दर",
    kpi_dedup_sub: "समान शिकायतें एकीकृत",
    kpi_high_risk: "अति-संवेदनशील वार्ड",
    kpi_high_risk_sub: "मानसून पूर्व सुरक्षा अलर्ट",
    kpi_jan_sunwai: "जन सुनवाई डॉकेट",
    kpi_jan_sunwai_sub: "आयुक्त समीक्षा हेतु सूचीबद्ध",

    queue_title: "मास्टर शिकायत सूची",
    queue_subtitle: "स्थान-समय एकीकृत नागरिक शिकायतें",
    filter_all: "सभी स्थितियाँ",
    filter_open: "खुला (Open)",
    filter_in_progress: "प्रगति पर (In Progress)",
    filter_resolved: "समाधान हुआ (Resolved)",
    filter_jan_sunwai: "केवल जन सुनवाई में सूचीबद्ध",

    map_legend_title: "मानचित्र संकेतिका",
    map_legend_critical: "🔴 गंभीर तात्कालिकता (5+ शिकायतें / खतरा)",
    map_legend_high: "🟠 उच्च तात्कालिकता (2-4 शिकायतें)",
    map_legend_med: "🟡 सामान्य तात्कालिकता (1 शिकायत)",
    map_legend_gate: "🔵 300 मीटर क्लस्टरिंग दायरा",

    predictive_title: "पूर्वानुमानित नगर जोखिम एवं अवसंरचना भेद्यता",
    predictive_sub: "ओपन-मेटियो वर्षा पूर्वानुमान, ढलान एवं जल निकासी के आधार पर मानसून पूर्व विफलता का पूर्वानुमान।",
    refresh_forecast: "🔄 मौसम पूर्वानुमान ताज़ा करें",
    critical_infra_title: "महत्वपूर्ण सार्वजनिक संपत्तियों की विफलता जोखिम",

    portal_title: "नागरिक शिकायत पंजीकरण",
    portal_sub: "अपनी समस्या हिंदी, हिंग्लिश, कन्नड़, तमिल या अंग्रेजी में दर्ज करें। एआई स्वचालित रूप से विभाग का चयन और डुप्लीकेट शिकायतों का मिलान करेगा।",
    voice_record_btn: "🎙️ बोलकर बताएं / वॉइस नोट रिकॉर्ड करें",
    voice_record_stop: "⏹️ रिकॉर्डिंग बंद करें",
    voice_quick_samples: "त्वरित स्थानीय आवाज़ नमूने (क्लिक करें):",
    label_describe: "शिकायत का विवरण (टेक्स्ट या बोलकर)",
    placeholder_describe: "उदा: भैया सड़क पर 4 दिन से स्ट्रीट लाइट बंद है, शर्मा जनरल स्टोर के पास, वार्ड 7",
    label_lat: "अक्षांश (Latitude)",
    label_lon: "देशांतर (Longitude)",
    btn_gps: "📍 जीपीएस द्वारा स्थान चुनें (वार्ड पिन)",
    label_photo: "फोटो अपलोड करें (एआई दृष्टि परीक्षण)",
    photo_none: "कोई फोटो नहीं",
    photo_pothole: "फोटो: सड़क पर गड्ढा / टूटी सड़क",
    photo_sewage: "फोटो: सीवर ओवरफ्लो / नाला जाम",
    photo_garbage: "फोटो: कचरे का ढेर",
    photo_streetlight: "फोटो: खराब स्ट्रीट लाइट",
    photo_spam: "फोटो: अन्य फोटो / मीम (स्पैम परीक्षण)",
    label_name: "आपका नाम",
    label_phone: "मोबाइल नंबर",
    btn_submit_portal: "नगर निगम को शिकायत भेजें",

    wa_title: "नागरिक सेवा व्हाट्सएप बॉट",
    wa_sub: "आधिकारिक नगर निगम हेल्पलाइन",
    wa_welcome: "नमस्ते! 🙏 नागरिक सेवा हेल्पलाइन में आपका स्वागत है।\nअपनी समस्या (हिंदी/हिंग्लिश/अंग्रेजी) टाइप करें या फोटो/वॉइस नोट भेजें।",
    wa_placeholder: "संदेश टाइप करें (उदा. सड़क पर गड्ढा है)...",
    wa_voice_btn: "🎙️ आवाज़",
    quick_road: "🚧 सड़क पर गड्ढा",
    quick_light: "💡 स्ट्रीट लाइट खराब",
    quick_garbage: "🧹 कचरा उठाव",
    quick_water: "💧 पानी / सीवर लीकेज",

    jan_sunwai_title: "जन सुनवाई व लोकतांत्रिक वार्ड सभा डैशबोर्ड",
    jan_sunwai_desc: "शुक्रवार जन सुनवाई (समाधान दिवस), पार्षद एवं विधायक जवाबदेही, वार्ड सभा समय-सारणी एवं मानसून पूर्व गाद सफाई प्रगति।",
    col_ward: "वार्ड व जनप्रतिनिधि",
    col_corporator: "पार्षद (Corporator)",
    col_mla: "विधायक व विधानसभा",
    col_ward_sabha: "वार्ड सभा बैठक",
    col_desilting: "गाद सफाई (Desilting) तैयारी",
    col_jan_sunwai_cases: "जन सुनवाई में दर्ज मामले",

    btn_sunlight: "☀️ धूप मोड (Sunlight Mode)",
    btn_lite_mode: "📶 2G लाइट डेटा"
  },

  hg: {
    brand_sub: "SamAashwas Municipal Intelligence Platform",
    ulb_badge: "ULB Live Command Center",
    tab_command_center: "Officer Command Center",
    tab_predictive_view: "Predictive Risk Index",
    tab_jan_sunwai: "Jan Sunwai & Ward Sabha",
    tab_citizen_portal: "Citizen Portal",
    tab_whatsapp_bot: "WhatsApp Bot",

    kpi_total_reports: "Total Citizen Reports",
    kpi_total_sub: "WhatsApp, App aur Portal se",
    kpi_master_tickets: "Active Master Incidents",
    kpi_master_sub: "Ward Engineers ko auto-routed",
    kpi_dedup_rate: "Deduplication Rate",
    kpi_dedup_sub: "Similar complaints grouped together",
    kpi_high_risk: "High-Risk Wards",
    kpi_high_risk_sub: "Monsoon flood alerts",
    kpi_jan_sunwai: "Jan Sunwai Docket",
    kpi_jan_sunwai_sub: "Commissioner Hearing ke liye listed",

    queue_title: "Incident Master Queue",
    queue_subtitle: "Area-wise Clustered Problems",
    filter_all: "All Statuses",
    filter_open: "Open",
    filter_in_progress: "In Progress",
    filter_resolved: "Resolved",
    filter_jan_sunwai: "Jan Sunwai Cases Only",

    map_legend_title: "Map Legend",
    map_legend_critical: "🔴 Critical (5+ Reports / Khatra)",
    map_legend_high: "🟠 High Urgency (2-4 Reports)",
    map_legend_med: "🟡 Moderate Urgency (1 Report)",
    map_legend_gate: "🔵 300m Clustering Perimeter",

    predictive_title: "Predictive Municipal Risk & Flood Vulnerability Index",
    predictive_sub: "Open-Meteo baarish forecast, elevation aur drainage health se pre-monsoon risk calculation.",
    refresh_forecast: "🔄 Refresh Forecast",
    critical_infra_title: "Critical Infrastructure Failure Risk",

    portal_title: "Citizen Grievance Submission",
    portal_sub: "Apni samasya Hinglish, Hindi, Kannada, Tamil ya English mein likhein. AI automatically department select karega aur duplicate complaints merge karega.",
    voice_record_btn: "🎙️ Bolkar Batayein / Voice Note Record Karein",
    voice_record_stop: "⏹️ Stop Recording",
    voice_quick_samples: "Quick Sample Voice Inputs (Click karein):",
    label_describe: "Grievance Describe Karein (Voice ya Text)",
    placeholder_describe: "e.g. Bhaiya road par street light 4 din se band hai, near Sharma General Store, Ward 7",
    label_lat: "Latitude",
    label_lon: "Longitude",
    btn_gps: "📍 GPS Location Auto-Set Karein",
    label_photo: "Photo Upload (AI Verification)",
    photo_none: "No Image",
    photo_pothole: "Photo: Road Pothole / Gaddha",
    photo_sewage: "Photo: Sewer Overflow / Drain Jam",
    photo_garbage: "Photo: Garbage Dump / Kachra Pile",
    photo_streetlight: "Photo: Broken Streetlight",
    photo_spam: "Photo: Random Selfie / Meme (Spam Check)",
    label_name: "Aapka Naam",
    label_phone: "Phone Number",
    btn_submit_portal: "ULB ko Grievance Bhejein",

    wa_title: "CivicSense Municipal Bot",
    wa_sub: "Official WhatsApp Helpline",
    wa_welcome: "Namaste! 🙏 CivicSense Municipal Helpline mein aapka swagat hai.\nApni samasya (Hinglish/Hindi/English) yahan type karein ya photo/voice note bhejein.",
    wa_placeholder: "Type karein (e.g. road par bada gaddha hai)...",
    wa_voice_btn: "🎙️ Voice",
    quick_road: "🚧 Sadak par Gaddha",
    quick_light: "💡 Streetlight Kharab",
    quick_garbage: "🧹 Kachra Safai",
    quick_water: "💧 Paani / Gutter Overflow",

    jan_sunwai_title: "Jan Sunwai & Ward Sabha Dashboard",
    jan_sunwai_desc: "Friday Jan Sunwai (Public Grievance Day), Corporator & MLA details, Ward Committee meetings aur Pre-Monsoon Desilting progress.",
    col_ward: "Ward & Janpratinidhi",
    col_corporator: "Corporator (Parshad)",
    col_mla: "MLA & Vidhan Sabha",
    col_ward_sabha: "Ward Sabha Schedule",
    col_desilting: "Desilting Readiness",
    col_jan_sunwai_cases: "Jan Sunwai Docketed Incidents",

    btn_sunlight: "☀️ Outdoor Sunlight Mode",
    btn_lite_mode: "📶 2G Lite Data"
  },

  kn: {
    brand_sub: "ಸಮಾಶ್ವಾಸ ಪೌರ ಸೌಲಭ್ಯ ಮತ್ತು ಜನತಂತ್ರ ವೇದಿಕೆ",
    ulb_badge: "ನಗರ ಪಾಲಿಕೆ ಕಮಾಂಡ್ ಸೆಂಟರ್",
    tab_command_center: "ಅಧಿಕಾರಿಯ ನಿಯಂತ್ರಣ ಕೇಂದ್ರ",
    tab_predictive_view: "ಮುನ್ಸೂಚಕ ಅಪಾಯ ಸೂಚ್ಯಂಕ",
    tab_jan_sunwai: "ಜನಸ್ಪಂದನ ಮತ್ತು ವಾರ್ಡ್ ಸಭೆ",
    tab_citizen_portal: "ನಾಗರಿಕ ವೆಬ್ ಪೋರ್ಟಲ್",
    tab_whatsapp_bot: "ವಾಟ್ಸಾಪ್ ಬಾಟ್ ಡೆಮೊ",

    kpi_total_reports: "ಒಟ್ಟು ನಾಗರಿಕ ದೂರುಗಳು",
    kpi_total_sub: "ವಾಟ್ಸಾಪ್, ಆ್ಯಪ್ ಮತ್ತು ಪೋರ್ಟಲ್ ಮೂಲಕ",
    kpi_master_tickets: "ಸಕ್ರಿಯ ಮಾಸ್ಟರ್ ಪ್ರಕರಣಗಳು",
    kpi_master_sub: "ವಾರ್ಡ್ ಎಂಜಿನಿಯರ್‌ಗಳಿಗೆ ರವಾನೆ",
    kpi_dedup_rate: "ನಕಲು ತಡೆಗಟ್ಟುವಿಕೆ ದರ",
    kpi_dedup_sub: "ಪುನರಾವರ್ತಿತ ದೂರುಗಳ ವಿಲೀನ",
    kpi_high_risk: "ಹೆಚ್ಚಿನ ಅಪಾಯದ ವಾರ್ಡ್‌ಗಳು",
    kpi_high_risk_sub: "ಮುಂಗಾರು ಪೂರ್ವ ಮುನ್ನೆಚ್ಚರಿಕೆ",
    kpi_jan_sunwai: "ಜನಸ್ಪಂದನ ಪಟ್ಟಿ",
    kpi_jan_sunwai_sub: "ಆಯುಕ್ತರ ಸಾರ್ವಜನಿಕ ವಿಚಾರಣೆ",

    queue_title: "ಮಾಸ್ಟರ್ ದೂರುಗಳ ಪಟ್ಟಿ",
    queue_subtitle: "ಸ್ಥಳೀಯ ಹಾಗೂ ಕಾಲಿಕ ಒಟ್ಟುಗೂಡಿಸಿದ ದೂರುಗಳು",
    filter_all: "ಎಲ್ಲಾ ಸ್ಥಿತಿಗಳು",
    filter_open: "ತೆರೆದಿದೆ (Open)",
    filter_in_progress: "ಪ್ರಗತಿಯಲ್ಲಿದೆ (In Progress)",
    filter_resolved: "ಪರಿಹರಿಸಲಾಗಿದೆ (Resolved)",
    filter_jan_sunwai: "ಜನಸ್ಪಂದನ ಪ್ರಕರಣಗಳು ಮಾತ್ರ",

    map_legend_title: "ನಕ್ಷೆಯ ವಿವರಣೆ",
    map_legend_critical: "🔴 ಗಂಭೀರ ತುರ್ತುಸ್ಥಿತಿ (5+ ದೂರುಗಳು / ಅಪಾಯ)",
    map_legend_high: "🟠 ಹೆಚ್ಚಿನ ತುರ್ತುಸ್ಥಿತಿ (2-4 ದೂರುಗಳು)",
    map_legend_med: "🟡 ಮಧ್ಯಮ ತುರ್ತುಸ್ಥಿತಿ (1 ದೂರು)",
    map_legend_gate: "🔵 300 ಮೀಟರ್ ಸಮೂಹ ವಲಯ",

    predictive_title: "ಮುನ್ಸೂಚಕ ಪೌರ ಅಪಾಯ ಮತ್ತು ಆಸ್ತಿ ದುರ್ಬಲತೆ ಸೂಚ್ಯಂಕ",
    predictive_sub: "ಓಪನ್-ಮೆಟಿಯೊ ಮಳೆ ಮುನ್ಸೂಚನೆ ಮತ್ತು ಒಳಚರಂಡಿ ಸಾಮರ್ಥ್ಯದ ಆಧಾರದ ಮೇಲೆ ಮುಂಗಾರು ಮುನ್ನೆಚ್ಚರಿಕೆ.",
    refresh_forecast: "🔄 ಮುನ್ಸೂಚನೆ ನವೀಕರಿಸಿ",
    critical_infra_title: "ಪ್ರಮುಖ ಸಾರ್ವಜನಿಕ ಆಸ್ತಿಗಳ ವೈಫಲ್ಯದ ಅಪಾಯ",

    portal_title: "ನಾಗರಿಕ ದೂರು ಸಲ್ಲಿಕೆ",
    portal_sub: "ಕನ್ನಡ, ಇಂಗ್ಲಿಷ್ ಅಥವಾ ಹಿಂದಿಯಲ್ಲಿ ದೂರು ಸಲ್ಲಿಸಿ. ನಮ್ಮ ಎಐ ವ್ಯವಸ್ಥೆಯು ಇಲಾಖೆಯನ್ನು ಗುರುತಿಸಿ ಒಂದೇ ಪ್ರದೇಶದ ದೂರುಗಳನ್ನು ಒಟ್ಟುಗೂಡಿಸುತ್ತದೆ.",
    voice_record_btn: "🎙️ ಧ್ವನಿ ಮುದ್ರಿಸಿ / ಧ್ವನಿ ದೂರು ನೀಡಿ",
    voice_record_stop: "⏹️ ಧ್ವನಿಮುದ್ರಣ ನಿಲ್ಲಿಸಿ",
    voice_quick_samples: "ಮಾದರಿ ಧ್ವನಿ ದೂರುಗಳು (ಕ್ಲಿಕ್ ಮಾಡಿ):",
    label_describe: "ದೂರಿನ ವಿವರ (ಬರೆಯಿರಿ ಅಥವಾ ಮಾತನಾಡಿ)",
    placeholder_describe: "ಉದಾ: ರಸ್ತೆಯಲ್ಲಿ ದೊಡ್ಡ ಗುಂಡಿ ಬಿದ್ದಿದೆ, ಶರ್ಮಾ ಸ್ಟೋರ್ ಬಳಿ ಬೀದಿ ದೀಪ ಹತ್ತುತ್ತಿಲ್ಲ, ವಾರ್ಡ್ 7",
    label_lat: "ಅಕ್ಷಾಂಶ (Latitude)",
    label_lon: "ರೇಖಾಂಶ (Longitude)",
    btn_gps: "📍 ಜಿಪಿಎಸ್ ಸ್ಥಳ ಗುರುತಿಸಿ (ವಾರ್ಡ್ ಪಿನ್)",
    label_photo: "ಚಿತ್ರ ಅಪ್‌ಲೋಡ್ ಮಾಡಿ (ಎಐ ಪರಿಶೀಲನೆ)",
    photo_none: "ಚಿತ್ರವಿಲ್ಲ",
    photo_pothole: "ಚಿತ್ರ: ರಸ್ತೆ ಗುಂಡಿ / ಹಾಳಾದ ರಸ್ತೆ",
    photo_sewage: "ಚಿತ್ರ: ಒಳಚರಂಡಿ ಉಕ್ಕಿ ಹರಿಯುವುದು",
    photo_garbage: "ಚಿತ್ರ: ಕಸದ ರಾಶಿ",
    photo_streetlight: "ಚಿತ್ರ: ಕೆಟ್ಟ ಬೀದಿ ದೀಪ",
    photo_spam: "ಚಿತ್ರ: ಸಂಬಂಧವಿಲ್ಲದ ಫೋಟೋ (ಸ್ಪ್ಯಾಮ್ ಪರೀಕ್ಷೆ)",
    label_name: "ನಿಮ್ಮ ಹೆಸರು",
    label_phone: "ದೂರವಾಣಿ ಸಂಖ್ಯೆ",
    btn_submit_portal: "ನಗರ ಪಾಲಿಕೆಗೆ ದೂರು ಸಲ್ಲಿಸಿ",

    wa_title: "ಸಿವಿಕ್‌ಸೆನ್ಸ್ ಪೌರ ವಾಟ್ಸಾಪ್ ಬಾಟ್",
    wa_sub: "ಅಧಿಕೃತ ವಾಟ್ಸಾಪ್ ಸಹಾಯವಾಣಿ",
    wa_welcome: "ನಮಸ್ಕಾರ! 🙏 ಸಿವಿಕ್‌ಸೆನ್ಸ್ ಮುನಿಸಿಪಲ್ ಸಹಾಯವಾಣಿಗೆ ಸ್ವಾಗತ.\nನಿಮ್ಮ ಸಮಸ್ಯೆಯನ್ನು (ಕನ್ನಡ/English/Hindi) ಟೈಪ್ ಮಾಡಿ ಅಥವಾ ಧ್ವನಿ ಸಂದೇಶ ಕಳುಹಿಸಿ.",
    wa_placeholder: "ಸಂದೇಶ ಬರೆಯಿರಿ (ಉದಾ: ರಸ್ತೆ ಗುಂಡಿ ದುರಸ್ತಿ ಮಾಡಿ)...",
    wa_voice_btn: "🎙️ ಧ್ವನಿ",
    quick_road: "🚧 ರಸ್ತೆ ಗುಂಡಿ",
    quick_light: "💡 ಬೀದಿ ದೀಪ ಕೆಟ್ಟಿದೆ",
    quick_garbage: "🧹 ಕಸ ವಿಲೇವಾರಿ",
    quick_water: "💧 ನೀರು / ಚರಂಡಿ ಸಮಸ್ಯೆ",

    jan_sunwai_title: "ಜನಸ್ಪಂದನ ಮತ್ತು ಪ್ರಜಾಸತ್ತಾತ್ಮಕ ವಾರ್ಡ್ ಸಭೆ",
    jan_sunwai_desc: "ಶುಕ್ರವಾರದ ಜನಸ್ಪಂದನ ಸಭೆ, ಕಾರ್ಪೊರೇಟರ್ ಮತ್ತು ಶಾಸಕರ ವಿವರಗಳು, ವಾರ್ಡ್ ಸಮಿತಿ ಸಭೆಗಳು ಮತ್ತು ಮುಂಗಾರು ಪೂರ್ವ ಹೂಳೆತ್ತುವ ಪ್ರಗತಿ.",
    col_ward: "ವಾರ್ಡ್ ಮತ್ತು ಜನಪ್ರತಿನಿಧಿ",
    col_corporator: "ಕಾರ್ಪೊರೇಟರ್",
    col_mla: "ಶಾಸಕರು ಮತ್ತು ಕ್ಷೇತ್ರ",
    col_ward_sabha: "ವಾರ್ಡ್ ಸಭೆಯ ದಿನಾಂಕ",
    col_desilting: "ಹೂಳೆತ್ತುವಿಕೆ ಸಿದ್ಧತೆ",
    col_jan_sunwai_cases: "ಜನಸ್ಪಂದನ ದೂರುಗಳು",

    btn_sunlight: "☀️ ಬಿಸಿಲು ಮೋಡ್ (Sunlight Mode)",
    btn_lite_mode: "📶 2G ಲೈಟ್ ಡೇಟಾ"
  },

  ta: {
    brand_sub: "சமாஷ்வாஸ் நகராட்சி நுண்ணறிவு மற்றும் குறைதீர்ப்பு தளம்",
    ulb_badge: "நகராட்சி நேரடி கட்டுப்பாட்டு மையம்",
    tab_command_center: "அதிகாரி கட்டளை மையம்",
    tab_predictive_view: "முன்னறிவிப்பு இடர் குறியீடு",
    tab_jan_sunwai: "மக்கள் குறைதீர்ப்பு & வார்டு சபை",
    tab_citizen_portal: "குடிமக்கள் சேவை தளம்",
    tab_whatsapp_bot: "வாட்ஸ்அப் பாட் டெமோ",

    kpi_total_reports: "மொத்த குடிமக்கள் புகார்கள்",
    kpi_total_sub: "வாட்ஸ்அப், ஆப் மற்றும் போர்டல் மூலம்",
    kpi_master_tickets: "செயலில் உள்ள முதன்மை புகார்கள்",
    kpi_master_sub: "வார்டு பொறியாளர்களுக்கு தானியங்கி ஒதுக்கீடு",
    kpi_dedup_rate: "நகல் குறைப்பு விகிதம்",
    kpi_dedup_sub: "ஒரே பகுதி புகார்கள் ஒருங்கிணைப்பு",
    kpi_high_risk: "அதிக ஆபத்துள்ள வார்டுகள்",
    kpi_high_risk_sub: "மழைக்கால முன்னெச்சரிக்கை எச்சரிக்கை",
    kpi_jan_sunwai: "மக்கள் குறைதீர்ப்பு பட்டியல்",
    kpi_jan_sunwai_sub: "ஆணையர் விசாரணைக்கு பட்டியலிடப்பட்டது",

    queue_title: "முதன்மை புகார்கள் வரிசை",
    queue_subtitle: "இடம் மற்றும் நேரம் சார்ந்து தொகுக்கப்பட்ட புகார்கள்",
    filter_all: "அனைத்து நிலைகளும்",
    filter_open: "திறந்துள்ளது (Open)",
    filter_in_progress: "நடவடிக்கையில் (In Progress)",
    filter_resolved: "தீர்க்கப்பட்டது (Resolved)",
    filter_jan_sunwai: "குறைதீர்ப்பு வழக்குகள் மட்டும்",

    map_legend_title: "வரைபடக் குறியீடுகள்",
    map_legend_critical: "🔴 தீவிர அவசரம் (5+ புகார்கள் / ஆபத்து)",
    map_legend_high: "🟠 அதிக அவசரம் (2-4 புகார்கள்)",
    map_legend_med: "🟡 நடுத்தர அவசரம் (1 புகார்)",
    map_legend_gate: "🔵 300 மீட்டர் ஒருங்கிணைப்பு எல்லை",

    predictive_title: "முன்னறிவிப்பு நகர்ப்புற இடர் மற்றும் உள்கட்டமைப்பு குறியீடு",
    predictive_sub: "வானிலை முன்னறிவிப்பு மற்றும் வடிகால் நிலையின் அடிப்படையில் வெள்ள முன்னெச்சரிக்கை.",
    refresh_forecast: "🔄 முன்னறிவிப்பை புதுப்பிக்கவும்",
    critical_infra_title: "முக்கிய நகராட்சி சொத்துக்களின் பாதிப்பு அபாயம்",

    portal_title: "குடிமக்கள் புகார் பதிவு",
    portal_sub: "உங்கள் புகாரை தமிழ், ஆங்கிலம் அல்லது இந்தியில் பதிவு செய்யவும். செயற்கை நுண்ணறிவு தானாகவே துறையை அடையாளம் கண்டு புகார்களை இணைக்கும்.",
    voice_record_btn: "🎙️ குரல் பதிவு மூலம் புகார் அளிக்கவும்",
    voice_record_stop: "⏹️ பதிவை நிறுத்தவும்",
    voice_quick_samples: "மாதிரி குரல் புகார்கள் (கிளிக் செய்யவும்):",
    label_describe: "புகார் விவரம் (எழுதவும் அல்லது பேசவும்)",
    placeholder_describe: "உதா: தெரு விளக்கு எரியவில்லை, சாக்கடை நீர் சாலையில் வழிகிறது, வார்டு 7",
    label_lat: "அட்சரேகை (Latitude)",
    label_lon: "தீர்க்கரேகை (Longitude)",
    btn_gps: "📍 ஜிபிஎஸ் மூலம் இருப்பிடத்தை தேர்வு செய்",
    label_photo: "புகைப்படம் பதிவேற்றவும் (AI சரிபார்ப்பு)",
    photo_none: "புகைப்படம் இல்லை",
    photo_pothole: "படம்: சாலையில் குழி / உடைந்த சாலை",
    photo_sewage: "படம்: சாக்கடை நீர் வழிதல்",
    photo_garbage: "படம்: குப்பைக் குவியல்",
    photo_streetlight: "படம்: பழுதான தெரு விளக்கு",
    photo_spam: "படம்: தொடர்பில்லாத புகைப்படம் (ஸ்பேம் சோதனை)",
    label_name: "உங்கள் பெயர்",
    label_phone: "தொலைபேசி எண்",
    btn_submit_portal: "நகராட்சிக்கு புகாரை அனுப்பவும்",

    wa_title: "சிவிக்சென்ஸ் நகராட்சி வாட்ஸ்அப் பாட்",
    wa_sub: "அதிகாரப்பூர்வ நகராட்சி உதவி மையம்",
    wa_welcome: "வணக்கம்! 🙏 சிவிக்சென்ஸ் நகராட்சி உதவி மையத்திற்கு வரவேற்கிறோம்.\nஉங்கள் புகாரை (தமிழ்/English/Hindi) டைப் செய்யவும் அல்லது குரல் பதிவு அனுப்பவும்.",
    wa_placeholder: "செய்தியை டைப் செய்யவும் (உதா: சாலையில் பெரிய குழி)...",
    wa_voice_btn: "🎙️ குரல்",
    quick_road: "🚧 சாலை குழி",
    quick_light: "💡 தெரு விளக்கு பழுது",
    quick_garbage: "🧹 குப்பை அகற்றுதல்",
    quick_water: "💧 குடிநீர் / சாக்கடை கசிவு",

    jan_sunwai_title: "மக்கள் குறைதீர்ப்பு நாள் & வார்டு சபை",
    jan_sunwai_desc: "வெள்ளிக்கிழமை மக்கள் குறைதீர்ப்பு நாள், கவுன்சிலர் மற்றும் சட்டமன்ற உறுப்பினர் விவரங்கள், மற்றும் மழைக்கால தூர்வாரும் பணிகள்.",
    col_ward: "வார்டு மற்றும் மக்கள் பிரதிநிதிகள்",
    col_corporator: "கவுன்சிலர்",
    col_mla: "சட்டமன்ற உறுப்பினர்",
    col_ward_sabha: "வார்டு சபை அட்டவணை",
    col_desilting: "தூர்வாரும் முன்னேற்றம்",
    col_jan_sunwai_cases: "குறைதீர்ப்பில் உள்ள வழக்குகள்",

    btn_sunlight: "☀️ நேரடி வெயில் முறை (Sunlight Mode)",
    btn_lite_mode: "📶 2G குறைந்த டேட்டா"
  }
};

let currentLang = 'en';

function setLanguage(lang) {
  if (!I18N_TRANSLATIONS[lang]) return;
  currentLang = lang;
  localStorage.setItem('civicsense_lang', lang);

  // Update language selector active button
  document.querySelectorAll('.lang-btn').forEach(btn => {
    btn.classList.toggle('active', btn.dataset.lang === lang);
  });

  const t = I18N_TRANSLATIONS[lang];

  // Apply to elements with data-i18n
  document.querySelectorAll('[data-i18n]').forEach(el => {
    const key = el.getAttribute('data-i18n');
    if (t[key]) {
      if (el.tagName === 'INPUT' || el.tagName === 'TEXTAREA') {
        el.placeholder = t[key];
      } else {
        el.innerText = t[key];
      }
    }
  });

  // Update dynamic elements
  updateDynamicTexts();
}

function updateDynamicTexts() {
  const t = I18N_TRANSLATIONS[currentLang];
  const sunlightBtn = document.getElementById('btn-sunlight-toggle');
  if (sunlightBtn) {
    const isSunlight = document.body.classList.contains('sunlight-mode');
    sunlightBtn.innerText = isSunlight ? "🌙 Indoor / Dark Mode" : t.btn_sunlight;
  }
}
