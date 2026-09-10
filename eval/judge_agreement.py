import csv
from scipy.stats import pearsonr
from sklearn.metrics import cohen_kappa_score

def main():
    with open("eval/judge_agreement_sample.csv", encoding="utf-8") as f:
        machine = {r["id"]: int(r["judge_total"]) for r in csv.DictReader(f, fieldnames=["id","text","pred_intent","pred_escalate","reply","judge_total"])}

    with open("eval/human_scores.csv", encoding="utf-8") as f:
        human = {r["id"]: int(r["human_total"]) for r in csv.DictReader(f)}

    ids = list(human.keys())
    y_machine = [machine[i] for i in ids]
    y_human = [human[i] for i in ids]

    corr, pval = pearsonr(y_machine, y_human)

    threshold = 4
    machine_bin = [1 if v >= threshold else 0 for v in y_machine]
    human_bin = [1 if v >= threshold else 0 for v in y_human]
    kappa = cohen_kappa_score(machine_bin, human_bin)
    agree_rate = sum(1 for a, b in zip(machine_bin, human_bin) if a == b) / len(ids)

    print(f"n={len(ids)}")
    print(f"pearson correlation (raw 0-5 scores): {corr:.3f} (p={pval:.3f})")
    print(f"binary agreement rate (>=4 = good): {agree_rate:.3f}")
    print(f"cohen kappa (binary good/bad): {kappa:.3f}")

    disagreements = [(i, machine[i], human[i]) for i in ids if abs(machine[i] - human[i]) >= 2]
    print(f"\nlarge disagreements (diff >= 2): {len(disagreements)}")
    for i, m, h in disagreements:
        print(f"  id={i} judge={m} human={h}")

if __name__ == "__main__":
    main()
