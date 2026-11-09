
from app.knowledge.retriever import retrieve_denial_reference


def test_retrieve_co50_reference():
    result = retrieve_denial_reference("CO-50")

    assert result["found"] is True
    assert result["denial_code"] == "CO-50"
    assert "medical necessity" in (
        result["reference"]["official_description"].lower()
    )


def test_retrieve_unknown_code():
    result = retrieve_denial_reference("CO-999")

    assert result["found"] is False
    assert result["reference"] is None


def test_retrieve_code_case_insensitive():
    result = retrieve_denial_reference("co-50")

    assert result["found"] is True
