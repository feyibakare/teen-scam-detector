import re
from dataclasses import dataclass, field

KEYWORDS = [
    "free", "urgent", "winner", "you won", "claim now", "limited time",
    "click here", "password", "verify", "bank", "gift card"
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
