import requests
import logging

def get_user_data():
    try:
        url = "https://jsonplaceholder.typicode.com/users/1"

        response = requests.get(url)

        response.raise_for_status()

        data = response.json()

        logging.info("sccessfully fetched user data")

        return data
    
    except requests.exceptions.RequestException as e:
        logging.error(f"API request failed: {e}")
        return None