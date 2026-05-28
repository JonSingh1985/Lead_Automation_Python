import asyncio

from fastapi import APIRouter
from typing import List

from src.lead_automation.api.models.lead import Lead, LeadResponse
from src.lead_automation.services.lead_cleaner import LeadCleaner
from src.lead_automation.utils.validation import validate_row
from src.lead_automation.services.enrichment_client import EnrichmentClient


router = APIRouter()



@router.post("/clean")
def clean_leads(leads: List[Lead]):
    cleaner = LeadCleaner()
    cleaned_data = []

    for lead in leads:
        row = lead.dict()

        try:
            validate_row(row)

            cleaned_data.append({
                "name": row["name"].strip(),
                "email": cleaner.clean_email(row["email"]),
                "phone": cleaner.clean_phone(row["phone"])
            })

        except ValueError:
            continue

    unique_data = cleaner.remove_duplicates(cleaned_data)

    return unique_data

@router.post("/enrich")
async def enrich_leads(leads: List[Lead]):
    cleaner = LeadCleaner()
    client = EnrichmentClient()

    cleaned_data = []

    # 🔹 Step 1 — validate + clean
    for lead in leads:
        row = lead.dict()

        try:
            validate_row(row)

            cleaned_data.append({
                "name": row["name"].strip(),
                "email": cleaner.clean_email(row["email"]),
                "phone": cleaner.clean_phone(row["phone"])
            })

        except ValueError:
            continue

    unique_data = cleaner.remove_duplicates(cleaned_data)

    # 🔹 Step 2 — API lookup
    users = client.fetch_all_users()
    lookup = client.create_lookup(users)

    # 🔹 Step 3 — async enrichment
    enriched_data = await client.process_lead_async(unique_data, lookup)

    return enriched_data



# @router.get("/leads", response_model=List[LeadResponse])
# def get_leads():
#     return FAKE_DB