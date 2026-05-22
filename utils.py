def clean_email(email):
    return email.strip().lower()

def clean_phone(phone):
    return ''.join(filter(str.isdigit, phone))


def remove_duplicates(data):

    unique_data = []
    seen = set()

    for row in data:
        identifier = (row["email"], row["phone"])

        if identifier not in seen:
            seen.add(identifier)
            unique_data.append(row)

    return unique_data