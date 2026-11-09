
import re


def validate_response_quality(explanation: str) -> dict:
    text = explanation.strip()
    findings = []

    if len(text) < 100:
        findings.append("RESPONSE_TOO_SHORT")

    if "human review" not in text.lower():
        findings.append("HUMAN_REVIEW_MISSING")

    # Detect responses ending without normal sentence punctuation.
    if text and not re.search(r'[.!?]["\']?\s*$', text):
        findings.append("POSSIBLY_INCOMPLETE_RESPONSE")

    # Detect common generation truncation endings.
    incomplete_endings = [
        "and",
        "or",
        "the",
        "to",
        "for",
        "with",
        "as",
        "because",
        "accuracy",
        "completeness",
        "including",
    ]

    last_word = re.sub(r'[^a-zA-Z]', '', text.split()[-1]).lower() if text else ""

    if last_word in incomplete_endings:
        if "POSSIBLY_INCOMPLETE_RESPONSE" not in findings:
            findings.append("POSSIBLY_INCOMPLETE_RESPONSE")

    return {
        "quality_status": (
            "REVIEW_REQUIRED" if findings else "QUALITY_CHECK_PASS"
        ),
        "findings": findings,
        "human_review_required": True,
        "limitations": (
            "Rule-based quality checks do not establish factual correctness."
        )
    }
