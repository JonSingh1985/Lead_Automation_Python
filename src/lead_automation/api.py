import requests
import logging
import time




def fetch_all_users(retries=3, delay=2):
    
    url = "https://jsonplaceholder.typicode.com/users"

    for attempt in range(retries):
        try:

            logging.info(f"API attempt {attempt + 1}")
        
            response = requests.get(url, timeout=5)
            response.raise_for_status()

            users = response.json()

            logging.info(f"Fetched {len(users)} users fron API.")

            return users
    
        except requests.exceptions.RequestException as e:
            logging.warning(f"Attempt {attempt + 1} failed: {e}")

            if attempt < retries - 1:
                logging.info(f"retring in {delay} seconds...")
                time.sleep(delay)

            else:
                logging.error("All API attemps failed.")
                return []

















def get_user_data(email):
    try:
        # Simulating API call to fetch user data based on email
        url = "https://jsonplaceholder.typicode.com/users"

        response = requests.get(url, timeout = 5)

        response.raise_for_status()

        users = response.json()

        # logging.info(f"User data: ", users)

        # Find matching user by email
        for user in users:
            if user.get("email","").lower() == email.lower():
                extracted_data = {
                    "company": user.get("company", {}).get("name"),
                    "city": user.get("address", {}).get("city")
                }

                logging.info(f"Match found for email: {email}")
                return extracted_data

        logging.warning(f"no match found for email: {email}")
        return None
    
    except requests.exceptions.RequestException as e:
        logging.error(f"API request failed: {e}")
        return None
    
