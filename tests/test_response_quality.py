
from app.validation.response_quality import validate_response_quality


def test_complete_response():
    text = (
        "The claim was denied because medical necessity was not established. "
        "Review supporting clinical documentation. Human review is required."
    )

    result = validate_response_quality(text)
    assert result["quality_status"] == "QUALITY_CHECK_PASS"


def test_short_response():
    result = validate_response_quality("Denied.")

    assert result["quality_status"] == "REVIEW_REQUIRED"
    assert "RESPONSE_TOO_SHORT" in result["findings"]


def test_missing_human_review():
    result = validate_response_quality(
        "The payer denied the claim because medical necessity was not established."
    )

    assert "HUMAN_REVIEW_MISSING" in result["findings"]


def test_incomplete_response():
    text = (
        "The payer denied the claim because medical necessity was not "
        "established. Human review is required to verify completeness "
        "and accuracy"
    )

    result = validate_response_quality(text)

    assert result["quality_status"] == "REVIEW_REQUIRED"
    assert "POSSIBLY_INCOMPLETE_RESPONSE" in result["findings"]
