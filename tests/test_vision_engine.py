import pytest
from backend.app.core.vision_engine import vision_engine

def test_authentic_matching_photo():
    # Garbage complaint with garbage photo
    result = vision_engine.verify_image(
        text_complaint="Kachra nahi uthaya gaya hai 3 din se",
        department="Sanitation & Solid Waste",
        image_category_hint="garbage_dump"
    )
    assert result is not None
    assert result.is_authentic is True
    assert result.mismatch_detected is False
    assert result.status_label == "Auto-Verified"

def test_mismatched_photo():
    # Electrical complaint with pothole photo
    result = vision_engine.verify_image(
        text_complaint="Streetlight band hai",
        department="Electrical & Streetlighting",
        image_category_hint="pothole"
    )
    assert result is not None
    assert result.is_authentic is False
    assert result.mismatch_detected is True
    assert result.status_label == "Possible Spam / Flagged"

def test_spam_or_selfie_detection():
    result = vision_engine.verify_image(
        text_complaint="Road repair needed",
        department="Roads & Traffic Infrastructure",
        image_category_hint="unrelated_or_spam"
    )
    assert result is not None
    assert result.is_authentic is False
    assert "spam" in result.explanation.lower()
