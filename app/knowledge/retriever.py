
import json
from pathlib import Path

KNOWLEDGE_FILE = Path("app/knowledge/denial_codes.json")


def retrieve_denial_reference(denial_code: str) -> dict:
    """Retrieve a trusted denial-code reference from the local knowledge base."""

    if not KNOWLEDGE_FILE.exists():
        raise FileNotFoundError(
            f"Knowledge base not found: {KNOWLEDGE_FILE}"
        )

    with KNOWLEDGE_FILE.open("r", encoding="utf-8") as file:
        knowledge = json.load(file)

    code = denial_code.strip().upper()

    if code not in knowledge:
        return {
            "found": False,
            "denial_code": code,
            "reference": None
        }

    return {
        "found": True,
        "denial_code": code,
        "reference": knowledge[code]
    }
