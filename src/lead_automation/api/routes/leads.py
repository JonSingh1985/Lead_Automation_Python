from fastapi import APIRouter
from typing import List

from src.lead_automation.api.models.lead import LeadCreate, LeadResponse

router = APIRouter()

# fake DB (temp)
FAKE_DB = []
lead_id_counter = 1



@router.post("/leads", response_model=LeadResponse)
def create_lead(lead: LeadCreate):
    global lead_id_counter

    new_lead = {
        "id": lead_id_counter,
        "name": lead.name,
        "email": lead.email,
        "phone": lead.phone,
    }

    FAKE_DB.append(new_lead)
    lead_id_counter += 1

    return new_lead

@router.get("/leads", response_model=List[LeadResponse])
def get_leads():
    return FAKE_DB