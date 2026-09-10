import csv

RISK_KEYWORDS = ["hack", "fraud", "sue", "lawsuit", "lawyer", "stole", "stolen", "identity",
                  "threat", "emergency", "danger", "dangerous", "swelling", "unsafe", "legal",
                  "spark", "fire risk", "erase it", "lock it"]
REPEAT_KEYWORDS = ["third time", "again and again", "4 messages", "3 times", "called 3 times",
                    "still no fix", "nothing has changed", "not been resolved", "5 times"]

edge_manual_escalate = {
    "910001": (True, "account takeover, needs urgent human verification"),
    "910002": (True, "legal threat mentioned"),
    "910003": (True, "stolen device, needs urgent account/security action"),
    "910004": (True, "possible fraud, unauthorized charge"),
    "910005": (True, "battery safety hazard"),
    "910006": (False, "venting about wait time, routine acknowledgment"),
    "910007": (False, "routine repair cost question"),
    "910008": (False, "routine troubleshooting"),
    "910009": (False, "routine billing question, no risk signal"),
    "910010": (False, "routine product question"),
    "910011": (True, "repeated unresolved complaint, 3rd contact"),
    "910012": (False, "no signal is a routine troubleshooting case despite anxious framing"),
    "910013": (False, "farewell/compliment, no action needed"),
    "910014": (True, "account disabled without explanation needs human review"),
    "910015": (True, "possible unauthorized account use"),
    "910016": (False, "routine pre-update question"),
    "910017": (False, "routine subscription cancellation plus bug report"),
    "910018": (True, "payment discrepancy, money left account, needs verification"),
    "910019": (False, "routine store hours question"),
    "910020": (True, "complaint about rep conduct, needs human review"),
    "910021": (True, "device safety hazard"),
    "910022": (False, "compliment, no action needed"),
    "910023": (True, "identity theft concern"),
    "910024": (False, "routine pricing question"),
    "910025": (True, "repeated unresolved issue, 4 prior contacts"),
    "910026": (False, "routine document request"),
    "910027": (False, "routine discount question"),
    "910028": (False, "billing dispute but routine, no risk keyword"),
    "910029": (False, "retention question, but not yet a cancellation request"),
    "910030": (True, "stolen device, needs urgent account action"),
    "910031": (False, "routine how-to question"),
    "910032": (True, "water damage plus device wont power on, safety-adjacent hardware case"),
    "910033": (False, "frustration about lack of response, routine acknowledgment"),
    "910034": (True, "repeated failed verification, account access risk"),
    "910035": (False, "routine hardware troubleshooting"),
    "910036": (False, "routine trade-in question"),
    "910037": (True, "billing error despite active AppleCare, needs review"),
    "910038": (False, "compliment, no action needed"),
    "910039": (False, "routine software issue despite dramatic framing"),
    "910040": (False, "routine how-to question"),
    "910041": (True, "account hacked with unauthorized purchases"),
    "910042": (True, "repeated unresolved issue, 3 prior contacts"),
    "910043": (False, "routine product question"),
    "910044": (True, "spark near charging port, safety hazard"),
    "910045": (False, "compliment, no action needed"),
}

real_golden_escalate = {
    "119293": (False, "routine battery complaint, matches known resolution pattern"),
    "119298": (False, "routine account/App Store code issue, matches known resolution pattern"),
    "119300": (False, "routine software update complaint, matches known resolution pattern"),
    "119323": (False, "routine software update complaint, matches known resolution pattern"),
    "119325": (False, "routine software update complaint, matches known resolution pattern"),
}

def score_risk(text):
    t = text.lower()
    for kw in RISK_KEYWORDS:
        if kw in t:
            return True, f"risk keyword matched: '{kw}'"
    for kw in REPEAT_KEYWORDS:
        if kw in t:
            return True, f"repeat-contact signal: '{kw}'"
    return False, ""

def main():
    rows_out = []

    with open("data/held_out_pool.csv", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            escalate, reason = score_risk(r["text"])
            if not escalate:
                reason = "routine issue, matches known resolution pattern"
            rows_out.append({
                "id": r["tweet_id"],
                "text": r["text"],
                "gold_intent": r["intent"],
                "gold_escalate": escalate,
                "gold_escalate_reason": reason,
                "source": "held_out_synthetic",
            })

    with open("data/real_golden_rows.csv", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            escalate, reason = real_golden_escalate[r["tweet_id"]]
            rows_out.append({
                "id": r["tweet_id"],
                "text": r["text"],
                "gold_intent": r["intent"],
                "gold_escalate": escalate,
                "gold_escalate_reason": reason,
                "source": "real",
            })

    with open("data/edge_cases.csv", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            tid = r["tweet_id"]
            escalate, reason = edge_manual_escalate.get(tid, (False, "unreviewed"))
            rows_out.append({
                "id": tid,
                "text": r["text"],
                "gold_intent": r["intent"],
                "gold_escalate": escalate,
                "gold_escalate_reason": reason,
                "source": "edge_case",
            })

    with open("eval/golden_eval.csv", "w", newline="", encoding="utf-8") as f:
        fieldnames = ["id", "text", "gold_intent", "gold_escalate", "gold_escalate_reason", "source"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows_out)

    print(f"wrote {len(rows_out)} golden examples")
    from collections import Counter
    print(Counter(r["source"] for r in rows_out))

if __name__ == "__main__":
    main()
