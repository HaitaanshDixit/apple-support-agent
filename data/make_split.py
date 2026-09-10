import csv
import random

random.seed(11)

FIELDS = ["tweet_id", "author", "text", "intent", "agent_reply", "source"]

def main():
    with open("data/apple_synthetic_corpus.csv", encoding="utf-8") as f:
        synthetic = list(csv.DictReader(f))

    with open("data/apple_real_labeled.csv", encoding="utf-8") as f:
        real = list(csv.DictReader(f))

    real_train = [r for r in real if r["split"] == "train"]
    real_golden = [r for r in real if r["split"] == "golden"]

    random.shuffle(synthetic)
    synth_train = synthetic[:80]
    synth_held_out = synthetic[80:]

    train_pool = real_train + synth_train
    held_out_pool = synth_held_out

    with open("data/train_pool.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        for r in train_pool:
            writer.writerow({k: r[k] for k in FIELDS})

    with open("data/held_out_pool.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        for r in held_out_pool:
            writer.writerow({k: r[k] for k in FIELDS})

    with open("data/real_golden_rows.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        for r in real_golden:
            writer.writerow({k: r[k] for k in FIELDS})

    print(f"train_pool={len(train_pool)} (real={len(real_train)}, synthetic={len(synth_train)})")
    print(f"held_out_pool={len(held_out_pool)}")
    print(f"real_golden_rows={len(real_golden)}")

if __name__ == "__main__":
    main()
