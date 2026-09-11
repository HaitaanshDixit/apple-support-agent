import os
import re
from src.retrieve import top_matches
from src.llm_backend import generate

def strip_mention(reply_text):
    return re.sub(r"^@\S+\s*", "", reply_text).strip()

def template_draft(text, intent):
    matches = top_matches(text, intent=intent, k=3)
    base_reply = strip_mention(matches[0][0]["agent_reply"]) if matches else \
        "Sorry for the trouble, please DM us your Apple ID email so we can help."
    return base_reply, matches

    if escalate:
        base_reply += " We're connecting you with a specialist to make sure this is handled correctly."

    return base_reply, matches

def llm_draft(text, intent, matches):
    examples = "\n".join(
        f"- customer: {m[0]['text']}\n  agent: {strip_mention(m[0]['agent_reply'])}"
        for m in matches
    )

    prompt = f"""You are an AppleSupport agent replying on Twitter.
Intent: {intent}

Similar past resolved cases:
{examples}

New customer message:
{text}

Write a short, on-brand reply (1-2 sentences, empathetic, asks for a DM with device/Apple ID details when relevant, no hashtags)."""

    return generate(prompt, max_tokens=200)

def draft(text, intent, use_llm=True):
    base_reply, matches = template_draft(text, intent)
    if use_llm:
        llm_reply, backend = llm_draft(text, intent, matches)
        if llm_reply:
            return llm_reply, backend
    return base_reply, "template"