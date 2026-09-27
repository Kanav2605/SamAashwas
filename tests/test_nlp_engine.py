import pytest
from backend.app.core.nlp_engine import nlp_engine, detect_language, extract_ward, extract_landmark
from backend.app.models.schemas import UrgencyEnum

def test_hinglish_language_detection():
    text_hinglish = "Bhaiya road par street light 4 din se band hai, near Sharma General Store, Ward 7"
    assert detect_language(text_hinglish) == "Hinglish"

    text_english = "The street light in front of my house has been broken for 3 days."
    assert detect_language(text_english) == "English"

def test_entity_extraction_ward_and_landmark():
    text = "Bhaiya road par street light 4 din se band hai, near Sharma General Store, Ward 7"
    ward = extract_ward(text)
    assert "7" in ward

    landmark = extract_landmark(text)
    assert "Sharma General Store" in landmark

def test_department_routing_electrical():
    text = "Bhaiya road par street light 4 din se band hai, near Sharma General Store, Ward 7"
    result = nlp_engine.analyze(text)
    assert result.department == "Electrical & Streetlighting"
    assert result.urgency in [UrgencyEnum.HIGH, UrgencyEnum.MEDIUM]

def test_department_routing_sanitation():
    text = "Kachra gadi nahi aayi 3 din se, kachra sadak pe pada hai badbu aa rahi hai"
    result = nlp_engine.analyze(text)
    assert result.department == "Sanitation & Solid Waste"

def test_department_routing_sewage():
    text = "Ward 12 gali mein sewer overflow ho raha hai, gutter ganda paani"
    result = nlp_engine.analyze(text)
    assert result.department == "Water Supply & Sewage"

def test_department_routing_roads_and_potholes():
    text = "Main road pe huge pothole hai accident hone ka chance hai, 27th Main"
    result = nlp_engine.analyze(text)
    assert result.department == "Roads & Traffic Infrastructure"
    assert result.urgency == UrgencyEnum.CRITICAL

def test_devanagari_hindi_complaint():
    text = "वार्ड ५ में सीवर का गंदा पानी बह रहा है, बदबू आ रही है"
    result = nlp_engine.analyze(text)
    assert result.language_detected == "Hindi (Devanagari)"
    assert result.department == "Water Supply & Sewage"
    assert "5" in result.ward_extracted
