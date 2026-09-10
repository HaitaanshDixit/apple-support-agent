import argparse
import json
from src.classify import predict, load_model
from src.escalate import decide
from src.draft_reply import draft

def run(text, use_llm=False):
    vectorizer, clf = load_model()
    intent, confidence, all_probs = predict(text, vectorizer, clf)
    escalate, reason = decide(text, intent, confidence)
    reply, reply_source = draft(text, intent, escalate, use_llm=use_llm)

    return {
        "text": text,
        "intent": intent,
        "confidence": round(confidence, 3),
        "escalate": escalate,
        "escalate_reason": reason,
        "reply": reply,
        "reply_source": reply_source,
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--text", required=True)
    parser.add_argument("--use_llm", action="store_true")
    args = parser.parse_args()

    result = run(args.text, use_llm=args.use_llm)
    print(json.dumps(result, indent=2))
