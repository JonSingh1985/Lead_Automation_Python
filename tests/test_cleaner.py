import pytest
from src.lead_automation.services.lead_cleaner import LeadCleaner

# def test_clean_email():
#     cleaner = LeadCleaner()

#     result = cleaner.clean_email(" TEsT@email.com")

#     assert result == "test@email.com"

# def test_clean_phone():
#     cleaner = LeadCleaner()

#     result = cleaner.clean_phone("+91 98765-43210")
#     assert result == "919876543210"


# def test_remove_duplicates():
#     cleaner = LeadCleaner()

#     data = [
#         {"email": "a@test.com", "phone": "123"},
#         {"email": "b@test.com", "phone": "456"},
#         {"email": "b@test.com", "phone": "456"}
#     ]

#     result = cleaner.remove_duplicates(data)
#     assert len(result) == 2

@pytest.fixture
def cleaner():
    return LeadCleaner()

@pytest.fixture
def sample_rows():
    return [
        {"name": " Jonh ", "email": " Test@EmAil.com", "phone": "123-456"},
        {"name": "Alice", "email": "alice@rmail.com", "phone": "(987) 654"}
    ]

@pytest.mark.parametrize("input_email, expected", [
    (" Test@EmAil.com ", "test@email.com"),
    ("hello@world.com", "hello@world.com"),
    (" MIXED@Case.com", "mixed@case.com"),
])
def test_clean_email(cleaner, input_email, expected):
    result = cleaner.clean_email(input_email)
    assert result == expected

@pytest.mark.parametrize("input_phone, expected", [
    ("123-456", "123456"),
    ("(987) 654", "987654"),
    ("+91 987-654-3210", "919876543210"),
])
def test_clean_phone(cleaner, input_phone, expected):
    result = cleaner.clean_phone(input_phone)
    assert result == expected

def test_remove_duplicates(cleaner):
    data = [
        {"email": "a@test", "phone": "123"},
        {"email": "b@test", "phone": "456"},
        {"email": "a@test", "phone": "123"},
    ]

    result = cleaner.remove_duplicates(data)
    assert len(result) == 2