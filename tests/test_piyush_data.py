from src.intent_classifier import load_dataset

def test_dataset_loading():
    df = load_dataset()
    assert len(df) >= 240
    assert "query" in df.columns
    assert "intent" in df.columns
