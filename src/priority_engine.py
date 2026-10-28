"""Module owner: Aman Tiwari, Purpose: Assign Low/Medium/High/Emergency priority using keyword rules, Reviewed by: Krishna Murari"""
import re
from src import config
from src.preprocessing import normalize

EMERGENCY_PATTERNS = [
    ("chest pain", r"chest\W+(?:\w+\W+){0,2}?pain|pain\W+(?:\w+\W+){0,2}?chest"),
    ("heart attack", r"heart\W+attack"),
    ("breathing difficulty", r"breath\w*\W+(?:\w+\W+){0,3}?(?:not|problem|difficult\w*|trouble|stopped)\b|\b(?:cannot|unable|difficulty|trouble|problem)\W+(?:\w+\W+){0,3}?breath|\bnot\W+breath|short\w*\W+of\W+breath"),
    ("unconscious", r"unconscious|fainted|passed\W+out|collapsed|not\W+responding|unresponsive|consciousness\W+(?:\w+\W+){0,2}?not"),
    ("severe bleeding", r"(?:severe|heavy|excessive|profuse)\W+bleeding|bleeding\W+(?:\w+\W+){0,3}?(?:not\W+stop|will\W+not\W+stop)|blood\W+(?:\w+\W+){0,3}?(?:flowing|bleeding)"),
    ("stroke", r"\bstroke\b|face\W+(?:\w+\W+){0,2}?drooping|slurred\W+speech|speech\W+(?:\w+\W+){0,2}?slurred"),
    ("poisoning", r"poison\w*|overdose"),
    ("seizure", r"seizure|convulsion"),
    ("accident", r"accident|ambulance"),
]

HIGH_PATTERNS = [
    r"\bsevere\b", r"unbearable", r"high\W+fever", r"fracture", r"broken",
    r"(?:vomit\w*|stool|urine|cough\w*)\W+(?:\w+\W+){0,2}?blood",
    r"blood\W+(?:\w+\W+){0,2}?(?:vomit\w*|stool|urine)",
]

URGENT_PATTERNS = [r"urgent", r"\basap\b", r"immediately", r"\btoday\b", r"\bnow\b"]

def detect_emergency(text):
    clean = normalize(text)
    for label, pattern in EMERGENCY_PATTERNS:
        if re.search(pattern, clean):
            return label
    return None

def assign_priority(text, intent, confidence=None):
    if detect_emergency(text):
        return "Emergency"
    sure = confidence is None or confidence >= config.CONFIDENCE_THRESHOLD
    if intent == "emergency" and sure:
        return "Emergency"
    clean = normalize(text)
    if intent == "symptom_guidance":
        if any(re.search(p, clean) for p in HIGH_PATTERNS):
            return "High"
        return "Medium"
    if any(re.search(p, clean) for p in URGENT_PATTERNS):
        return "Medium"
    return "Low"
