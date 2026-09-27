# CivicSense AI: REST API Documentation

Base URL: `http://localhost:8000/api/v1`

---

## 1. Citizen Complaints

### `POST /complaints/submit`
Submit a new grievance via web portal, mobile application, or bot.

#### Request Body
```json
{
  "raw_text": "Ward 2 gali mein sewer overflow ho raha hai near Sharma General Store",
  "lat": 12.9352,
  "lon": 77.6245,
  "ward_hint": "Ward 2",
  "citizen_name": "Aarav Sharma",
  "citizen_phone": "9845012345",
  "channel": "web_portal",
  "image_category_hint": "sewage_overflow"
}
```

#### Response (`200 OK`)
```json
{
  "complaint_id": "CMP-9A4E21BC",
  "raw_text": "Ward 2 gali mein sewer overflow ho raha hai near Sharma General Store",
  "department": "Water Supply & Sewage",
  "issue_type": "Sewer Line Overflow & Blockage",
  "urgency": "High",
  "location_landmark": "Sharma General Store",
  "ward_extracted": "Koramangala 4th Block",
  "language_detected": "Hinglish",
  "lat": 12.9352,
  "lon": 77.6245,
  "channel": "web_portal",
  "citizen_name": "Aarav Sharma",
  "citizen_phone": "9845012345",
  "image_verification": {
    "is_authentic": true,
    "detected_class": "sewage_overflow",
    "confidence": 0.89,
    "mismatch_detected": false,
    "status_label": "Auto-Verified",
    "explanation": "Visual verification passed. Image depicts sewage overflow matching 'Water Supply & Sewage'."
  },
  "master_ticket_id": "MST-83F1A90B",
  "is_duplicate": true,
  "created_at": "2026-09-27T18:30:00Z"
}
```

---

## 2. ULB Officer Master Incidents

### `GET /master-tickets`
Query params: `status` (`OPEN`, `IN_PROGRESS`, `RESOLVED`)

### `GET /master-tickets/{ticket_id}`
Returns full ticket history including linked citizen submissions.

### `PATCH /master-tickets/{ticket_id}`
Update ticket status or assigned engineer.

---

## 3. Predictive Maintenance & Risk Scoring

### `GET /predictive-maintenance/ward-risk`
Calculates Ward Vulnerability Scores (0-100) using live Open-Meteo rainfall and terrain data.

### `GET /predictive-maintenance/assets`
Lists municipal infrastructure assets (drains, transformers, roads) with calculated failure probability.

---

## 4. WhatsApp Webhook

### `POST /webhook/whatsapp`
Receives inbound WhatsApp chat messages and returns automated replies.
