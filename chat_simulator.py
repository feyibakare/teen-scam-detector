from scam_detector import analyze_message

fake_messages = [
    "Hey, are you coming to school today?",
    "URGENT! You won a free iPhone! Click here now!",
    "Your bank account is locked. Verify your password.",
    "Wanna play Roblox later?"
]

for msg in fake_messages:
    print("\n📩 New Message:", msg)
    risk, score, reasons = analyze_message(msg)

    print("⚠️ Scan Result:", risk)
    for r in reasons:
        print("  -", r)
