import csv
import logging
import asyncio
import time
import typer
# from src.lead_automation.utils.utils import clean_email, clean_phone, remove_duplicates
# from api import get_user_data, fetch_all_users
from src.lead_automation.services.lead_cleaner import LeadCleaner
from src.lead_automation.services.enrichment_client import EnrichmentClient
from src.lead_automation.utils.validation import validate_row



app = typer.Typer()         


#loging configuration
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

#HELPER FUNCTION 

def normalize_row(row, cleaner):
    return {
        "name": row["name"].strip(),
        "email": cleaner.clean_email(row["email"]),
        "phone": cleaner.clean_phone(row["phone"])
    }

# COMMAND 1 — CLEAN LEADS

@app.command()

def clean_leads(input_file: str, output_file: str = "output/cleaned_leads.csv"):
    """
    clean CSV leads (email, phone, remove duplicates)
    """

    try:
        logging.info("Starting data cleaning process.")

        cleaner = LeadCleaner()
        cleaned_data = []

    # Read file
        with open(input_file, "r") as file:
            reader = csv.DictReader(file)
            
            for row in reader:
            
                try:
                    validate_row(row)

                    cleaned_data.append(
                        normalize_row(row, cleaner)
                    )


                except ValueError as e:
                    logging.warning(f"Skipping invalid row: {e}")

        logging.info("Finished cleaning data.")

        # Remove duplecates
        unique_data = cleaner.remove_duplicates(cleaned_data)
        logging.info(f"Removed duplicates, Final count: {len(unique_data)}")

        # Write output 
        with open(output_file, "w", newline="") as file:
            fieldnames = ["name", "email", "phone"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)

            writer.writeheader()
            writer.writerows(unique_data)

            # print("Enriched data: ", enriched_data)

        logging.info(f"Successfully wrote cleaned data to output file:{output_file} ")
    
    except Exception as e:
        logging.error(f"Error in clean_leads: {e}")

        
        
    # COMMAND 2 — ENRICH LEADS
    #  API data enrichment
@app.command()
def enrich_leads(input_file: str, output_file: str = "output/enriched_leads.csv"):
    """
    Enrich lead using API + AI
    """
    try:
        logging.info("Starting enrichment process...")

        # fetch API data once
        cleaner = LeadCleaner()
        client = EnrichmentClient()
        cleaned_data = []
       

        # Read file
        with open(input_file, "r") as file:
            reader = csv.DictReader(file)

            for row in reader:
                try:
                    validate_row(row)

                    cleaned_data.append(
                        normalize_row(row, cleaner)
                    )

                except ValueError as e:
                    logging.warning(f"Skipping invalid row: {e}")
          
            
            
        unique_data = cleaner.remove_duplicates(cleaned_data)


        # API Look up dictionary
        users = client.fetch_all_users()
        lookup = client.create_lookup(users)

        # Async enrichment        
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
        with open(output_file, "w", newline="") as file:
            fieldnames = ["name", "email", "phone", "company", "city", "lead_score", "reason"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)

            writer.writeheader()
            writer.writerows(enriched_data)

            # print("Enriched data: ", enriched_data)

        logging.info("Successfully wrote cleaned data to output file.")

    
    except Exception as e:
        logging.critical(f"Error in enrich_lead: {e}")




if __name__ == "__main__":
    app()

