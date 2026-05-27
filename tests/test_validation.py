import pytest
from src.lead_automation.utils.validation import validate_row

def test_valid_row():
    row = {
        "name": "jon",
        "email": "a@email.com",
        "phone": "123"
    }

    assert validate_row(row)

def test_missing_email():
    row = {
        "name": "jon",
        "phone": "123"
    }

    with pytest.raises(ValueError):
        validate_row(row)

def test_invalid_email():
    row = {
        "name": "jon",
        "email": "Invlid Email",
        "phone": "123"
    }

    with pytest.raises(ValueError):
        validate_row(row)