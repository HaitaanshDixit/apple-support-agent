RISK_KEYWORDS = ["hack", "fraud", "sue", "lawsuit", "lawyer", "stole", "stolen", "identity",
                  "threat", "emergency", "danger", "dangerous", "swelling", "unsafe", "legal",
                  "spark", "fire risk", "erase it", "lock it"]
REPEAT_KEYWORDS = ["third time", "again and again", "4 messages", "3 times", "called 3 times",
                    "still no fix", "nothing has changed", "not been resolved", "5 times"]

CONFIDENCE_THRESHOLD = 0.55

def decide(text, intent, confidence):
    t = text.lower()

    for kw in RISK_KEYWORDS:
        if kw in t:
            return True, f"risk keyword matched: '{kw}'"

    for kw in REPEAT_KEYWORDS:
        if kw in t:
            return True, f"repeat-contact signal: '{kw}'"

    if confidence < CONFIDENCE_THRESHOLD:
        return True, f"low classifier confidence ({confidence:.2f} < {CONFIDENCE_THRESHOLD})"

    return False, "routine issue, matches known resolution pattern"
