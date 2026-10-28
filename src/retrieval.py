"""Module owner: Swet Kumar, Purpose: Return the most similar predefined KB answer, Reviewed by: Aman Tiwari"""
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from src import config
from src.preprocessing import preprocess

_RETRIEVER = None

class Retriever:
    def __init__(self, kb_path=None):
        with open(kb_path or config.KB_PATH, encoding="utf-8") as f:
            self.entries = json.load(f)
        self.vectorizer = TfidfVectorizer(preprocessor=preprocess, ngram_range=(1, 2))
        corpus = [e["question"] + " " + e.get("keywords", "") for e in self.entries]
        self.matrix = self.vectorizer.fit_transform(corpus)

    def get_best_answer(self, query, intent=None):
        candidates = [i for i, e in enumerate(self.entries) if e["intent"] == intent]
        if not candidates:
            candidates = list(range(len(self.entries)))
        query_vector = self.vectorizer.transform([query])
        scores = cosine_similarity(query_vector, self.matrix[candidates])[0]
        best_pos = int(scores.argmax())
        best_score = float(scores[best_pos])
        best_index = candidates[best_pos]

        if best_score < config.RETRIEVAL_MIN_SCORE:
            for i in candidates:
                if self.entries[i].get("default"):
                    best_index = i
                    break
        entry = self.entries[best_index]
        return {"answer": entry["answer"], "score": best_score, "kb_id": entry["id"]}

def get_best_answer(query, intent=None):
    global _RETRIEVER
    if _RETRIEVER is None:
        _RETRIEVER = Retriever()
    return _RETRIEVER.get_best_answer(query, intent)
