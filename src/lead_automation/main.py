import csv
import logging
import asyncio
# from src.lead_automation.utils.utils import clean_email, clean_phone, remove_duplicates
# from api import get_user_data, fetch_all_users
from src.lead_automation.services.lead_cleaner import LeadCleaner
from src.lead_automation.services.enrichment_client import EnrichmentClient
import time



         


#loging configuration
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def main():
    try:
        logging.info("Starting data cleaning process.")

    # Read file
        with open("data/leads.csv", "r") as file:
            reader = csv.DictReader(file)
            cleaner = LeadCleaner()
            
            try:
                     cleaned_data =[
                        {
                            "name": row["name"].strip(),
                            "email": cleaner.clean_email(row["email"]),
                            "phone": cleaner.clean_phone(row["phone"])
                       }
                       for row in reader
                    ]


            except KeyError as e:
                logging.warning(f"missing column in row: {e}")
            except Exception as e:
                logging.error(f"Error processing row: {e}")

        logging.info("Finished cleaning data.")

        # Remove duplecates
        unique_data = cleaner.remove_duplicates(cleaned_data)
        logging.info(f"Removed duplicates, Final count: {len(unique_data)}")

        # API data enrichment






        # fetch API data once
        client = EnrichmentClient()
        users = client.fetch_all_users()

        # Look up dictionary
        lookup = client.create_lookup(users)
        
        logging.info("Starting async enrichment process...")

        start_time = time.time()

        enriched_data = asyncio.run(
             client.process_lead_acync(unique_data, lookup)
        )

        end_time = time.time()

        logging.info(f"Async enrichment completed: {end_time - start_time:.2f} seconds.")

        # logging.info("Starting sync enrichment process...")

        # start_time = time.time()

        # sync_data = client.process_leads_sync(unique_data, lookup)

        # end_time = time.time()

        # logging.info(f"Sync processing time: {end_time - start_time:.2f} seconds")




        # Write output 
        with open("output/cleaned_leads.csv", "w", newline="") as file:
            fieldnames = ["name", "email", "phone", "company", "city", "lead_score", "reason"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)

            writer.writeheader()
            writer.writerows(enriched_data)

            # print("Enriched data: ", enriched_data)

        logging.info("Successfully wrote cleaned data to output file.")

    except FileNotFoundError:
        logging.error("Input file not found. Check file path.")
    except Exception as e:
        logging.critical(f"Unexpected error: {e}")




if __name__ == "__main__":
    main()

# API data fetching and extraction -----

# data = get_user_data()

# api_data = get_user_data()

# if api_data:
#     print("API Data: ", api_data)