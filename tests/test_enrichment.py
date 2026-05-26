from src.lead_automation.services.enrichment_client import EnrichmentClient

def test_create_lookup():
    client = EnrichmentClient()

    users = [
        {"email": "a@test.com"},
        {"email": "b@test.com"}
    ]

    lookup = client.create_lookup(users)

    assert "a@test.com" in lookup
    assert "b@test.com" in lookup


def test_parse_ai_response():
    client = EnrichmentClient()

    ai_text = '{"score": "Hot", "reason": "Business email"}'

    result = client.parse_ai_response(ai_text)
    assert result["score"] == "Hot"
    assert result["reason"] == "Business email"

def test_parse_ai_response_invalid():
    client = EnrichmentClient()

    ai_notjson = "This is not JSON"

    result = client.parse_ai_response(ai_notjson)

    assert result["score"] is None
    assert result["reason"] is None