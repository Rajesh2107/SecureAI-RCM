
import json
import re
from pathlib import Path

KNOWLEDGE_FILE = Path("app/knowledge/denial_codes.json")


def load_denial_codes():
    with KNOWLEDGE_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)


def validate_denial_explanation(
    denial_code: str,
    explanation: str
) -> dict:
    denial_codes = load_denial_codes()

    code = denial_code.upper().strip()
    explanation = explanation.lower()

    if code not in denial_codes:
        return {
            "valid": False,
            "denial_code": code,
            "validation_status": "UNKNOWN_CODE",
            "reason": "Denial code is not present in the knowledge base."
        }

    reference = denial_codes[code]
    keywords = reference["validation_keywords"]

    matched_keywords = [
        keyword for keyword in keywords
        if keyword.lower() in explanation
    ]

    # Basic heuristic: check whether the explanation
    # contains at least one expected reference keyword.
    if matched_keywords:
        status = "REFERENCE_MATCH"
        valid = True
        reason = "Explanation contains reference-related keywords."
    else:
        status = "REVIEW_REQUIRED"
        valid = False
        reason = "Expected reference keywords were not detected."

    return {
        "valid": valid,
        "denial_code": code,
        "validation_status": status,
        "matched_keywords": matched_keywords,
        "expected_keywords": keywords,
        "reference_description": reference["official_description"],
        "reason": reason,
        "human_review_required": True
    }
