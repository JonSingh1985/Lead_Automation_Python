from services.lead_cleaner import LeadCleaner

def test_clean_email():
    cleaner = LeadCleaner()

    result = cleaner.clean_email(" TEsT@email.com")

    assert result == "test@email.com"

def test_clean_phone():
    cleaner = LeadCleaner()

    result = cleaner.clean_phone("+91 98765-43210")
    assert result == "919876543210"


def test_remove_duplicates():
    cleaner = LeadCleaner()

    data = [
        {"email": "a@test.com", "phone": "123"},
        {"email": "b@test.com", "phone": "456"},
        {"email": "b@test.com", "phone": "456"}
    ]

    result = cleaner.remove_duplicates(data)
    assert len(result) == 2