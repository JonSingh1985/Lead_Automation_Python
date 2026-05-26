import logging

class LeadCleaner:
    def clean_email(self, email):
        try:
            return email.strip().lower()
        except Exception as e:
            logging.error(f"Error cleaning email: {e}")
            return None
        
    def clean_phone(self, phone):
        try:
            return "".join(filter(str.isdigit, phone))
        except Exception as e:
            logging.error(f"Error cleaning phone: {e}")
            return None
        
    def remove_duplicates(self, data):
        
        seen = set()
        unique_data = []

        for row in data:
            identifier = (row["email"], row["phone"])

            if identifier not in seen:
                seen.add(identifier)
                unique_data.append(row)

        return unique_data


