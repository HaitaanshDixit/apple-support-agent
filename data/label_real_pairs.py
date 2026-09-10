import csv

LABELS = {
    "119248": ("software_update_device_issue", "train"),
    "119252": ("software_update_device_issue", "train"),
    "119262": ("software_update_device_issue", "train"),
    "119267": ("software_update_device_issue", "train"),
    "119269": ("software_update_device_issue", "train"),
    "119271": ("software_update_device_issue", "train"),
    "119279": ("software_update_device_issue", "train"),
    "119289": ("software_update_device_issue", "train"),
    "119293": ("software_update_device_issue", "golden"),
    "119298": ("apple_id_account_access", "golden"),
    "119300": ("software_update_device_issue", "golden"),
    "119323": ("software_update_device_issue", "golden"),
    "119325": ("software_update_device_issue", "golden"),
}

def main():
    with open("data/apple_support_real_pairs.csv", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    out = []
    for r in rows:
        intent, split = LABELS[r["tweet_id"]]
        out.append({
            "tweet_id": r["tweet_id"],
            "author": f"real_customer_{r['tweet_id']}",
            "text": r["customer_text"],
            "intent": intent,
            "agent_reply": r["agent_reply"],
            "source": "real",
            "split": split,
        })

    with open("data/apple_real_labeled.csv", "w", newline="", encoding="utf-8") as f:
        fieldnames = ["tweet_id", "author", "text", "intent", "agent_reply", "source", "split"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(out)

    print(f"labeled {len(out)} real rows: "
          f"{sum(1 for r in out if r['split']=='train')} train / "
          f"{sum(1 for r in out if r['split']=='golden')} golden")

if __name__ == "__main__":
    main()
