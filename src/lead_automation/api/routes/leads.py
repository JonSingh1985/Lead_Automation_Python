import asyncio

from fastapi import APIRouter, Depends
from fastapi import HTTPException
from typing import List

from src.lead_automation.api.models.lead import Lead, LeadResponse
from src.lead_automation.services.lead_cleaner import LeadCleaner
from src.lead_automation.utils.validation import validate_row
from src.lead_automation.services.enrichment_client import EnrichmentClient

from sqlalchemy.orm import Session
from src.lead_automation.db.dependencies import get_db

router = APIRouter()



@router.post("/clean")
def clean_leads(leads: List[Lead]):
    cleaner = LeadCleaner()
    cleaned_data = []

    if not leads:
        raise HTTPException(status_code=400, detail="No leads provided")

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

    if not cleaned_data:
        raise HTTPException(status_code=400, detail="All rows invalid")

    unique_data = cleaner.remove_duplicates(cleaned_data)

    return {
        "status": "success",
        "count": len(unique_data),
        "data": unique_data
    }





@router.post("/enrich")
async def enrich_leads(leads: List[Lead]):
    cleaner = LeadCleaner()
    client = EnrichmentClient()

    if not leads:
        raise HTTPException(status_code=400, detail="No leads provided")

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

    if not cleaned_data:
        raise HTTPException(status_code=400, detail="All rows invalid")

    unique_data = cleaner.remove_duplicates(cleaned_data)

    try:
        # 🔹 Step 2 — API lookup
        users = client.fetch_all_users()
        lookup = client.create_lookup(users)

        # 🔹 Step 3 — async enrichment
        enriched_data = await client.process_lead_async(unique_data, lookup)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Enrichment faield: {str(e)}")


    return {
        "status": "success",
        "count": len(enriched_data),
        "data": enriched_data
    }


@router.get("/test-db")
def test_db(db: Session = Depends(get_db)):
    return {"message": "DB connected"}


# @router.get("/leads", response_model=List[LeadResponse])
# def get_leads():
#     return FAKE_DB