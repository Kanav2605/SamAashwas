# Project Decisions Log (docs/DECISIONS.md)

Record of all architectural, scope, security, and design decisions made for SamAashwas v2.

---

## Decision 1: Execution Priority — "Better UI First"
- **Context:** The user explicitly commanded: *"I want better UI first and then the next things"*.
- **Decision:** Execute Phase 1 (UI Transformation, Civic Design System, 3 Display Modes, Hash Router, 4-Step Citizen Wizard, Field Crew PWA, Officer Triage Queue, Dispatch & Risk Screens) as the immediate top priority before deep backend algorithmic refactoring.
- **Alternatives Considered:** Fixing backend security defects first (P0).
- **Rationale:** Aligns strictly with user request while ensuring UI components are ready to display real data and verification flows.

## Decision 2: Academic Prototype Transparency (Rule 4)
- **Context:** Previous UI had simulated Government of NCT of Delhi / MCD official banners with "सत्यमेव जयते".
- **Decision:** Remove all official state symbols and simulated government federation titles. Display a persistent, clear banner: *"Independent academic prototype. Not an official government service."*
- **Rationale:** Prevents impersonation, complies with Indian state emblem laws, and sets honest expectations for evaluators and citizens.

## Decision 3: Design System & Theme Bans (Sticker Book Civic)
- **Context:** Visual identity was previously split between "CampusHop Bus Stop" leftovers and neo-brutalist government portal elements.
- **Decision:** Formalize the "Sticker Book Civic" theme: flat cream paper (`#FFF6E5`), 2.5px solid ink outlines, hard offset shadows, municipal inspector mascot Aashwas-Babu, 24 civic floating SVG items, zero gradients, zero `backdrop-filter`, zero dark mode, and zero blue brand colors.
- **Rationale:** Preserves the friendly, unique, accessible aesthetic while fixing all transit/bus theme leaks (F6).

## Decision 4: Three Display Modes (Normal, Sunlight, 2G Lite)
- **Context:** Municipal staff work in bright outdoor sunlight on mobile phones with fluctuating connectivity.
- **Decision:** 
  1. *Normal Mode*: Sticker Book styling with 4 persistent skins.
  2. *Sunlight Mode*: High-contrast light mode (contrast ratio ≥ 7:1, 3.5px borders, flat cards without tilt, 56px minimum tap targets).
  3. *2G Lite Mode*: Disables raster tile maps in favor of an instant SVG ward-grid map, compresses assets, and pauses non-essential animations.
- **Rationale:** Ensures accessibility (WCAG AAA) for field crews and reliable operation in low-bandwidth Indian environments.

## Decision 5: Reframing Synopsis Claims
- **Context:** Synopsis claimed "Tailwind CSS", "100% automated routing", and "Blockchain audit trail".
- **Decision:**
  - Tailwind: Removed claim in favor of custom Sticker Book CSS tokens; logged in `docs/SYNOPSIS_DELTA.md`.
  - Routing: Reframed to confidence-gated routing (auto-route above `τ_auto = 0.80`, otherwise triage queue).
  - Blockchain: Reframed to SHA-256 tamper-evident hash-chained audit log with public verification endpoint.
- **Rationale:** Honesty in engineering defense. A system that never abstains is merely 100% confident, not 100% accurate.

## Decision 6: Hash Router & UI View Modularization
- **Context:** User requested deep linking across citizen report, field crew, officer triage, dispatch optimizer, and transparency views while maintaining single-page application speed.
- **Decision:** Implement a bidirectional hash router in `frontend/js/app.js` mapping `#/`, `#/report`, `#/track`, `#/field`, `#/officer/triage`, `#/officer/dispatch`, `#/transparency`, `#/risk`, `#/jan-sunwai`, `#/rewards`, `#/gallery` with synchronization between desktop nav tabs, mobile bottom nav, and URL hash without page reload.
- **Rationale:** Enables direct bookmarking, field crew home-screen shortcuts, and seamless navigation between citizen and officer personas.

## Decision 7: Duplicate Deflection & Endorsement Workflow (+1 Me Too)
- **Context:** Multiple citizens in the same ward often report the same civic issue within minutes of each other.
- **Decision:** In Step 2 (Where) of the report wizard, query active master incidents within 300m matching the selected category. Present up to 3 candidate issues with a `+1 Me too` button. Clicking `+1 Me too` invokes `POST /api/v1/master-tickets/{id}/endorse`, boosting priority and awarding 50 civic karma points without creating redundant duplicate tickets.
- **Rationale:** Directly resolves duplicate flooding at intake, protects municipal worker capacity, and rewards proactive civic participation.

