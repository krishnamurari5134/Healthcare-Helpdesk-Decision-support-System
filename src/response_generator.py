"""Module owner: Krishna Murari, Purpose: Combine all modules into one pipeline and build the final reply, Reviewed by: Swet Kumar"""
import re
from src import config
from src.database import log_query
from src.department_rules import get_department, get_department_info
from src.escalation import create_escalation
from src.intent_classifier import predict_intent
from src.priority_engine import assign_priority, detect_emergency
from src.retrieval import get_best_answer

UNDECIDED_DEPARTMENT = "To be decided by staff"

def validate_query(query):
    if query is None or not str(query).strip():
        return False, "Please type your question. The message cannot be empty."
    if len(str(query)) > config.MAX_QUERY_LENGTH:
        return False, f"Your message is too long. Please keep it under {config.MAX_QUERY_LENGTH} characters."
    if not re.search(r"[A-Za-z0-9]", str(query)):
        return False, "Please type your question using letters or numbers."
    return True, ""

def process_query(query, db_path=None):
    ok, error = validate_query(query)
    if not ok:
        return {"valid": False, "error": error}
    query = str(query).strip()
    intent, confidence = predict_intent(query)
    low_confidence = confidence < config.CONFIDENCE_THRESHOLD
    priority = assign_priority(query, intent, confidence)
    emergency_trigger = detect_emergency(query)
    department = get_department(query, intent, priority)

    if low_confidence and priority != "Emergency":
        department = UNDECIDED_DEPARTMENT

    kb_id = None
    if priority == "Emergency":
        answer = config.EMERGENCY_ADVICE
    elif low_confidence:
        answer = config.LOW_CONFIDENCE_ANSWER
    else:
        match = get_best_answer(query, intent)
        answer, kb_id = match["answer"], match["kb_id"]

    escalated = low_confidence or priority == "Emergency"
    reason = "emergency" if priority == "Emergency" else "low_confidence"
    log_query(query, intent, confidence, department, priority, escalated, db_path)
    if escalated:
        create_escalation(query, reason, priority, db_path)

    parts = [answer]
    info = get_department_info(department)
    if info:
        parts.append(f"Department: {department} ({info['floor']}, OPD: {info['opd_timing']})")
    elif department != "Not applicable":
        parts.append(f"Department: {department}")
    parts.append(f"Priority: {priority}")
    if escalated:
        parts.append(config.TRANSFER_MESSAGE)
    parts.append(config.DISCLAIMER)

    return {
        "valid": True, "query": query, "intent": intent, "confidence": confidence,
        "department": department, "priority": priority,
        "emergency_trigger": emergency_trigger, "low_confidence": low_confidence,
        "escalated": escalated, "escalation_reason": reason if escalated else None,
        "answer": answer, "kb_id": kb_id, "department_info": info,
        "disclaimer": config.DISCLAIMER, "full_text": "\n\n".join(parts),
    }
