"""Module owner: Mohd. Arsalan, Purpose: Central configuration for paths and constants, Reviewed by: Krishna Murari"""
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
MODELS_DIR = BASE_DIR / "models"
DOCS_DIR = BASE_DIR / "docs"

QUERIES_CSV = DATA_DIR / "queries.csv"
KB_PATH = DATA_DIR / "knowledge_base.json"
DEPARTMENTS_PATH = DATA_DIR / "departments.json"
DB_PATH = BASE_DIR / "helpdesk.db"
MODEL_PATH = MODELS_DIR / "intent_model.pkl"

CONFIDENCE_THRESHOLD = 0.60
RETRIEVAL_MIN_SCORE = 0.30
MAX_QUERY_LENGTH = 500
TEST_SIZE = 0.20
RANDOM_STATE = 42

DISCLAIMER = (
    "DISCLAIMER: This decision support system is for informational and "
    "navigational support only. It does NOT provide medical diagnoses or "
    "prescribe medicines. Please consult a qualified doctor for medical advice."
)

EMERGENCY_ADVICE = (
    "EMERGENCY DETECTED: This sounds like a medical emergency. "
    "Please call emergency services immediately:\n"
    "- National Emergency Number (India): 112\n"
    "- Ambulance: 108\n"
    "Or visit the nearest hospital emergency room (Casualty) right away."
)

LOW_CONFIDENCE_ANSWER = (
    "We could not classify your query with high confidence. "
    "Your request has been flagged for review by our human helpdesk staff."
)

TRANSFER_MESSAGE = "This query will be transferred to human helpdesk staff."
