"""Module owner: Mohd. Arsalan, Purpose: Text normalization, stopword removal and Hinglish spelling mapping, Reviewed by: Krishna Murari"""
import re

HINGLISH_MAP = {
    "bukhar": "fever",
    "fever": "fever",
    "dard": "pain",
    "sir dard": "headache",
    "pet dard": "stomach pain",
    "saans": "breath",
    "ulti": "vomit",
    "dast": "diarrhea",
    "khasi": "cough",
    "zukam": "cold",
    "chakkar": "dizziness",
    "khoon": "blood",
    "haddi": "bone",
    "joro": "joint",
    "kamzori": "weakness",
    "thakawat": "fatigue",
    "bp": "blood pressure",
}

STOPWORDS = {
    "hai", "hain", "ko", "se", "mein", "aur", "ki", "ka", "ke", "kya", "kese",
    "kaise", "mujhe", "mera", "meri", "ek", "yeh", "woh", "par", "ho", "raha",
    "rahi", "the", "tha", "to", "hi", "bhi", "please", "help", "kardo", "di",
    "do", "kijiye", "batao", "bataiye"
}

def normalize(text):
    if not text:
        return ""
    text = str(text).lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    tokens = text.split()
    tokens = [HINGLISH_MAP.get(t, t) for t in tokens]
    tokens = [t for t in tokens if t not in STOPWORDS]
    return " ".join(tokens)

def preprocess(text):
    return normalize(text)
