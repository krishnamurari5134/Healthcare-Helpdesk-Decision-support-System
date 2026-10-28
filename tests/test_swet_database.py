from src.database import log_query, get_all_logs

def test_database_logging(tmp_path):
    db = tmp_path / "test.db"
    log_id = log_query("test query", "general_greeting_other", 0.95, "Not applicable", "Low", 0, db_path=db)
    assert log_id > 0
    logs = get_all_logs(db_path=db)
    assert len(logs) == 1
    assert logs[0]["query"] == "test query"
