---
name: civicsense-municipal-pipeline
description: >
  End-to-end municipal grievance intake, code-mixed Hinglish NLP, multimodal vision verification,
  spatio-temporal deduplication (300m spatial gate + sentence cosine similarity), and predictive
  monsoon failure risk indexing for Indian Urban Local Bodies (ULBs).
---

# CivicSense Municipal Grievance & Predictive Maintenance Skill

This skill orchestrates the end-to-end workflow for Indian Urban Local Body (ULB) civic operations:

## Workflow Steps:
1. **Intake & Multilingual Code-Mixed NLP**: Parse citizen complaints submitted in Hinglish, Hindi, or English. Extract municipal department, issue classification, landmark, ward number, and urgency level.
2. **Visual Verification**: Run cross-modal validation on uploaded photos to detect civic classes (pothole, garbage, sewer overflow, dark streetlight) and filter out spam/selfies.
3. **Geo-Semantic Deduplication**: Gated 300-meter spatial buffer check combined with sub-word TF-IDF / sentence embedding cosine similarity ($\ge 0.82$). Redundant grievances are merged into an active Master Ticket with citizen upvote count incremented.
4. **Predictive Maintenance & Risk Modeling**: Ingest Open-Meteo precipitation forecasts, elevation topography, and drainage health scores to generate real-time Ward Vulnerability Scores (0-100) ahead of monsoons.
5. **Command Center Operations**: Expose REST APIs for GIS Leaflet mapping, ticket lifecycle triage, and WhatsApp bot simulators.
