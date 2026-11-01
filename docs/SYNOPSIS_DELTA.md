# Synopsis Delta & Reconciliation Report (docs/SYNOPSIS_DELTA.md)

This document honestly reconciles the submitted capstone synopsis with the implementation reality of SamAashwas v2.

---

## 1. Pulled-In Future Scope Items

| Feature | Synopsis Status | v2 Reality | Rationale |
|---|---|---|---|
| **Telegram Bot Integration** | "Future Scope" (WhatsApp only) | Implemented as Tier-1 Channel | Free, instant setup without Meta Business Verification delays; runs identical conversation state machine. |
| **Field Crew Dispatch Optimizer** | Not in Synopsis | Fully Implemented Centrepiece | Transformed reactive complaint logging into proactive, route-optimized field crew dispatch (Insertion + 2-Opt local search). |
| **Human Triage Queue** | Not in Synopsis | Core Architectural Feature | Handles abstained and low-confidence complaints with keyboard-first officer triage. |
| **Open311 Interoperability API** | "Future Scope" | GeoReport v2 Facade | Allows third-party civic apps and municipal dashboards to seamlessly interface with SamAashwas. |

---

## 2. Reframed Items (Engineering Honesty)

| Synopsis Statement | v2 Reframing | Reason |
|---|---|---|
| *"100% automated routing"* | **Confidence-gated routing with abstention** (`τ_auto = 0.80`) | A system that never abstains is 100% confident, not 100% accurate. Unknown languages, ambiguous requests, and gibberish must be routed to human triage with clear explanations. |
| *"Blockchain audit trail"* | **SHA-256 Tamper-Evident Hash Chain** | A distributed blockchain is unnecessary and inefficient for a single urban local body. A cryptographic hash chain (`prev_hash ‖ canonical_json`) with public endpoint verification provides verifiable proof of tamper-resistance. |

---

## 3. Discrepancies & Corrections

| Synopsis Claim | Finding | v2 Resolution |
|---|---|---|
| *"Tailwind CSS"* | Orphan `tailwind.config.js` exists, but 0 Tailwind utility classes are used in `index.html` or `styles.css`. | Formally dropped Tailwind in favor of the custom, hand-crafted Sticker Book CSS design system. |
| *"Spatial R-Tree in v1"* | v1 code implemented a linear scan (`for m in db.master_tickets...`). | v2 implements true spatial indexing with category-aware radii and cluster medoid tracking. |
| *"CampusHop Bus Stop Theme"* | v1 retained bus stop graphics, "All Quiet on the Bus Stop!" empty states, and mini-bus floating stickers. | Replaced with pure municipal civic graphics, hard-hat municipal inspector mascot *Aashwas-Babu*, and 24 civic floating icons. |
