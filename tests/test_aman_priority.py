from src.priority_engine import detect_emergency, assign_priority

def test_detect_emergency():
    assert detect_emergency("chest pain hai") == "chest pain"
    assert detect_emergency("saans nahi aa rahi") == "breathing difficulty"
    assert detect_emergency("normal fever") is None

def test_assign_priority():
    assert assign_priority("chest pain hai", "symptom_guidance") == "Emergency"
    assert assign_priority("high fever and vomiting", "symptom_guidance") == "High"
    assert assign_priority("book appointment today", "appointment_booking") == "Medium"
