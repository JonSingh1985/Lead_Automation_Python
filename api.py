import requests
import logging

def get_user_data():
    try:
        url = "https://jsonplaceholder.typicode.com/users/1"

        response = requests.get(url)

        response.raise_for_status()

        data = response.json()

        #Extracting reevant fields
        extracted_data = {
            "name": data.get("name"),
            "email": data.get("email"),
            "company": data.get("company", {}).get("name"),
            "city": data.get("address", {}).get("city")
        }

        logging.info("sccessfully fetched and extracted relevant fields")

        return extracted_data
    
    except requests.exceptions.RequestException as e:
        logging.error(f"API request failed: {e}")
        return None