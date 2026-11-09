
import re

PHI_PATTERNS = {
    "email": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
    "phone": r"\b(?:\+91[- ]?)?[6-9]\d{9}\b",
    "ssn": r"\b\d{3}-\d{2}-\d{4}\b",
}


def detect_phi(text: str) -> dict:
    findings = []

    if not text:
        return {
            "contains_phi": False,
            "findings": []
        }

    for category, pattern in PHI_PATTERNS.items():
        matches = re.findall(pattern, text)

        if matches:
            findings.append({
                "category": category,
                "count": len(matches)
            })

    return {
        "contains_phi": len(findings) > 0,
        "findings": findings
    }


def mask_phi(text: str) -> str:
    if not text:
        return text

    masked_text = text

    for pattern in PHI_PATTERNS.values():
        masked_text = re.sub(
            pattern,
            "[REDACTED]",
            masked_text
        )

    return masked_text
