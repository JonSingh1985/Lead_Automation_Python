from src.lead_automation.utils.utils import clean_email, clean_phone, remove_duplicates

def test_clean_email():
    assert clean_email(" TEST@EMAIL.COM ") == "test@email.com"

def test_clean_phone():
    assert clean_phone("+91 98765-43210") == "919876543210"

def test_remove_duplicates():
    data = [
        {"email": "a@test.com", "phone": "123"},
        {"email": "b@test.com", "phone": "456"},
        {"email": "a@test.com", "phone": "123"},
    ]

    result = remove_duplicates(data)

    assert len(result) == 2