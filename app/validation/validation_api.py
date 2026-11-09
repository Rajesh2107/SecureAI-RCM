
from fastapi import APIRouter
from pydantic import BaseModel

from app.validation.denial_validator import validate_denial_explanation

router = APIRouter()


class DenialValidationRequest(BaseModel):
    denial_code: str
    explanation: str


@router.post("/validation/denial")
def validate_denial(request: DenialValidationRequest):
    result = validate_denial_explanation(
        request.denial_code,
        request.explanation
    )

    return {
        "validation_result": result,
        "security_control": "AI Output Validation",
        "human_review_required": True
    }
