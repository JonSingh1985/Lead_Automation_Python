import requests
import logging
import time
import os
import json
import httpx
import asyncio
from dotenv import load_dotenv

load_dotenv()


class EnrichmentClient:
    
    def __init__(self, retries=3, delay=2):
        self.retries = retries
        self.delay = delay
        self.base_url = "https://jsonplaceholder.typicode.com/users"
        self.cache = {}   
        self.cache_lock = asyncio.Lock()

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

    def parse_ai_response(self, ai_text):
        try:
            # String -> Dict
            parsed = json.loads(ai_text)

            score = parsed.get("score")
            reason = parsed.get("reason")

            return {
                "score": score,
                "reason": reason
            }
        except json.JSONDecodeError:
            logging.error(f"Failed to parse AI response: (invaied JSON)")
            return {
                "score": None,
                "reason": None
            }

        except Exception as e:
            logging.error(f"Unexpected error parsing AI response: {e}")
            return {
                "score": None,
                "reason": None
            }

    async def analyze_lead_with_ai_async(self, row):

        try:
            url = "https://openrouter.ai/api/v1/chat/completions"

            api_key = os.getenv("OPENROUTER_API_KEY")

            headers = {
                "authorization": f"Bearer {api_key}",
                "content": "application/json"
            }

            prompt = f"""
            Classify this lead:

            Name: {row['name']}
            Email: {row['email']}

            Return ONLY JSON like:
            {{
              "score": "Hot or Cold",
              "reason": "short explanation"
            }}
            """

            payload = {
                "model": "openai/gpt-3.5-turbo",
                "messages": [
                    {"role": "user", "content": prompt}
                ]
            }

            async with httpx.AsyncClient(timeout=10) as client:
                response = await client.post(url=url, headers=headers, json=payload)

                response.raise_for_status()
                result = response.json()

                content = result["choices"][0]["message"]["content"]

                return content
        except Exception as e:
            logging.error(f"Async AI call failed: {e}")
            return None
        
    
           #---------------------------------------------------------------------------------

        # Async data enrichment

    async def process_lead_acync(self, rows, lookup):
            
            semaphore = asyncio.Semaphore(2) # Limit to 2 concurrent AI calls

            enriched_rows = []
            tasks = []

            for row in rows:
                enriched_row = self.enrich_lead(row, lookup)
                enriched_rows.append(enriched_row)

                task = self._safe_ai_call(enriched_row, semaphore)
                tasks.append(task)

            results = await asyncio.gather(*tasks)

            # print(enriched_row, results)

            final_data = []

            for enriched_row, ai_text in zip(enriched_rows, results):
                ai_data = self.parse_ai_response(ai_text) if ai_text else {
                    "Score": None,
                    "reason": None
                }

                final_row = {
                    **enriched_row,
                    "lead_score": ai_data["score"],
                    "reason": ai_data["reason"]
                }

                # print(final_row)

                final_data.append(final_row)

            return final_data
    
    async def _safe_ai_call(self, row, semaphore):
        email = row.get("email")

        print(f"{self.cache} - email: {email}")



        async with semaphore:

            # Cache lock for checking
            async with self.cache_lock:

            # Check chache first

                if email in self.cache:
                    logging.info(f"Cache hit for {email}")
                    return self.cache[email]
                # print(self.cache)
                              
            try:
                result = await self.analyze_lead_with_ai_async(row)

                await asyncio.sleep(0.5) # Small delay to avoid hitting rate limits

                # Lock cache for writing
                async with self.cache_lock:

                # Save in cache
                    self.cache[email] = result
                    print(f"Cache updated for {email}")
                # print(self.cache)
               
                return result
            
            except Exception as e:
                logging.error(F"Safe AI call failed: {e}")
                return None
            
    
    # def process_leads_sync(self, rows, user_lookup):
    #     final_data = []

    #     for row in rows:
    #         enriched_row = self.enrich_lead(row, user_lookup)

    #         result = self.analyze_lead_with_ai(enriched_row)

    #         ai_data = self.parse_ai_response(result) if result else {
    #             "score": None,
    #             "reason": None
    #         }

    #         final_row = {
    #             **enriched_row,
    #             "lead_score": ai_data["score"],
    #             "reason": ai_data["reason"]
    #         }

    #         final_data.append(final_row)

    #     return final_data