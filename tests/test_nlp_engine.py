import pytest
from backend.app.core.nlp_engine import (
    nlp_engine,
    detect_language,
    extract_ward,
    extract_landmark
)
from backend.app.models.schemas import UrgencyEnum

def test_hinglish_language_detection():
    text_hinglish = "Bhaiya road par street light 4 din se band hai, near Sharma General Store, Ward 7"
    assert detect_language(text_hinglish) == "Hinglish"

    text_english = "The street light in front of my house has been broken for 3 days."
    assert detect_language(text_english) == "English"

def test_tier1_indian_languages_detection():
    # Telugu
    assert detect_language("రోడ్డుపై పెద్ద గుంత ఉంది ప్రమాదం జరిగే అవకాశం ఉంది") == "Telugu"
    # Bengali
    assert detect_language("রাস্তায় বড় গর্ত রয়েছে অবিলম্বে মেরামত প্রয়োজন") == "Bengali"
    # Urdu
    assert detect_language("سڑک پر گڑھا ہے حادثے کا خطرہ ہے") == "Urdu"
    # Punjabi
    assert detect_language("ਸੜਕ ਤੇ ਵੱਡਾ ਟੋਆ ਹੈ ਕ੍ਰਿਪਾ ਕਰਕੇ ਠੀਕ ਕਰੋ") == "Punjabi"
    # Marathi
    assert detect_language("रस्त्यावर मोठा खड्डा आहे त्वरित दुरुस्ती करावी") == "Marathi"

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
    assert result.is_abstained is False

def test_department_routing_sanitation():
    text = "Kachra gadi nahi aayi 3 din se, kachra sadak pe pada hai badbu aa rahi hai"
    result = nlp_engine.analyze(text)
    assert result.department == "Sanitation & Solid Waste"
    assert result.is_abstained is False

def test_department_routing_sewage():
    text = "Ward 12 gali mein sewer overflow ho raha hai, gutter ganda paani"
    result = nlp_engine.analyze(text)
    assert result.department == "Water Supply & Sewage"
    assert result.is_abstained is False

def test_department_routing_roads_and_potholes():
    text = "Main road pe huge pothole hai accident hone ka chance hai, 27th Main"
    result = nlp_engine.analyze(text)
    assert result.department == "Roads & Traffic Infrastructure"
    assert result.urgency == UrgencyEnum.CRITICAL
    assert result.is_abstained is False

def test_devanagari_hindi_complaint():
    text = "वार्ड ५ में सीवर का गंदा पानी बह रहा है, बदबू आ रही है"
    result = nlp_engine.analyze(text)
    assert result.language_detected == "Hindi (Devanagari)"
    assert result.department == "Water Supply & Sewage"
    assert "5" in result.ward_extracted
    assert result.is_abstained is False

def test_negation_window_suppression():
    # "no pothole" should NOT classify into Roads if it's explicitly negated
    text = "Everything is fine here, there is no pothole on the road"
    result = nlp_engine.analyze(text)
    # Because pothole is negated, it shouldn't score for Roads and should abstain
    assert result.is_abstained is True

def test_abstention_on_non_civic_text():
    # Non-civic input should abstain and route to Triage & Verification Queue
    text = "Please order two large cheese pizzas with extra olives and coke"
    result = nlp_engine.analyze(text)
    assert result.is_abstained is True
    assert result.department == "Triage & Verification Queue"

def test_wrong_door_jurisdiction_detection():
    # NHAI
    text_nhai = "Huge pothole on NH-44 highway near toll plaza accident risk"
    res_nhai = nlp_engine.analyze(text_nhai)
    assert res_nhai.is_wrong_door is True
    assert "NHAI" in res_nhai.jurisdiction
    assert "1033" in res_nhai.wrong_door_advice

    # Indian Railways
    text_rail = "Water logging near railway track and train station platform"
    res_rail = nlp_engine.analyze(text_rail)
    assert res_rail.is_wrong_door is True
    assert "Railways" in res_rail.jurisdiction
    assert "RailMadad" in res_rail.wrong_door_advice
