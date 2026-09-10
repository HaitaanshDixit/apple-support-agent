import os
import re
import json

RUBRIC = [
    "acknowledges_issue",
    "correct_next_action",
    "empathetic_tone",
    "no_fabricated_promise",
    "concise",
]

FABRICATION_PATTERNS = [
    r"\$\d+ refund guaranteed",
    r"we will waive",
    r"100% refund",
    r"free replacement guaranteed",
]

DM_INTENTS = {"software_update_device_issue", "apple_id_account_access", "billing_subscription_dispute",
              "hardware_physical_damage", "how_to_question"}

def heuristic_judge(text, intent, escalate, reply):
    scores = {}

    key_terms = [w for w in re.findall(r"[a-z]+", text.lower()) if len(w) > 4]
    scores["acknowledges_issue"] = 1 if any(term in reply.lower() for term in key_terms[:6]) or len(key_terms) == 0 else 0
    if intent == "general_complaint_or_praise":
        scores["acknowledges_issue"] = 1

    if intent in DM_INTENTS:
        scores["correct_next_action"] = 1 if "dm" in reply.lower() else 0
    else:
        scores["correct_next_action"] = 1

    negative_words = ["no.", "cant help", "not our problem", "figure it out"]
    scores["empathetic_tone"] = 0 if any(w in reply.lower() for w in negative_words) else 1

    scores["no_fabricated_promise"] = 0 if any(re.search(p, reply.lower()) for p in FABRICATION_PATTERNS) else 1

    scores["concise"] = 1 if len(reply) <= 280 else 0

    total = sum(scores.values())
    return {"subscores": scores, "total": total, "max": len(RUBRIC), "backend": "heuristic"}

def llm_judge(text, intent, escalate, reply):
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        return None
    try:
        import anthropic
    except ImportError:
        return None

    prompt = f"""Rate this customer support reply on a 0/1 scale for each criterion. Return only JSON.

Customer message: {text}
Detected intent: {intent}
Escalated to human: {escalate}
Agent reply: {reply}

Criteria:
- acknowledges_issue: does the reply show it understood the specific issue
- correct_next_action: does it ask for the right info (e.g. DM Apple ID/device model) or take the right action
- empathetic_tone: is the tone appropriate and non-dismissive
- no_fabricated_promise: does it avoid promising specific refund amounts or made-up policy
- concise: is it a reasonable length for a Twitter reply

Return JSON like: {{"acknowledges_issue": 1, "correct_next_action": 1, "empathetic_tone": 1, "no_fabricated_promise": 1, "concise": 1}}"""

    client = anthropic.Anthropic()
    resp = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=200,
        messages=[{"role": "user", "content": prompt}],
    )
    raw = resp.content[0].text.strip()
    raw = re.sub(r"^```json|```$", "", raw).strip()
    try:
        subscores = json.loads(raw)
    except json.JSONDecodeError:
        return None
    total = sum(subscores.values())
    return {"subscores": subscores, "total": total, "max": len(RUBRIC), "backend": "llm"}

def judge(text, intent, escalate, reply, use_llm=True):
    if use_llm:
        result = llm_judge(text, intent, escalate, reply)
        if result:
            return result
    return heuristic_judge(text, intent, escalate, reply)
