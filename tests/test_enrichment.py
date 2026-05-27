import pytest
from src.lead_automation.services.enrichment_client import EnrichmentClient
from unittest.mock import AsyncMock, patch

@pytest.fixture
def client():
    return EnrichmentClient()

@patch("src.lead_automation.services.enrichment_client.EnrichmentClient.analyze_lead_with_ai")
def test_ai_enrichment(mock_ai, client):
    # Fake API response
    mock_ai.return_value = '{"score": "Hot", "reason": "Test lead"}'

    # Sample input
    row = {
        "name": "John",
        "email": "john@test.com",
        "phone": "123456",
    }

    # Call method
    result = client.analyze_lead_with_ai(row)

    assert result is not None

@patch("src.lead_automation.services.enrichment_client.EnrichmentClient.analyze_lead_with_ai_async", new_callable=AsyncMock)
@pytest.mark.asyncio
async def test_async_ai(mock_ai, client):
    mock_ai.return_value = '{"score": "Hot", "reason": "Async test"}'
    row = {
        "name": "John",
        "email": "john@test.com",
        "phone": "123"
    }

    result = await client.analyze_lead_with_ai_async(row)

    assert result is not None






























# def test_create_lookup():
#     client = EnrichmentClient()

#     users = [
#         {"email": "a@test.com"},
#         {"email": "b@test.com"}
#     ]

#     lookup = client.create_lookup(users)

#     assert "a@test.com" in lookup
#     assert "b@test.com" in lookup


# def test_parse_ai_response():
#     client = EnrichmentClient()

#     ai_text = '{"score": "Hot", "reason": "Business email"}'

#     result = client.parse_ai_response(ai_text)
#     assert result["score"] == "Hot"
#     assert result["reason"] == "Business email"

# def test_parse_ai_response_invalid():
#     client = EnrichmentClient()

#     ai_notjson = "This is not JSON"

#     result = client.parse_ai_response(ai_notjson)

#     assert result["score"] is None
#     assert result["reason"] is None