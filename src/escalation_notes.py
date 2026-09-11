RISK_NOTE = "Flag for a human specialist: this message contains a safety, fraud, or legal risk signal and should not be auto-resolved."
REPEAT_NOTE = "Flag for a human specialist: this customer has contacted us multiple times about the same unresolved issue."
CONFIDENCE_NOTE = "Flag for a human specialist: the intent classifier had low confidence on this message."
DEFAULT_NOTE = "Flag for a human specialist."

def escalation_note_for_reason(reason):
    if "risk keyword" in reason:
        return RISK_NOTE
    if "repeat-contact" in reason:
        return REPEAT_NOTE
    if "confidence" in reason:
        return CONFIDENCE_NOTE
    return DEFAULT_NOTE