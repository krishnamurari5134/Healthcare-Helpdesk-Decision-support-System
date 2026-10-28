from src.escalation import create_escalation, list_pending, mark_resolved

def test_escalation_workflow(tmp_path):
    db = tmp_path / "test.db"
    esc_id = create_escalation("unclear query", "low_confidence", "Low", db_path=db)
    assert esc_id > 0
    pending = list_pending(db_path=db)
    assert len(pending) == 1
    assert pending[0]["status"] == "pending"
    success = mark_resolved(esc_id, db_path=db)
    assert success is True
    assert len(list_pending(db_path=db)) == 0
