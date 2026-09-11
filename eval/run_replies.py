import csv
from src.pipeline import run
from eval.judge import judge

def main():
    with open("eval/golden_eval.csv", encoding="utf-8") as f:
        golden = list(csv.DictReader(f))

    out_rows = []
    for row in golden:
        result = run(row["text"], use_llm=False)
        j = judge(row["text"], result["intent"], result["escalate"], result["reply"], use_llm=False)
        out_rows.append({
            "id": row["id"],
            "text": row["text"],
            "gold_intent": row["gold_intent"],
            "pred_intent": result["intent"],
            "confidence": result["confidence"],
            "gold_escalate": row["gold_escalate"],
            "pred_escalate": result["escalate"],
            "escalate_reason": result["escalate_reason"],
            "internal_note": result["internal_note"],
            "reply": result["reply"],
            "judge_total": j["total"],
            "judge_subscores": j["subscores"],
        })

    with open("eval/pipeline_outputs.csv", "w", newline="", encoding="utf-8") as f:
        fieldnames = list(out_rows[0].keys())
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(out_rows)

    avg_judge = sum(r["judge_total"] for r in out_rows) / len(out_rows)
    print(f"wrote {len(out_rows)} rows to eval/pipeline_outputs.csv")
    print(f"average judge score: {avg_judge:.2f} / 5")

if __name__ == "__main__":
    main()
