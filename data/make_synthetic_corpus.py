import csv
import random

random.seed(7)

names = ["jake", "maria", "tom", "priya", "chris", "dana", "alex", "sam", "nicole", "marcus",
         "leah", "omar", "kelly", "ryan", "sofia", "derek", "amy", "ben", "tara", "victor"]

software_update = [
    "phone has been frozen since i updated to the new ios, apps wont even open",
    "battery drains so fast after this update, from 100 to 40 in an hour",
    "wifi keeps disconnecting every few minutes since i updated my phone",
    "apps keep crashing constantly after the latest ios update",
    "my phone is so laggy since the update, everything takes forever to load",
    "bluetooth wont connect to my car since i updated to the new ios",
    "phone overheats now every time i open the camera after updating",
    "screen keeps flickering since the software update last week",
    "cant believe how bad my battery life got after this update, its unusable",
    "keyboard is lagging so bad since i updated, this update is a disaster",
]
software_update_replies = [
    "Thanks for reaching out to us. We are always happy to help. Send us a DM so we can look into this together.",
    "We'd love to help! Please DM us and let us know any steps you've tried since experiencing these behaviors.",
    "Battery life is important, and we're here for you. DM us the iOS version your iPhone is running. We'll go from there.",
    "Let's take a look. What is the exact iOS you're using? Are you using any specific apps when noticing this? DM us your reply.",
    "Is there a particular app that seems to cause these issues more than others? What model iPhone are you using? Join us in DM.",
]

account_access = [
    "verification code never arrives when i try to sign into my apple id",
    "forgot my apple id password and the reset link isnt coming through",
    "account got locked after too many login attempts, need help asap",
    "cant sign into icloud on my new phone, keeps saying incorrect password",
    "i need a new code for the app store, havent received any but it says too many sent",
    "someone changed my apple id password and i didnt do it",
    "two factor authentication code isnt showing up on my other device",
    "app store keeps asking me to sign in again and again",
    "my apple id got disabled and i dont know why",
    "cant reset my password, the email link keeps expiring",
]
account_access_replies = [
    "We'd like to provide some assistance with this. Tell us more about the issue you're experiencing in DM. We'll go from there.",
    "Sorry about that! Please DM us your email associated with the Apple ID so we can look into this.",
    "That sounds frustrating, let's get this sorted. Send us a DM with more details so we can help.",
    "We can help you get back in. Please DM us so we can walk through account recovery steps.",
    "Let's fix this together. DM us with when this started and we'll go from there.",
]

billing = [
    "got charged for an app subscription i already cancelled months ago",
    "app store charged me twice for the same purchase this week",
    "i want a refund for an app that doesnt work as advertised",
    "icloud storage charge showed up but i never upgraded my plan",
    "apple music billed me after i cancelled my subscription",
    "why was i charged for an in app purchase i never made",
    "my kid bought something in an app without permission, need a refund",
    "subscription renewed even though i turned off auto renew",
    "charged for a free trial that was supposed to be free",
    "app store bill is higher than what i actually purchased",
]
billing_replies = [
    "Sorry to hear about the unexpected charge. Please DM us your Apple ID email so we can look into this together.",
    "We understand the frustration. Send us a DM with the order details or receipt so we can help.",
    "Let's take a look at that charge. Please DM us the date and amount so we can investigate.",
    "We'd like to help with this. DM us your Apple ID email and we'll check the billing history.",
    "That doesn't look right, let's fix it. Please DM us so we can review the transaction.",
]

hardware = [
    "screen cracked after i dropped my phone, whats the repair cost",
    "phone wont turn on at all after it got wet",
    "home button completely stopped working out of nowhere",
    "battery is swelling and pushing the screen up, is this dangerous",
    "camera lens shattered, can this be repaired",
    "charging port seems damaged, phone wont charge with any cable",
    "speaker stopped working after i dropped the phone",
    "screen has dead pixels since yesterday, never dropped it",
    "phone gets extremely hot and shuts off randomly",
    "back glass is cracked, do you replace just that",
]
hardware_replies = [
    "Sorry to hear that! Please DM us your device model and we can go over repair options.",
    "We can help with that. DM us your device model so we can check service options near you.",
    "Let's find the best fix for this. Please DM us with your device model and what happened.",
    "That sounds concerning, let's look into it. Please DM us your device model right away.",
    "We're here to help. Please DM us with more detail on the device and issue.",
]

howto = [
    "how do i transfer my photos to my new phone",
    "how do i turn off notifications for one specific app",
    "how do i free up storage space on my phone",
    "how do i set up face id on my new phone",
    "how do i find my phone if i lost it",
    "how do i turn on dark mode",
    "how do i backup my phone before i sell it",
    "how do i share my location with a family member",
    "how do i change my apple id email address",
    "how do i restore from an icloud backup",
]
howto_replies = [
    "Happy to help with that! Please DM us and we'll walk you through the steps.",
    "Sure thing, please DM us your device model and iOS version so we can guide you.",
    "We can help you set that up. DM us and we'll get you the right steps.",
    "Great question! Send us a DM and we'll walk you through it.",
    "Let's get that set up for you. Please DM us so we can help step by step.",
]

general = [
    "your customer service is honestly amazing, thank you for the quick help",
    "been on hold forever, nobody is answering my messages",
    "just wanted to say i love my new phone, best purchase ever",
    "so disappointed with the support ive gotten this week",
    "does anyone actually check these messages",
    "shoutout to the genius bar team for fixing my phone so fast",
    "worst experience ive had with any tech company honestly",
    "thanks for finally getting back to me after days of waiting",
    "just have a general question about my warranty coverage",
    "your app is so buggy lately it barely works",
]
general_replies = [
    "Thank you for the kind words, we'll pass that along to the team!",
    "We're sorry to hear that and appreciate you flagging it. Please DM us so we can make this right.",
    "Glad we could help! Let us know if anything else comes up.",
    "We hear you and we're sorry for the delay. DM us your account details so we can help directly.",
    "Sorry for the trouble, we're here now. Please DM us with more details so we can assist.",
]

buckets = [
    ("software_update_device_issue", software_update, software_update_replies),
    ("apple_id_account_access", account_access, account_access_replies),
    ("billing_subscription_dispute", billing, billing_replies),
    ("hardware_physical_damage", hardware, hardware_replies),
    ("how_to_question", howto, howto_replies),
    ("general_complaint_or_praise", general, general_replies),
]

rows = []
tweet_id = 200000
for intent, msgs, replies in buckets:
    for i in range(30):
        name = random.choice(names)
        base = random.choice(msgs)
        reply = random.choice(replies)
        prefix = random.choice(["@AppleSupport ", "@AppleSupport hey, ", "@AppleSupport "])
        suffix = random.choice(["", " smh", " !!", " ...", " pls help", " 😡", " 🙄", ""])
        customer_msg = f"{prefix}{base}{suffix}"
        rows.append({
            "tweet_id": tweet_id,
            "author": f"user_{name}_{tweet_id}",
            "text": customer_msg,
            "intent": intent,
            "agent_reply": f"@user_{name}_{tweet_id} {reply}",
            "source": "synthetic",
        })
        tweet_id += 1

random.shuffle(rows)

with open("data/apple_synthetic_corpus.csv", "w", newline="", encoding="utf-8") as f:
    fieldnames = ["tweet_id", "author", "text", "intent", "agent_reply", "source"]
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print(f"wrote {len(rows)} synthetic rows")
