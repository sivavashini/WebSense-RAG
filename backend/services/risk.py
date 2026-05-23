import re
from dataclasses import dataclass


CATEGORIES = {
    "Pet Safety": [
        "pet",
        "dog",
        "cat",
        "puppy",
        "kitten",
        "animal",
        "leash",
        "collar",
        "microchip",
        "lost dog",
        "lost cat",
        "missing pet",
    ],
    "Lost & Found": [
        "lost",
        "missing",
        "misplaced",
        "found",
        "wallet",
        "keys",
        "phone",
        "bag",
        "id card",
        "passport",
        "item",
    ],
    "Public Help": [
        "help someone",
        "stranger needs help",
        "directions",
        "public",
        "neighbor",
        "community",
        "welfare check",
    ],
    "Cyber Threat": ["phishing", "malware", "ransomware", "password", "hack", "breach", "link", "account", "otp"],
    "Physical Threat": ["weapon", "gun", "knife", "fight", "attack", "stalking", "break-in", "violence"],
    "Medical Emergency": ["bleeding", "unconscious", "accident", "medical", "poison", "chest pain", "not breathing", "seizure"],
    "Ethical Concern": ["cheat", "lie", "hide", "unfair", "privacy", "consent", "blackmail"],
    "Suspicious Activity": ["suspicious", "unknown person", "following", "strange package", "scam"],
    "Harassment": ["harassment", "abuse", "unwanted", "creepy", "threat messages", "bully", "humiliate", "rumor", "mock", "harass"],
    "Theft": ["steal", "stolen", "robbery", "shoplift", "missing wallet", "fraud"],
}

CRITICAL = ["gun", "knife", "fire", "unconscious", "suicide", "bomb", "explosion", "active shooter"]
HIGH = ["ransomware", "break-in", "stalking", "blackmail", "violence", "bleeding", "threaten"]
MEDIUM = ["phishing", "suspicious", "harass", "bully", "stolen", "privacy", "scam", "missing wallet", "passport"]
LOW_CONTEXT = ["lost dog", "lost cat", "missing pet", "lost pet", "misplaced", "lost keys", "lost phone", "lost bag"]


@dataclass
class RiskResult:
    risk_level: str
    category: str
    confidence: float


def classify_risk(text: str) -> RiskResult:
    lowered = text.lower()
    category_scores = {
        category: sum(1 for word in words if re.search(rf"\b{re.escape(word)}\b", lowered))
        for category, words in CATEGORIES.items()
    }
    category = max(category_scores, key=category_scores.get)
    if category_scores[category] == 0:
        category = "Suspicious Activity"

    if any(term in lowered for term in LOW_CONTEXT) and not any(term in lowered for term in CRITICAL + HIGH):
        level, base = "LOW", 0.7
    elif any(term in lowered for term in CRITICAL):
        level, base = "CRITICAL", 0.92
    elif any(term in lowered for term in HIGH):
        level, base = "HIGH", 0.86
    elif any(term in lowered for term in MEDIUM):
        level, base = "MEDIUM", 0.74
    else:
        level, base = "LOW", 0.58

    confidence = min(0.98, base + category_scores.get(category, 0) * 0.03)
    return RiskResult(level, category, round(confidence, 2))


def actions_for(level: str, category: str) -> list[str]:
    shared = [
        "Pause before acting and avoid escalating the situation.",
        "Preserve relevant evidence such as screenshots, filenames, timestamps, or witness details.",
    ]
    if category == "Pet Safety":
        return [
            "Search nearby calmly, starting from the last known location and familiar routes.",
            "Ask neighbors, security staff, local shelters, and nearby vets if they have seen the pet.",
            "Share a clear photo, name, collar details, and contact number in local groups.",
        ]
    if category == "Lost & Found":
        return [
            "Retrace your last steps and check likely places before assuming theft.",
            "Contact the venue, transit desk, building security, or lost-and-found counter.",
            "For cards or IDs, lock or report them only if they may be misused.",
        ]
    if category == "Public Help":
        return [
            "Offer help from a safe distance and ask what support is needed.",
            "Involve staff, neighbors, or a trusted nearby person if the situation feels unclear.",
            "Avoid sharing personal information or entering isolated places alone.",
        ]
    if level == "CRITICAL":
        return ["Move to immediate safety now.", "Call local emergency services if anyone may be harmed.", *shared]
    if level == "HIGH":
        return ["Contact a trusted authority, security team, guardian, or emergency line if danger is imminent.", *shared]
    if category == "Cyber Threat":
        return ["Do not click links, share OTPs, or install files.", "Change exposed passwords from a trusted device.", *shared]
    return ["Choose the option that protects people first and respects consent, privacy, and law.", *shared]
