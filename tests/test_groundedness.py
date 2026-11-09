
from app.validation.groundedness import check_groundedness


def test_normal_explanation():
    result = check_groundedness(
        "The service was not medically necessary under payer rules.",
        "Non-covered services because this is not deemed a medical necessity."
    )

    assert result["groundedness_status"] == "HEURISTIC_PASS"


def test_specific_authorization_number_flagged():
    result = check_groundedness(
        "Authorization number: ABC123456 was approved.",
        "Authorization absent."
    )

    assert result["groundedness_status"] == "REVIEW_REQUIRED"
    assert "authorization_number" in result["suspicious_patterns"]


def test_date_flagged():
    result = check_groundedness(
        "The claim was approved on 05/10/2024.",
        "Non-covered service."
    )

    assert result["groundedness_status"] == "REVIEW_REQUIRED"
    assert "specific_date" in result["suspicious_patterns"]
