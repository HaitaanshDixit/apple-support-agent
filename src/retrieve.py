import csv
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

INDEX_PATH = "src/retrieval_index.pkl"

def load_train_rows(path="data/train_pool.csv"):
    with open(path, encoding="utf-8") as f:
        return list(csv.DictReader(f))

def build_index():
    rows = load_train_rows()
    texts = [r["text"] for r in rows]
    vectorizer = TfidfVectorizer(ngram_range=(1, 2), min_df=1, stop_words="english")
    X = vectorizer.fit_transform(texts)
    with open(INDEX_PATH, "wb") as f:
        pickle.dump((vectorizer, X, rows), f)
    return vectorizer, X, rows

def load_index():
    with open(INDEX_PATH, "rb") as f:
        return pickle.load(f)

def top_matches(text, intent=None, k=3, vectorizer=None, X=None, rows=None):
    if vectorizer is None:
        vectorizer, X, rows = load_index()
    q = vectorizer.transform([text])
    sims = cosine_similarity(q, X)[0]
    candidates = list(range(len(rows)))
    if intent:
        candidates = [i for i in candidates if rows[i]["intent"] == intent]
        if not candidates:
            candidates = list(range(len(rows)))
    ranked = sorted(candidates, key=lambda i: sims[i] + (0.05 if rows[i].get("source") == "real" else 0), reverse=True)[:k]
    return [(rows[i], float(sims[i])) for i in ranked]

if __name__ == "__main__":
    build_index()
    print("index built at", INDEX_PATH)
