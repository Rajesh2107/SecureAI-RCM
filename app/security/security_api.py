
from fastapi import APIRouter
from pydantic import BaseModel

from app.security.prompt_guard import detect_prompt_injection
from app.security.phi_detector import detect_phi, mask_phi

router = APIRouter()


class PromptCheckRequest(BaseModel):
    text: str


class PHICheckRequest(BaseModel):
    text: str


@router.post("/security/prompt-check")
def prompt_check(request: PromptCheckRequest):
    result = detect_prompt_injection(request.text)

    return {
        "input": request.text,
        "blocked": result["blocked"],
        "reason": result["reason"],
        "security_control": "Prompt Injection Detection"
    }


@router.post("/security/phi-check")
def phi_check(request: PHICheckRequest):
    result = detect_phi(request.text)

    return {
        "contains_phi": result["contains_phi"],
        "findings": result["findings"],
        "security_control": "PHI Detection"
    }


@router.post("/security/phi-mask")
def phi_mask(request: PHICheckRequest):
    masked_text = mask_phi(request.text)

    return {
        "original_text": request.text,
        "masked_text": masked_text,
        "security_control": "PHI Masking"
    }
