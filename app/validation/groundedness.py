
import re


SUSPICIOUS_PATTERNS = {
    "specific_date": r"\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b",
    "authorization_number": r"\b(?:auth(?:orization)?|approval)\s*(?:number|#|no\.?)\s*[:#]?\s*[A-Z0-9-]{5,}\b",
    "specific_policy_claim": r"\b(?:always|required by law|guaranteed|must approve)\b",
}


def check_groundedness(
    explanation: str,
    reference_description: str
) -> dict:
    """
    Heuristic groundedness check.
    This detects selected suspicious patterns, not all hallucinations.
    """

    findings = []

    for category, pattern in SUSPICIOUS_PATTERNS.items():
        if re.search(pattern, explanation, re.IGNORECASE):
            findings.append(category)

    reference_terms = {
        term.lower()
        for term in re.findall(r"\b[a-zA-Z]{5,}\b", reference_description)
    }

    explanation_terms = {
        term.lower()
        for term in re.findall(r"\b[a-zA-Z]{5,}\b", explanation)
    }

    matched_reference_terms = sorted(
        reference_terms.intersection(explanation_terms)
    )

    suspicious = len(findings) > 0

    return {
        "groundedness_status": (
            "REVIEW_REQUIRED" if suspicious else "HEURISTIC_PASS"
        ),
        "suspicious_patterns": findings,
        "matched_reference_terms": matched_reference_terms,
        "human_review_required": True,
        "limitations": (
            "Heuristic checks cannot prove factual accuracy "
            "or detect every hallucination."
        )
    }
