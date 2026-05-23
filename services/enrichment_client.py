import requests
import logging
import time



class EnrichmentClient:
    
    def __init__(self, retries=3, delay=2):
        self.retries = retries
        self.delay = delay
        self.base_url = "https://jsonplaceholder.typicode.com/users"

    def fetch_all_users(self):

        for attempt in range(self.retries):
            try:
                logging.info(F"API attemp: {attempt + 1}")

                response = requests.get(self.base_url, timeout=5)
                response.raise_for_status()

                users = response.json()

                logging.info(f"Fetched {len(users)} users from API.")
                return users
            
            except requests.exceptions.RequestException as e:
                logging.warning(f"Attept {attempt + 1} failed: {e}")

                if attempt < self.retries - 1:
                    logging.info(f" Retrying in {self.delay} seconds...")
                    time.sleep(self.delay)
                else:
                    logging.error("All API attempts failed.")
                    return []
                
    def create_lookup(self, users):
        return {
            user.get("email", "").lower(): user
            for user in users
        }
    
    def enrich_lead(sefl, row, user_lookup):

        email = row["email"].lower()

        user = user_lookup.get(email)

        if user:
            return {
                **row,
                "company": user.get("company", {}).get("name"),
                "city": user.get("address", {}).get("city")
            }
        else:
            return {
                **row,
                "company": None,
                "city": None
            }
