
import re

INJECTION_PATTERNS = [
    r"ignore\s+(all\s+)?previous\s+instructions",
    r"ignore\s+(all\s+)?system\s+instructions",
    r"reveal\s+(the\s+)?system\s+prompt",
    r"show\s+(me\s+)?(all\s+)?patient\s+data",
    r"bypass\s+(security|safety|restrictions)",
    r"override\s+(all\s+)?security",
    r"act\s+as\s+an?\s+unrestricted",
]


def detect_prompt_injection(text: str) -> dict:
    if not text:
        return {"blocked": False, "reason": None}

    for pattern in INJECTION_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            return {
                "blocked": True,
                "reason": "Potential prompt injection detected",
            }

    return {"blocked": False, "reason": None}
