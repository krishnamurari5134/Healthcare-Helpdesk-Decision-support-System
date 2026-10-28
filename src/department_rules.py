"""Module owner: Aman Tiwari, Purpose: Map intent and keywords to a hospital department, Reviewed by: Swet Kumar"""
import json
import re
from src import config
from src.preprocessing import normalize

KEYWORD_MAP = [
    ("Pediatrics", ["child", "children", "baby", "infant", "kid", "kids", "toddler", "newborn", "pediatric", "pediatrics", "pediatrician"]),
    ("Emergency", ["emergency", "ambulance", "trauma", "casualty"]),
    ("Cardiology", ["heart", "chest", "cardiac", "cardiology", "cardiologist", "blood pressure", "palpitations", "ecg"]),
    ("Neurology", ["head", "headache", "migraine", "neurology", "neurologist", "seizure", "dizziness", "brain", "nerve", "numbness"]),
    ("Orthopedics", ["bone", "fracture", "joint", "knee", "back", "spine", "orthopedic", "orthopedics", "shoulder", "ankle"]),
    ("ENT", ["ear", "nose", "throat", "sinus", "ent", "hearing", "tonsil"]),
    ("Dermatology", ["skin", "rash", "itching", "acne", "allergy", "dermatology", "hair", "eczema"]),
    ("Gynecology", ["pregnancy", "pregnant", "period", "periods", "gynecology", "gynecologist", "menstrual", "ovary", "uterus"]),
    ("Radiology/Lab", ["x ray", "mri", "ct scan", "scan", "ultrasound", "sonography", "blood test", "lab", "pathology", "urine test", "radiology"]),
    ("Billing", ["billing", "bill", "fee", "fees", "payment", "insurance", "tpa"]),
    ("General Medicine", ["fever", "cold", "cough", "stomach", "vomiting", "diarrhea", "weakness", "tired", "acidity", "physician", "diabetes", "thyroid", "general medicine"]),
]

def get_department(text, intent, priority=None):
    if priority == "Emergency" or intent == "emergency":
        return "Emergency"
    if intent == "billing_insurance":
        return "Billing"
    if intent == "report_enquiry":
        return "Radiology/Lab"
    if intent == "general_greeting_other":
        return "Not applicable"
    clean = normalize(text)
    for department, keywords in KEYWORD_MAP:
        for keyword in keywords:
            if re.search(r"\b" + re.escape(keyword) + r"\b", clean):
                return department
    return "General Medicine"

def get_department_info(name):
    with open(config.DEPARTMENTS_PATH, encoding="utf-8") as f:
        for dept in json.load(f):
            if dept["name"] == name:
                return dept
    return None
