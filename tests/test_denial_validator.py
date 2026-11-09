
from app.validation.denial_validator import validate_denial_explanation


def test_co50_correct_explanation():
    result = validate_denial_explanation(
        "CO-50",
        "The payer denied this service because it was not medically necessary."
    )
    assert result["valid"] is True


def test_co50_unrelated_explanation():
    result = validate_denial_explanation(
        "CO-50",
        "This is a graphics card hardware failure."
    )
    assert result["valid"] is False


def test_unknown_denial_code():
    result = validate_denial_explanation(
        "CO-999",
        "Some explanation."
    )
    assert result["validation_status"] == "UNKNOWN_CODE"
