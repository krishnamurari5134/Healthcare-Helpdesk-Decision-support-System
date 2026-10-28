from src.preprocessing import normalize, preprocess

def test_normalize():
    assert normalize("Bukhar hai!") == "fever"
    assert normalize("pet dard") == "stomach pain"
    assert normalize("") == ""
