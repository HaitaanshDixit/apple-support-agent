import csv
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

MODEL_PATH = "src/intent_model.pkl"

def load_train_rows(path="data/train_pool.csv"):
    with open(path, encoding="utf-8") as f:
        return list(csv.DictReader(f))

def train():
    rows = load_train_rows()
    texts = [r["text"] for r in rows]
    labels = [r["intent"] for r in rows]

    vectorizer = TfidfVectorizer(ngram_range=(1, 2), min_df=2, stop_words="english")
    X = vectorizer.fit_transform(texts)

    clf = LogisticRegression(max_iter=1000, C=5.0, class_weight="balanced")
    clf.fit(X, labels)

    with open(MODEL_PATH, "wb") as f:
        pickle.dump((vectorizer, clf), f)

    return vectorizer, clf

def load_model():
    with open(MODEL_PATH, "rb") as f:
        return pickle.load(f)

def predict(text, vectorizer=None, clf=None):
    if vectorizer is None or clf is None:
        vectorizer, clf = load_model()
    X = vectorizer.transform([text])
    probs = clf.predict_proba(X)[0]
    classes = clf.classes_
    best_idx = probs.argmax()
    return classes[best_idx], float(probs[best_idx]), dict(zip(classes, probs))

if __name__ == "__main__":
    train()
    print("trained and saved to", MODEL_PATH)
