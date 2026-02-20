import time
from scam_detector import analyze_message

fake_inbox = [
    "Hey Fridaous, are you coming to school?",
    "URGENT! You won a free iPhone! Click here now!",
    "Your bank account is locked. Verify your password.",
    "Wanna play Roblox later?"
]

print("📱 Teen Scam Detector Running...\n")

for msg in fake_inbox:
    time.sleep(2)  # wait 2 seconds like real messages
    print("\n📩 New Message:", msg)

    risk, score, reasons = analyze_message(msg)
    print("🚨 Scan Result:", risk)

    for r in reasons:
        print(" -", r)
