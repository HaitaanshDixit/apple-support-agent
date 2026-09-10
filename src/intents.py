INTENTS = [
    "software_update_device_issue",
    "apple_id_account_access",
    "billing_subscription_dispute",
    "hardware_physical_damage",
    "how_to_question",
    "general_complaint_or_praise",
]

INTENT_DESCRIPTIONS = {
    "software_update_device_issue": "battery drain, app crashes, freezing, wifi/bluetooth problems after an iOS update",
    "apple_id_account_access": "cant log in, forgot password, verification code not arriving, locked account",
    "billing_subscription_dispute": "unexpected App Store/iCloud/Apple Music charge, refund request, subscription cancellation",
    "hardware_physical_damage": "cracked screen, wont power on, water damage, battery swelling, physical repair",
    "how_to_question": "how do i do X, feature question, setup question, no problem being reported",
    "general_complaint_or_praise": "general venting, compliment, or something that doesn't fit the above",
}

REAL_DATA_GROUNDED_INTENTS = {
    "software_update_device_issue": 12,
    "apple_id_account_access": 1,
}
