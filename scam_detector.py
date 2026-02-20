scam_keywords = [
    "free", "urgent", "winner", "claim now", "limited time",
    "click here", "password", "verify", "bank", "gift card"
]

def analyze_message(msg):
    msg = msg.lower()
    score = 0
    reasons = []

    for word in scam_keywords:
        if word in msg:
            score += 1
            reasons.append(f"Contains suspicious keyword: '{word}'")

    if "http" in msg or "www" in msg:
        score += 2
        reasons.append("Contains a link (common scam sign)")

    if score >= 4:
        risk = "⚠️ HIGH RISK SCAM"
    elif score >= 2:
        risk = "⚠️ POSSIBLE SCAM"
    else:
        risk = "✅ Likely Safe"

    return risk, score, reasons

def explain_scam(reasons):
    explanations = {
        "free": "Scammers use free prizes to trick teens into clicking links.",
        "urgent": "Urgency makes people panic and stop thinking carefully.",
        "click here": "Scam links often steal passwords or install malware.",
        "bank": "Fake bank messages try to steal your money.",
        "password": "Real companies NEVER ask for passwords in messages."
    }

    text = "Explanation for teens:\n"
    for r in reasons:
        for key in explanations:
            if key in r:
                text += "- " + explanations[key] + "\n"
    return text


if __name__ == "__main__":
    msg = input("Paste a message or link: ")
    risk, score, reasons = analyze_message(msg)

    print("\nResult:", risk)
    print("Risk Score:", score)
    for r in reasons:
        print("-", r)
