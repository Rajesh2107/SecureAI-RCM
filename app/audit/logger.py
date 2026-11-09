
import json
import logging
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

AUDIT_FILE = Path("logs/security_audit.jsonl")

logger = logging.getLogger("secureai.audit")


def write_audit_event(
    claim_id: str,
    security_allowed: bool,
    phi_detected: bool,
    denial_validation_status: str,
    groundedness_status: str,
    response_quality_status: str,
    human_review_required: bool = True,
) -> dict:
    event = {
        "event_id": str(uuid4()),
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "claim_id": claim_id,
        "security_allowed": security_allowed,
        "phi_detected": phi_detected,
        "denial_validation_status": denial_validation_status,
        "groundedness_status": groundedness_status,
        "response_quality_status": response_quality_status,
        "human_review_required": human_review_required,
    }

    try:
        AUDIT_FILE.parent.mkdir(parents=True, exist_ok=True)

        with AUDIT_FILE.open("a", encoding="utf-8") as file:
            file.write(json.dumps(event) + "\n")

    except OSError:
        logger.exception("Security audit event could not be written")
        raise

    return event
