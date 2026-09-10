import csv
import random

def main():
    random.seed(3)
    with open("eval/pipeline_outputs.csv", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    sample = random.sample(rows, 30)
    with open("eval/judge_agreement_sample.csv", "w", newline="", encoding="utf-8") as f:
        fieldnames = ["id", "text", "pred_intent", "pred_escalate", "reply", "judge_total"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        for r in sample:
            writer.writerow({k: r[k] for k in fieldnames})
    print(f"wrote {len(sample)} rows to eval/judge_agreement_sample.csv")

if __name__ == "__main__":
    main()
