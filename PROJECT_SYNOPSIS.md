# PROJECT SYNOPSIS

---

### **1. Project Title**
**SamAashwas: Municipal Grievance Intelligence & Predictive Maintenance Platform**  
*(Course Code: 24CSP-337 – Full Stack-II | Capstone Project)*

---

### **2. Student Details**
* **Candidate 1:** Kanav Kaul (UID: 24BAI70060)
* **Candidate 2:** Shivansh Paliwal (UID: 24BAI70045)
* **Academic Batch:** 2024–2028 (5th Semester)
* **Institution:** Chandigarh University, Gharuan, Mohali, Punjab
* **GitHub Repository:** [https://github.com/Kanav2605/SamAashwas](https://github.com/Kanav2605/SamAashwas)

---

### **3. Introduction**
Urban Local Bodies (ULBs) and Municipal Corporations across India (such as BBMP, BMC, MCD) receive tens of thousands of citizen grievances every day via municipal helplines, WhatsApp portals, and web portals. Effective civic grievance redressal directly impacts urban quality of life, public health, and municipal infrastructure resilience. 

**SamAashwas** is an AI-powered, full-stack municipal grievance intelligence and predictive maintenance platform engineered to modernize public grievance handling. Tailored specifically for the Indian linguistic, socio-cultural, and administrative landscape, SamAashwas empowers citizens of all literacy levels to report civic issues effortlessly in their native tongues (Hindi, Hinglish, Kannada, Tamil, English) via text or voice notes. For municipal administration, it provides automated NLP department routing, computer vision fraud detection, spatio-temporal geo-semantic deduplication, citizen charter SLA tracking with Jan Sunwai escalation, and pre-monsoon predictive infrastructure risk mapping.

---

### **4. Problem Statement**
Current municipal grievance systems in Indian Urban Local Bodies suffer from four critical structural bottlenecks:

1. **Linguistic Misrouting & Drop-Offs:** Standard portals mandate English drop-down menus. Indian citizens communicate in colloquial code-mixed dialects (*Hinglish*, *Kanglish*, *Tanglish*, or native Devanagari/Dravidian scripts, e.g., *"Gali mein sewer overflow ho raha hai"* or *"Street light band ide"*). Keyword-based bots fail to extract wards, landmarks, or assign the proper municipal engineer.
2. **Duplicate Flooding & Artificial Backlogs:** Whenever a major civic breakdown occurs (e.g., a burst water main or collapsed road culvert), 50–100 neighborhood residents submit duplicate tickets. Field engineers are inundated with duplicate work orders, obscuring genuine unserved issues.
3. **Fraudulent, Irrelevant & Unverified Reports:** Citizens frequently upload memes, selfies, screenshots, or unrelated images to gain attention, wasting manual auditing bandwidth.
4. **Reactive Firefighting vs. Proactive Maintenance:** Municipal engineers act only after catastrophic failures occur (e.g., severe urban waterlogging during monsoons) rather than proactively servicing vulnerable drainage basins and electrical transformers ahead of heavy rainfall.

---

### **5. Objectives**
The core objectives of the SamAashwas platform are:
1. **Develop a Vernacular-First Citizen Interface:** Enable seamless multimodal grievance filing (text, audio/voice notes, photos, and GPS) across multiple Indian languages (Hindi, Kannada, Tamil, Hinglish, English) with speech-to-text recognition and WhatsApp-like conversational bots.
2. **Build an Automated Code-Mixed NLP Pipeline:** Accurately classify municipal departments (Sanitation, Water/Sewage, Roads, Streetlighting, Public Health, Encroachment), extract spatial landmarks, and parse municipal ward notations.
3. **Implement Geo-Semantic Incident Deduplication:** Cluster overlapping complaints within a 300-meter geographic gate and semantic text similarity into unified **Master Incidents**, dynamically aggregating citizen votes and elevating urgency.
4. **Integrate Visual Complaint Verification:** Leverage computer vision to cross-verify uploaded images against complaint categories (potholes, garbage dumps, waterlogging, sewage overflow, broken poles) while filtering out spam and selfies.
5. **Establish Democratic Accountability & SLA Tracking:** Enforce Citizen Charter SLA countdowns, map local Ward Corporators and MLAs to tickets, and automate escalation to **Jan Sunwai (Public Grievance Day)** upon SLA breaches.
6. **Formulate Predictive Municipal Maintenance Models:** Ingest historical complaint density, asset age, and live 48-hour rainfall forecasts to generate Ward Vulnerability Indices (0–100) and automated pre-emptive action orders for field squads.

---

### **6. Proposed Solution**
SamAashwas proposes a cohesive, two-tier architecture:

* **Citizen Experience Tier (Mobile-First & Low-Bandwidth Resilient):**
  A lightweight Progressive Web App (PWA) and WhatsApp Bot interface equipped with an **Outdoor Sunlight Readability Mode** for field officers, offline-resilient service workers, and voice note transcription. Citizens can speak or type in their local language, pin their geolocation, and attach photos.
* **Intelligent Municipal Command Center & Engine Tier:**
  A FastAPI-powered backend integrating:
  * **Multilingual NLP Engine:** Tokenizes and extracts entities (Ward, Landmark, Urgency) across Indic Unicode blocks and phonetic transliterations.
  * **Visual Verifier:** Validates civic image contents with confidence scoring.
  * **Spatio-Temporal Deduplicator:** Employs Haversine geographic radius filters combined with Jaccard and containment semantic vector algorithms.
  * **Predictive Risk Engine:** Computes ward vulnerability scores from open meteorological forecasts and infrastructure age logs.
  * **Live Incident Map:** An interactive Leaflet GIS dashboard color-coded by hazard severity with SLA breach monitors and Jan Sunwai escalation alerts.

---

### **7. Modules / Key Features**

1. **Citizen Portal & Vernacular Voice Submission Module:**
   * Instant UI language switching (English, हिन्दी, ಕನ್ನಡ, தமிழ்).
   * Speech-to-text voice note grievance capture for semi-literate citizens.
   * Interactive WhatsApp chatbot simulator with instant formatted receipt cards.
2. **Code-Mixed Civic NLP & Routing Module:**
   * Automated intent routing across 6 municipal departments.
   * Named Entity Recognition (NER) for ward notations (`Ward-7`, `W-12`, Indic numerals `०-९`) and landmarks (`near Sharma Store`, `opp Metro Pillar`).
3. **Computer Vision Complaint Verifier & Anti-Spam Module:**
   * Multi-class civic image classifier (`pothole`, `garbage_dump`, `waterlogging`, `sewage_overflow`, `broken_streetlight`, `fallen_tree`).
   * Image-to-text correlation check with confidence scoring and spam/selfie rejection.
4. **Spatio-Temporal Deduplication & Master Ticket Aggregator:**
   * 300-meter spatial bounding gate.
   * Hybrid semantic similarity clustering linking duplicate complaints to a single Master Ticket.
   * Dynamic urgency escalation: Automatically escalates master tickets to *Critical* when hazardous conditions or multiple endorsements are detected.
5. **Democratic Representation & Jan Sunwai Escalation Module:**
   * Automated mapping of Ward Corporators (पार्षद / ಕಾರ್ಪೊರೇಟರ್ / கவுன்சிலர்) and MLAs with contact details.
   * Statutory Citizen Charter SLA countdown with `⚠️ SLA: Overdue` flags.
   * Direct escalation pipeline to **Jan Sunwai (Public Grievance Day)** for municipal commissioner review.
6. **Predictive Maintenance & Geospatial Command Center Module:**
   * Real-time Leaflet GIS ward map with clustered incident markers.
   * 48-Hour Open-Meteo rainfall forecast integration.
   * Ward Vulnerability Index (0–100) triggering automated pre-monsoon desilting squads and mobile dewatering pump deployments.
   * National Mission Tagging (Swachh Bharat 2.0, AMRUT 2.0, Jal Jeevan Mission, Smart Cities SLNP).

---

### **8. Technology Stack**

| Layer / Component | Technology Selected | Rationale & Purpose |
| :--- | :--- | :--- |
| **Frontend Framework** | Vanilla ES6+ JavaScript, HTML5, CSS3, Tailwind Utility Classes | Ultra-lightweight, zero bundle overhead, rapid loading on low-end 2G/3G mobile devices in India |
| **Mapping & GIS** | Leaflet.js, OpenStreetMap Tiles | Open-source, lightweight GIS map rendering with custom ward-level marker clustering |
| **Web Accessibility & Offline** | Progressive Web App (PWA), Service Workers, Web Speech API | Offline caching, home-screen installability, and vernacular voice note speech recognition |
| **Backend Framework** | Python 3.11, FastAPI, Uvicorn | High-performance asynchronous REST API with automatic OpenAPI (Swagger) documentation |
| **Validation & Schema** | Pydantic v2 | Strict request validation, type checking, and domain modeling |
| **Data Layer & Spatial Logic** | In-Memory Spatial Stores / PostgreSQL + PostGIS Architecture | Spatial distance calculation (Haversine / `ST_DWithin`) and relational persistence |
| **NLP & Text Processing** | Regex NER, Scikit-learn TF-IDF, Multilingual Token Normalization | Fast, low-latency parsing of code-mixed Hindi, Kannada, Tamil, and Hinglish without GPU lock-in |
| **Predictive Modeling** | Scikit-learn, Open-Meteo Weather API Integration | Multi-factor tabular risk scoring combining weather forecasts and asset age logs |
| **Testing & Quality Assurance** | Pytest, AnyIO, HTTPX | 34 automated unit and integration tests with 100% pass rate |
| **Version Control & CI/CD** | Git, GitHub | Distributed version control and remote tracking on `origin/main` |

---

### **9. Expected Outcome**
* **70%+ Reduction in Municipal Ticket Duplication:** Redundant reports are consolidated into unified master tickets, saving municipal administrative overhead.
* **100% Automated Grievance Routing:** Complaints are routed instantly to the right ward engineer without human manual sorting.
* **Enhanced Citizen Inclusivity:** Marginalized and semi-literate citizens can voice grievances in their regional mother tongue.
* **Proactive Disaster Prevention:** Cities can preempt urban flooding and power outages through 48-hour pre-monsoon predictive risk alerts.
* **Transparent Democratic Accountability:** Citizens and ward officers can track SLA countdowns and see unresolved issues escalated directly to Jan Sunwai hearings.

---

### **10. Future Scope**
1. **Live WhatsApp Business API & IVR Integration:** Connect Twilio/Meta WhatsApp Cloud API webhooks and automated interactive voice response (IVR) phone lines for non-smartphone users.
2. **Deep Edge YOLOv8 & Indic-BERT Deployment:** Deploy quantized Onnx/PyTorch YOLOv8 on camera edge streams and fine-tune Indic-BERT models for deeper dialectical sentiment analysis.
3. **IoT Sensor Ingestion:** Integrate ultrasonic water-level sensors in municipal stormwater drains and smart electricity meter telemetry directly into the predictive maintenance engine.
4. **Blockchain-Backed Audit Trail:** Immutably record contractor work order completion and citizen resolution sign-offs for transparent public auditing.

---

### **11. References**
1. Ministry of Housing and Urban Affairs (MoHUA), Government of India – *Swachh Bharat Mission (Urban 2.0) & AMRUT Guidelines*, [https://mohua.gov.in](https://mohua.gov.in).
2. Department of Administrative Reforms & Public Grievances (DARPG) – *CPGRAMS Public Grievance Portal & Citizen Charter Standards*, [https://pgportal.gov.in](https://pgportal.gov.in).
3. Open-Meteo Weather Forecast API Documentation – *High-Resolution Global Meteorological Models*, [https://open-meteo.com/](https://open-meteo.com/).
4. Reimers, N., & Gurevych, I. (2019). *Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks*. Proceedings of the 2019 Conference on Empirical Methods in Natural Language Processing (EMNLP).
5. Ultralytics (2023). *YOLOv8: Real-Time Computer Vision and Object Detection Architecture*. [https://github.com/ultralytics/ultralytics](https://github.com/ultralytics/ultralytics).
6. FastAPI Documentation & Asynchronous Web Architecture in Python, [https://fastapi.tiangolo.com/](https://fastapi.tiangolo.com/).
