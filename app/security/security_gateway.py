
import json

from app.security.prompt_guard import detect_prompt_injection
from app.security.phi_detector import detect_phi, mask_phi


def inspect_and_sanitize_claim(claim: dict) -> dict:
    """
    Inspect a claim for prompt injection and PHI.
    Mask detectable PHI before AI processing.
    """

    serialized_claim = json.dumps(claim, ensure_ascii=False)

    injection_result = detect_prompt_injection(serialized_claim)

    if injection_result["blocked"]:
        return {
            "allowed": False,
            "reason": "Potential prompt injection detected",
            "phi_detected": False,
            "sanitized_claim": None
        }

    phi_result = detect_phi(serialized_claim)

    def sanitize_value(value):
        if isinstance(value, str):
            return mask_phi(value)

        if isinstance(value, dict):
            return {
                key: sanitize_value(item)
                for key, item in value.items()
            }

        if isinstance(value, list):
            return [sanitize_value(item) for item in value]

        return value

    sanitized_claim = sanitize_value(claim)

    return {
        "allowed": True,
        "reason": None,
        "phi_detected": phi_result["contains_phi"],
        "sanitized_claim": sanitized_claim
    }
