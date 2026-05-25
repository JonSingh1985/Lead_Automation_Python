import requests
import logging
import time
import os
from dotenv import load_dotenv

load_dotenv()


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
        
    def analyze_lead_with_ai(self, row):

        

        try:
            url = "https://openrouter.ai/api/v1/chat/completions"

            api_key = os.getenv("OPENROUTER_API_KEY")

            headers = {
                "Authorization": f"Bearer {api_key}",
                "content-type": "application/json",
            }

            

            prompt = f"""
            Classify this lead:
            Name: {row["name"]}
            Email: {row["email"]}
           
            return only JSON like this:
            {{ 
            "score": "Hot or Cold",
            "reason": "Short explanation"
            }}
            """

            payload = {
                "model": "openai/gpt-3.5-turbo",
                "messages": [
                    {"role": "user", "content": prompt}
                ]
            }

            response = requests.post(url, headers=headers, json=payload, timeout=10)
            response.raise_for_status()

            result = response.json()

            content = result["choices"][0]["message"]["content"]

            return content
        
        except Exception as e:
            logging.error(f"AI enrichment failed: {e}")
            return None
