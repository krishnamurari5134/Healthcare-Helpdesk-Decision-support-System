"""Module owner: Swet Kumar, Purpose: Create, list and resolve escalation records in SQLite, Reviewed by: Krishna Murari"""
from contextlib import closing
from datetime import datetime
from src.database import connect

VALID_REASONS = ("low_confidence", "emergency")

def init_escalation_table(db_path=None):
    with closing(connect(db_path)) as conn, conn:
        conn.execute(
            """CREATE TABLE IF NOT EXISTS escalations (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   timestamp TEXT NOT NULL,
                   query TEXT NOT NULL,
                   reason TEXT NOT NULL,
                   priority TEXT,
                   status TEXT NOT NULL DEFAULT 'pending',
                   resolved_at TEXT
               )"""
        )

def create_escalation(query, reason, priority, db_path=None):
    if reason not in VALID_REASONS:
        raise ValueError(f"reason must be one of {VALID_REASONS}")
    init_escalation_table(db_path)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with closing(connect(db_path)) as conn, conn:
        cursor = conn.execute(
            "INSERT INTO escalations (timestamp, query, reason, priority, status) VALUES (?, ?, ?, ?, 'pending')",
            (now, query, reason, priority),
        )
        return cursor.lastrowid

def list_pending(db_path=None):
    init_escalation_table(db_path)
    with closing(connect(db_path)) as conn:
        rows = conn.execute("SELECT * FROM escalations WHERE status = 'pending' ORDER BY id").fetchall()
    return [dict(r) for r in rows]

def list_all(db_path=None):
    init_escalation_table(db_path)
    with closing(connect(db_path)) as conn:
        rows = conn.execute("SELECT * FROM escalations ORDER BY id DESC").fetchall()
    return [dict(r) for r in rows]

def mark_resolved(escalation_id, db_path=None):
    init_escalation_table(db_path)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with closing(connect(db_path)) as conn, conn:
        cursor = conn.execute(
            "UPDATE escalations SET status = 'resolved', resolved_at = ? WHERE id = ? AND status = 'pending'",
            (now, escalation_id),
        )
        return cursor.rowcount > 0
