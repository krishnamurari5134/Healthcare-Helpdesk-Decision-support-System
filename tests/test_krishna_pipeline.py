from src.response_generator import process_query, validate_query

def test_validation():
    ok, err = validate_query("")
    assert ok is False
    ok, err = validate_query("Hello doctor")
    assert ok is True

def test_pipeline_emergency(tmp_path):
    db = tmp_path / "test.db"
    res = process_query("severe chest pain", db_path=db)
    assert res["valid"] is True
    assert res["priority"] == "Emergency"
    assert res["escalated"] is True
