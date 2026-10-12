import re
from dataclasses import dataclass, field

KEYWORDS = [
    "free", "urgent", "winner", "you won", "claim now", "limited time",
    "click here", "password", "verify", "bank", "gift card", "pay immediately", "you owe", 
        "unless you", "account will be deleted", "account will be suspended", "account has been locked", 
        "new number", "lost my phone", "it's mom", "it's dad", "send money", "e-transfer"
]
SHORTENERS = ["bit.ly", "tinyurl.com", "t.co", "goo.gl"]

HIGH = "high"
POSSIBLE = "possible"
SAFE = "safe"

LABELS = {
    HIGH: "⚠️ HIGH RISK SCAM",
    POSSIBLE: "⚠️ POSSIBLE SCAM",
    SAFE: "✅ Likely Safe",
}

EXPLANATIONS = {
    "free": "Scammers use free prizes to trick teens into clicking links.",
    "urgent": "Urgency makes people panic and stop thinking carefully.",
    "winner": "You can't win a contest you never entered.",
    "you won": "You can't win a contest you never entered.",
    "claim now": "Pressure to act immediately is a classic scam tactic.",
    "limited time": "Fake deadlines stop you from checking if it's real.",
    "click here": "Scam links often steal passwords or install malware.",
    "password": "Real companies NEVER ask for passwords in messages.",
    "verify": "Fake 'verify your account' messages are a common way to steal logins.",
    "bank": "Fake bank messages try to steal your money.",
    "gift card": "Scammers ask for gift cards because they're hard to trace.",
    "pay immediately": "Scammers pressure you to send money quickly so you don't have time to check if the request is real.", 
    "you owe": "Scammers may claim you owe money to frighten you into making a payment without verifying the debt.",
    "unless you": "Scammers often use threats or consequences to pressure you into taking action without thinking carefully.",
    "account will be deleted": "Scammers may threaten to delete your account to trick you into sharing personal information or clicking suspicious links.",
    "account will be suspended": "Fake account suspension warnings create fear and pressure you to reveal login details or visit fraudulent websites.",
    "account has been locked": "Scammers may pretend your account is locked to trick you into entering your password on a fake login page.", 
    "new number": "Scammers may pretend to be someone you know and claim they have a new phone number to gain your trust.",
    "lost my phone": "Scammers sometimes pretend they've lost their phone to explain why they're contacting you from an unfamiliar number.",
    "it's mom": "Scammers may impersonate your mother to gain your trust and trick you into sending money or sharing personal information.",
    "it's dad": "Scammers may impersonate your father to create a false sense of trust and pressure you into helping them.", 
    "send money": "Scammers may ask you to send money urgently, often using fake emergencies to stop you from verifying their identity.",
    "e-transfer": "Scammers may request an e-transfer because money sent this way can be difficult to recover after a scam."
}


@dataclass
class ScanResult:
    level: str
    score: int
    keywords: list = field(default_factory=list)
    links: list = field(default_factory=list)
    uses_shortener: bool = False

    @property
    def label(self):
        return LABELS[self.level]

    @property
    def reasons(self):
        out = [f"Contains suspicious keyword: '{k}'" for k in self.keywords]
        if self.links:
            out.append("Contains a link")
        if self.uses_shortener:
            out.append("Link uses a URL shortener that hides where it goes")
        return out


def contains_word(text, word):
    return re.search(rf"\b{re.escape(word)}\b", text) is not None


def find_links(text):
    return re.findall(r"(?:https?://|www\.)\S+", text)


def analyze_message(msg):
    text = msg.lower()
    keywords = [w for w in KEYWORDS if contains_word(text, w)]
    links = find_links(text)
    uses_shortener = any(s in link for link in links for s in SHORTENERS)

    score = len(keywords)
    if links:
        score += 1
    if uses_shortener:
        score += 2

    if score >= 3:
        level = HIGH
    elif score >= 2:
        level = POSSIBLE
    else:
        level = SAFE

    return ScanResult(level, score, keywords, links, uses_shortener)


def explain(result):
    return [EXPLANATIONS[k] for k in result.keywords if k in EXPLANATIONS]
