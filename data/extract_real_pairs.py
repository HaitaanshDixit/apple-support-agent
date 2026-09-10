import csv

def main():
    with open("data/twcs_sample_raw.csv", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    by_id = {r["tweet_id"]: r for r in rows}
    apple_replies = [r for r in rows if r["author_id"] == "AppleSupport"]

    out_rows = []
    for r in apple_replies:
        parent = by_id.get(r["in_response_to_tweet_id"])
        customer_text = parent["text"] if parent else ""
        out_rows.append({
            "tweet_id": r["tweet_id"],
            "customer_tweet_id": parent["tweet_id"] if parent else "",
            "customer_text": customer_text,
            "agent_reply": r["text"],
        })

    with open("data/apple_support_real_pairs.csv", "w", newline="", encoding="utf-8") as f:
        fieldnames = ["tweet_id", "customer_tweet_id", "customer_text", "agent_reply"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(out_rows)

    print(f"extracted {len(out_rows)} real AppleSupport reply pairs")

if __name__ == "__main__":
    main()
