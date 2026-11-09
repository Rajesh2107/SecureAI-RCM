
from fastapi import FastAPI, HTTPException
from pathlib import Path
import json
import subprocess
import sys

from app.ai.assistant import explain_denial
from app.security.security_api import router as security_router
from app.security.security_gateway import inspect_and_sanitize_claim
from app.validation.validation_api import router as validation_router
from app.validation.denial_validator import validate_denial_explanation
from app.validation.groundedness import check_groundedness
from app.validation.response_quality import validate_response_quality
from app.knowledge.retriever import retrieve_denial_reference
from app.audit.logger import write_audit_event

app = FastAPI(
    title="SecureAI-RCM",
    description="Healthcare AI Security & Governance Platform",
    version="0.9.0"
)

# Register API routers
app.include_router(security_router)
app.include_router(validation_router)

# Project paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_FILE = PROJECT_ROOT / "datasets" / "synthetic_claims.json"
SECURITY_SCRIPT = PROJECT_ROOT / "run_security_lab.py"


# -------------------- CLAIM DATA --------------------

def load_claims():
    if not DATA_FILE.exists():
        return []

    return json.loads(DATA_FILE.read_text(encoding="utf-8"))


# -------------------- GENERAL API --------------------

@app.get("/")
def home():
    return {
        "project": "SecureAI-RCM",
        "status": "running",
        "version": "0.9.0"
    }


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.get("/claims")
def get_claims():
    return load_claims()


@app.get("/claims/{claim_id}")
def get_claim(claim_id: str):
    for claim in load_claims():
        if claim["claim_id"] == claim_id:
            return claim

    raise HTTPException(status_code=404, detail="Claim not found")


# -------------------- METRICS --------------------

@app.get("/metrics/summary")
def metrics():
    claims = load_claims()

    total = len(claims)
    denied = sum(c["status"].lower() == "denied" for c in claims)
    approved = sum(c["status"].lower() == "approved" for c in claims)
    pending = sum(c["status"].lower() == "pending" for c in claims)

    return {
        "total_claims": total,
        "denied_claims": denied,
        "approved_claims": approved,
        "pending_claims": pending,
        "denial_rate": round(denied / total * 100, 2) if total else 0
    }


# -------------------- AI DENIAL EXPLANATION --------------------

@app.get("/ai/explain/{claim_id}")
def ai_explain_claim(claim_id: str):
    claims = load_claims()

    for claim in claims:
        if claim["claim_id"] == claim_id:

            if claim["status"].lower() != "denied":
                raise HTTPException(
                    status_code=400,
                    detail="AI denial explanation is available only for denied claims"
                )

            # Security gateway
            security_result = inspect_and_sanitize_claim(claim)

            if not security_result["allowed"]:
                raise HTTPException(
                    status_code=400,
                    detail="Claim blocked by security gateway"
                )

            sanitized_claim = security_result["sanitized_claim"]

            denial_code = claim.get("denial_code", "UNKNOWN")

            # Retrieve trusted denial reference
            retrieved = retrieve_denial_reference(denial_code)

            if not retrieved["found"]:
                raise HTTPException(
                    status_code=400,
                    detail="Denial code missing from trusted knowledge base"
                )

            reference = retrieved["reference"]

            # Generate grounded AI explanation
            explanation = explain_denial(sanitized_claim)

            # Validate denial explanation
            validation_result = validate_denial_explanation(
                denial_code,
                explanation
            )

            # Groundedness validation
            groundedness_result = check_groundedness(
                explanation,
                reference["official_description"]
            )

            # Response quality validation
            response_quality = validate_response_quality(explanation)

            # Security audit event
            audit_event = write_audit_event(
                claim_id=claim_id,
                security_allowed=security_result["allowed"],
                phi_detected=security_result["phi_detected"],
                denial_validation_status=validation_result["validation_status"],
                groundedness_status=groundedness_result["groundedness_status"],
                response_quality_status=response_quality["quality_status"],
                human_review_required=True
            )

            return {
                "claim_id": claim_id,
                "denial_code": denial_code,
                "ai_explanation": explanation,
                "security_gateway": {
                    "allowed": security_result["allowed"],
                    "phi_detected": security_result["phi_detected"],
                    "phi_masking_applied": security_result["phi_detected"]
                },
                "output_validation": validation_result,
                "groundedness_check": groundedness_result,
                "response_quality": response_quality,
                "audit_event_id": audit_event["event_id"],
                "human_review_required": True
            }

    raise HTTPException(status_code=404, detail="Claim not found")


# -------------------- AI SECURITY LAB --------------------

@app.post("/security/run")
def run_security_lab():

    if not SECURITY_SCRIPT.exists():
        raise HTTPException(
            status_code=404,
            detail="Security test runner not found"
        )

    try:
        result = subprocess.run(
            [sys.executable, str(SECURITY_SCRIPT)],
            cwd=str(PROJECT_ROOT),
            capture_output=True,
            text=True,
            timeout=120
        )

        output = (
            result.stdout + "\n" + result.stderr
        ).strip()

        return {
            "success": result.returncode == 0,
            "exit_code": result.returncode,
            "output": output,
            "message": (
                "Security tests completed successfully"
                if result.returncode == 0
                else "Security tests failed"
            )
        }

    except subprocess.TimeoutExpired:
        raise HTTPException(
            status_code=504,
            detail="Security test execution timed out"
        )

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Security test execution error: {str(exc)}"
        )
