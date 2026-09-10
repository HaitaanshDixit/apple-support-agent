KEYWORD_RULES = [
    ("software_update_device_issue", ["update", "ios", "battery", "crash", "freeze", "wifi", "bluetooth", "laggy", "lag"]),
    ("apple_id_account_access", ["apple id", "password", "login", "log in", "locked", "verification", "code", "2fa", "sign in"]),
    ("billing_subscription_dispute", ["charge", "charged", "refund", "subscription", "bill", "billed", "payment"]),
    ("hardware_physical_damage", ["screen", "cracked", "crack", "wont turn on", "water", "swelling", "repair", "dropped"]),
    ("how_to_question", ["how do i", "how to", "can you walk me", "does the"]),
    ("general_complaint_or_praise", []),
]

def majority_baseline(text):
    return "software_update_device_issue", 1.0

def keyword_baseline(text):
    t = text.lower()
    for intent, keywords in KEYWORD_RULES:
        for kw in keywords:
            if kw in t:
                return intent, 1.0
    return "general_complaint_or_praise", 1.0
