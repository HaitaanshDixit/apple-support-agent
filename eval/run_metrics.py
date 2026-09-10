import csv
import json
from sklearn.metrics import precision_recall_fscore_support
from src.classify import load_model, predict
from src.escalate import decide
from eval.baselines import majority_baseline, keyword_baseline

def load_golden(path="eval/golden_eval.csv"):
    with open(path, encoding="utf-8") as f:
        return list(csv.DictReader(f))

def bool_from_str(s):
    return s.strip().lower() == "true"

def eval_intent(golden, predict_fn, name):
    y_true = []
    y_pred = []
    for row in golden:
        pred, _ = predict_fn(row["text"])
        y_true.append(row["gold_intent"])
        y_pred.append(pred)

    precision, recall, f1, _ = precision_recall_fscore_support(y_true, y_pred, average="macro", zero_division=0)
    acc = sum(1 for a, b in zip(y_true, y_pred) if a == b) / len(y_true)
    print(f"\n=== Intent classifier: {name} ===")
    print(f"accuracy={acc:.3f} macro_precision={precision:.3f} macro_recall={recall:.3f} macro_f1={f1:.3f}")
    return {"name": name, "accuracy": acc, "macro_precision": precision, "macro_recall": recall, "macro_f1": f1}

def eval_our_model(golden):
    vectorizer, clf = load_model()
    def fn(text):
        intent, conf, _ = predict(text, vectorizer, clf)
        return intent, conf
    return eval_intent(golden, fn, "ours_tfidf_logreg")

def eval_by_source(golden):
    vectorizer, clf = load_model()
    sources = sorted(set(r["source"] for r in golden))
    for src in sources:
        subset = [r for r in golden if r["source"] == src]
        correct = 0
        for row in subset:
            pred, _, _ = predict(row["text"], vectorizer, clf)
            if pred == row["gold_intent"]:
                correct += 1
        print(f"  {src}: {correct}/{len(subset)} = {correct/len(subset):.3f}")

def eval_escalation(golden):
    vectorizer, clf = load_model()
    y_true = []
    y_pred_ours = []
    y_pred_always_auto = []
    y_pred_always_escalate = []

    for row in golden:
        gold = bool_from_str(row["gold_escalate"])
        y_true.append(gold)

        intent, conf, _ = predict(row["text"], vectorizer, clf)
        escalate, _ = decide(row["text"], intent, conf)
        y_pred_ours.append(escalate)
        y_pred_always_auto.append(False)
        y_pred_always_escalate.append(True)

    results = {}
    for name, preds in [("ours", y_pred_ours), ("always_auto_handle", y_pred_always_auto), ("always_escalate", y_pred_always_escalate)]:
        precision, recall, f1, _ = precision_recall_fscore_support(y_true, preds, average="binary", zero_division=0)
        acc = sum(1 for a, b in zip(y_true, preds) if a == b) / len(y_true)
        print(f"\n=== Escalation policy: {name} ===")
        print(f"accuracy={acc:.3f} precision={precision:.3f} recall={recall:.3f} f1={f1:.3f}")
        results[name] = {"accuracy": acc, "precision": precision, "recall": recall, "f1": f1}
    return results

def main():
    golden = load_golden()
    print(f"golden set size: {len(golden)}")

    intent_results = []
    intent_results.append(eval_intent(golden, majority_baseline, "trivial_majority_class"))
    intent_results.append(eval_intent(golden, keyword_baseline, "simple_keyword_rules"))
    intent_results.append(eval_our_model(golden))

    print("\n=== Intent accuracy by source (real vs synthetic vs edge case) ===")
    eval_by_source(golden)

    escalation_results = eval_escalation(golden)

    out = {"intent_results": intent_results, "escalation_results": escalation_results}
    with open("eval/metrics_summary.json", "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2)
    print("\nsaved eval/metrics_summary.json")

if __name__ == "__main__":
    main()
