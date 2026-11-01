# Baseline Audit Report (CivicSense AI / SamAashwas v1)

Verified against the codebase on 2026-11-01 using Python 3.11, FastAPI `TestClient`, and automated probe scripts.

---

## 1. Security and Privacy Findings

| ID | Severity | Finding | Evidence / Reproduction | Fix Target |
|---|---|---|---|---|
| **S1** | **P0** | **No authentication or authorization on mutating routes.** Any anonymous user can issue `PATCH /api/v1/master-tickets/{id}` with `{"status": "RESOLVED"}` and close municipal tickets without credentials. | `c.patch('/api/v1/master-tickets/MST-...', json={'status': 'RESOLVED'}).status_code == 200` | Require JWT token + role check (`require_role`). Returns 401/403. |
| **S2** | **P0** | **PII leak in public API.** `GET /api/v1/complaints` returns plain-text `citizen_name` and `citizen_phone` for every complaint. | `citizen_phone in c.get('/api/v1/complaints?limit=1').json()[0] == True` | Mask citizen PII (`+91 98xxx xx660`) by default on all public/unauthenticated endpoints. |
| **S3** | **P0** | **Stored XSS vulnerability.** `frontend/js/app.js` directly interpolates unescaped user text into `innerHTML`. | 36 instances of unescaped `innerHTML` assignments in `app.js`. | Add `esc()` DOM sanitizer helper and strictly use `textContent` or sanitized template tags. |
| **S4** | **P0** | **CORS reflection of arbitrary origins with credentials.** `main.py` hard-coded `allow_origins=["*"]` with `allow_credentials=True`. | `OPTIONS /api/v1/health` with `Origin: https://evil.example` reflected `https://evil.example`. | Bind CORS strictly to configured `CORS_ORIGINS`. Reject untrusted origins. |
| **S5** | **P0** | **No input bounds validation.** Extreme coordinates (`lat=999, lon=-999`) or massive 200 KB text payloads are accepted with HTTP 200. | `c.post('/api/v1/complaints/submit', json={'raw_text': 'x', 'lat': 999, 'lon': -999}).status_code == 200` | Enforce Pydantic validation: text ≤ 2,000 chars, lat/lon bounded within city bbox. |
| **S6** | **P1** | **Unauthenticated webhooks & silent default coordinates.** Missing signature verification; missing location silently defaults to Bengaluru coordinates. | WhatsApp webhook lacks HMAC signature check. | Add HMAC-SHA256 signature verification; require location or route to triage. |
| **S7** | **P1** | **Latent crash in fallback ward list.** Fallback ward list in `db/database.py` contains JavaScript `false`/`true` inside Python dictionaries. | `NameError: name 'false' is not defined` if JSON data file fails to load. | Replace with Python `False`/`True`. |
| **S8** | **P1** | **Real official names with invented phone numbers.** Sourced data pairs names with fictional phones; random 10-digit citizen numbers risk real person collisions. | Ward datasets contain placeholders resembling real phone numbers. | Use standard fictional prefix (0-5) or masked placeholders; require source + verification date. |
| **S9** | **P1** | **Impersonation of official government portal.** Use of "सत्यमेव जयते", tricolor strips, and simulated official government seals. | Top navigation contained simulated official national seal and government branding. | Display persistent Prototype Banner: *"Independent academic prototype. Not an official government service."* |

---

## 2. AI & Algorithmic Correctness Findings

| ID | Severity | Finding | Evidence / Reproduction | Fix Target |
|---|---|---|---|---|
| **A1** | **P1** | **Regional Indian language coverage gap.** Telugu, Bengali, Urdu, and Punjabi queries are detected as English and defaulted to Sanitation with 0.50 confidence. | `nlp_engine.analyze('రోడ్డు మీద గుंत ఉంది')` -> `lang=English, dept=Sanitation & Solid Waste, conf=0.5` | Implement multi-script detector and Tier-1 Indian language lexicon models. |
| **A2** | **P1** | **Substring keyword matching.** Words like "delight" trigger Electrical department routing because of "light". | `nlp_engine.analyze('delight cafe light fitting is great')` -> `Electrical & Streetlighting` | Token-aware matching with word boundaries. |
| **A3** | **P1** | **No negation handling.** "No garbage problem here, the road is fine" routes to Sanitation. | `nlp_engine.analyze('No garbage problem here...')` -> `Sanitation & Solid Waste` | Implement negation window (±3 tokens) with localized negation words. |
| **A4** | **P1** | **No router abstention.** Meaningless input ("hello", "thanks") routes to Sanitation at 0.50 confidence instead of abstaining. | `nlp_engine.analyze('hello')` -> `Sanitation & Solid Waste` | Calibrated routing with confidence gating (`τ_auto=0.80`, `τ_floor=0.45`); abstain to Triage. |
| **A5** | **P1** | **Vision engine relies on filename keywords rather than pixels.** `selfie_pothole.jpg` is auto-verified; opaque filename `IMG_2231.jpg` is flagged as spam. | Image verification matches string in `image_url` instead of decoding image content. | Add real image upload path with EXIF parsing, pHash duplicate detection, blur/brightness checks. |
| **A6** | **P1** | **Deduplication uses linear scan without cluster cap.** Radius is globally 300m for all categories; no diameter cap to prevent chaining drift. | `core/deduplication.py` iterates through all master tickets linearly. | Spatial index (H3/grid), category-aware radii (30m-400m), 2× diameter cap, recurrence tracking. |
| **A7** | **P1** | **Ward assignment uses nearest centroid instead of polygon.** Boundary complaints get assigned to wrong ward. | Centroid distance calculation used for ward lookup. | Shapely STRtree point-in-polygon assignment against GeoJSON boundaries. |
| **A8** | **P1** | **Jan Sunwai over-escalation.** Every High/Critical complaint is auto-docketed for Friday Jan Sunwai, flooding the docket. | Docket escalation lacks capacity caps or multi-factor qualification. | Capped docket builder (top 25) requiring SLA breach ≥ 1.5×, recurrence ≥ 2×, or ≥ 5 unique citizens. |
| **A9** | **P1** | **Unvalidated risk model with hardcoded years.** Uses `2026 - installed_year` and fabricated weather fallback formula. | `45 + |lat*10| % 30` mm labeled "Calibrated Weather Engine". | Open-Meteo real archive/forecast API; IMD 24h rainfall categories; dynamic year calculation. |

---

## 3. Product Honesty, Theme & Frontend Findings

| ID | Severity | Finding | Evidence / Reproduction | Fix Target |
|---|---|---|---|---|
| **H1** | **P1** | **Hard-coded marketing counters.** "18,450+ resolved", "16.4 Hrs", "96.2%" are static string literals. | Hard-coded in HTML hero section. | Dynamically compute counters from database or visibly display Demo Data ribbon. |
| **H2** | **P1** | **Static fixtures presented as live.** Before/After gallery and Rewards karma are static mock payloads. | Fixed arrays returned in `api/cities.py`. | Dynamically generate gallery from verified resolved tickets with geofenced after-photos. |
| **F1** | **P1** | **Tailwind claimed in synopsis but unused in code.** Zero Tailwind utility classes used. | Only an orphan `tailwind.config.js` exists. | Drop Tailwind claim honestly and document in `docs/SYNOPSIS_DELTA.md`. |
| **F2** | **P1** | **Offline and 2G Lite modes incomplete.** Service worker precache omits `sticker_theme.js`; external unpkg/CDN dependencies fail offline. | Offline mode fails when CDN tiles cannot be fetched. | Self-host Leaflet and fonts; implement SVG ward-grid fallback in Lite mode; IndexedDB queue. |
| **F6** | **P2** | **Theme carries leftover transit/bus motifs.** Header comments mention "CampusHop Bus Stop Theme", mascot tooltip reads "Aashwas-Babu, Your Civic Transit Guide", mini-bus in floating background, and empty state says "All Quiet on the Bus Stop!". | Verified in `frontend/js/sticker_theme.js` and `frontend/index.html`. | Redesign into Sticker Book Civic: municipal inspector mascot, 24 civic floating SVG items, zero bus leftovers. |
