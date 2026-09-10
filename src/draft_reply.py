import os
import re
from src.retrieve import top_matches

def strip_mention(reply_text):
    return re.sub(r"^@\S+\s*", "", reply_text).strip()

def template_draft(text, intent, escalate):
    matches = top_matches(text, intent=intent, k=3)
    base_reply = strip_mention(matches[0][0]["agent_reply"]) if matches else \
        "Sorry for the trouble, please DM us your Apple ID email so we can help."

    if escalate:
        base_reply += " We're connecting you with a specialist to make sure this is handled correctly."

    return base_reply, matches

def llm_draft(text, intent, escalate, matches):
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        return None

    try:
        import anthropic
    except ImportError:
        return None

    examples = "\n".join(
        f"- customer: {m[0]['text']}\n  agent: {strip_mention(m[0]['agent_reply'])}"
        for m in matches
    )

    prompt = f"""You are an AppleSupport agent replying on Twitter.
Intent: {intent}
Escalation status: {"escalating to a human specialist" if escalate else "handling directly"}

Similar past resolved cases:
{examples}

New customer message:
{text}

Write a short, on-brand reply (1-2 sentences, empathetic, asks for a DM with device/Apple ID details when relevant, no hashtags)."""

    client = anthropic.Anthropic()
    resp = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=200,
        messages=[{"role": "user", "content": prompt}],
    )
    return resp.content[0].text.strip()

def draft(text, intent, escalate, use_llm=True):
    base_reply, matches = template_draft(text, intent, escalate)
    if use_llm:
        llm_reply = llm_draft(text, intent, escalate, matches)
        if llm_reply:
            return llm_reply, "llm"
    return base_reply, "template"
