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

# ----------------------------
# 🔹 HELPER FUNCTIONS
# ----------------------------

def read_csv(file_path):
    with open(file_path, "r") as file:
        return list(csv.DictReader(file))


def write_csv(file_path, data, fieldnames):
    with open(file_path, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)



def normalize_row(row, cleaner):
    return {
        "name": row["name"].strip(),
        "email": cleaner.clean_email(row["email"]),
        "phone": cleaner.clean_phone(row["phone"])
    }


def process_cleaning(rows, cleaner):
    cleaned = []

    for row in rows:

        try:
            validate_row(row)

            cleaned.append(normalize_row(row, cleaner))

        except ValueError as e:
            logging.warning(f"Skipping invalid row: {e}")

    return cleaner.remove_duplicates(cleaned)

async def process_enrichment(rows, client, lookup):
    return await client.process_lead_async(rows, lookup)

# ----------------------------
#  CLI COMMANDS
# ----------------------------

# COMMAND 1 — CLEAN LEADS

@app.command()

def clean_leads(input_file: str, output_file: str = "output/cleaned_leads.csv"):
    """
    clean CSV leads (email, phone, remove duplicates)
    """

    try:
        logging.info("Starting data cleaning process.")

        cleaner = LeadCleaner()

        rows = read_csv(input_file)
        unique_data = process_cleaning(rows, cleaner)
        # print(f"unique_data is processed: {unique_data}")

        write_csv(output_file, unique_data, ["name", "email", "phone"])


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

        # Step 1 — Clean
        rows = read_csv(input_file)
        unique_data = process_cleaning(rows, cleaner)

        # Step 2 — API lookup
        users = client.fetch_all_users()
        lookup = client.create_lookup(users)

        # Step 3 — Async enrichment
        start_time = time.time()

        enriched_data = asyncio.run(
            process_enrichment(unique_data, client, lookup)
        )

        end_time = time.time()
        logging.info(f"Async enrichment completed: {end_time - start_time:.2f} seconds.")

        # Step 4 — Write output
        write_csv(output_file, enriched_data,  ["name", "email", "phone", "company", "city", "lead_score", "reason"])

        logging.info(f"Successfully wrote cleaned data to output file: {output_file}")

    
    except Exception as e:
        logging.critical(f"Error in enrich_lead: {e}")




if __name__ == "__main__":
    app()

