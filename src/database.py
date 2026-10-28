"""Module owner: Swet Kumar, Purpose: Create the SQLite log table and store/read query logs, Reviewed by: Krishna Murari"""
import sqlite3
from contextlib import closing
from datetime import datetime
from src import config

def connect(db_path=None):
    path = db_path or config.DB_PATH
    path = __import__("pathlib").Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(path))
    conn.row_factory = sqlite3.Row
    return conn

def init_db(db_path=None):
    with closing(connect(db_path)) as conn, conn:
        conn.execute(
            """CREATE TABLE IF NOT EXISTS query_logs (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   timestamp TEXT NOT NULL,
                   query TEXT NOT NULL,
                   intent TEXT,
                   confidence REAL,
                   department TEXT,
                   priority TEXT,
                   escalated INTEGER DEFAULT 0
               )"""
        )

def log_query(query, intent, confidence, department, priority, escalated, db_path=None):
    init_db(db_path)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with closing(connect(db_path)) as conn, conn:
        cursor = conn.execute(
            "INSERT INTO query_logs (timestamp, query, intent, confidence, department, priority, escalated) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (now, query, intent, round(float(confidence), 4), department, priority, 1 if escalated else 0),
        )
        return cursor.lastrowid

def get_all_logs(db_path=None):
    init_db(db_path)
    with closing(connect(db_path)) as conn:
        rows = conn.execute("SELECT * FROM query_logs ORDER BY id DESC").fetchall()
    return [dict(r) for r in rows]

def get_escalated_logs(db_path=None):
    init_db(db_path)
    with closing(connect(db_path)) as conn:
        rows = conn.execute("SELECT * FROM query_logs WHERE escalated = 1 ORDER BY id DESC").fetchall()
    return [dict(r) for r in rows]

def count_by_intent(db_path=None):
    init_db(db_path)
    with closing(connect(db_path)) as conn:
        rows = conn.execute("SELECT intent, COUNT(*) AS n FROM query_logs GROUP BY intent").fetchall()
    return {r["intent"]: r["n"] for r in rows}
