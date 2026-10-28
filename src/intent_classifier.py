"""Module owner: Krishna Murari, Purpose: Train, save, load and use the intent classifier, Reviewed by: Swet Kumar"""
import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from src import config
from src.preprocessing import preprocess

_MODEL = None

def load_dataset(csv_path=None):
    df = pd.read_csv(csv_path or config.QUERIES_CSV)
    return df.dropna(subset=["query", "intent"]).reset_index(drop=True)

def build_model():
    return Pipeline([
        ("tfidf", TfidfVectorizer(preprocessor=preprocess, ngram_range=(1, 2), sublinear_tf=True)),
        ("clf", LogisticRegression(C=10, max_iter=1000)),
    ])

def split_data(df):
    return train_test_split(
        df["query"], df["intent"],
        test_size=config.TEST_SIZE,
        random_state=config.RANDOM_STATE,
        stratify=df["intent"],
    )

def train_and_save(csv_path=None, model_path=None):
    global _MODEL
    df = load_dataset(csv_path)
    model = build_model()
    model.fit(df["query"], df["intent"])
    path = model_path or config.MODEL_PATH
    path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, path)
    _MODEL = model
    return model

def load_model():
    global _MODEL
    if _MODEL is None:
        if config.MODEL_PATH.exists():
            _MODEL = joblib.load(config.MODEL_PATH)
        else:
            _MODEL = train_and_save()
    return _MODEL

def predict_intent(text):
    model = load_model()
    probabilities = model.predict_proba([text])[0]
    best = probabilities.argmax()
    return str(model.classes_[best]), float(probabilities[best])
