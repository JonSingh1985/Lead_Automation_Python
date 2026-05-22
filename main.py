import csv
import logging
from utils import clean_email, clean_phone, remove_duplicates
from api import get_user_data


#loging configuration
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


# def main():
#     try:
#         logging.info("Starting data cleaning process.")

#     # Read file
#         with open("data/leads.csv", "r") as file:
#             reader = csv.DictReader(file)
            
            
#             try:
#                      cleaned_data =[
#                         {
#                             "name": row["name"].strip(),
#                             "email": clean_email(row["email"]),
#                             "phone": clean_phone(row["phone"])
#                        }
#                        for row in reader
#                     ]


#             except KeyError as e:
#                 logging.warning(f"missing column in row: {e}")
#             except Exception as e:
#                 logging.error(f"Error processing row: {e}")

#         logging.info("Finished cleaning data.")

#         # Remove duplecates
#         unique_data = remove_duplicates(cleaned_data)
#         logging.info(f"Removed duplicates, Final count: {len(unique_data)}")

#         # Write output 
#         with open("output/cleaned_leads.csv", "w", newline="") as file:
#             fieldnames = ["name", "email", "phone"]
#             writer = csv.DictWriter(file, fieldnames=fieldnames)

#             writer.writeheader()
#             writer.writerows(unique_data)

#         logging.info("Successfully wrote cleaned data to output file.")

#     except FileNotFoundError:
#         logging.error("Input file not found. Check file path.")
#     except Exception as e:
#         logging.critical(f"Unexpected error: {e}")




# if __name__ == "__main__":
#     main()

# API data fetching and extraction -----

data = get_user_data()

api_data = get_user_data()

if api_data:
    print("API Data: ", api_data)