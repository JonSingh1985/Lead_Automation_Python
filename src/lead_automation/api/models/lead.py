from pydantic import BaseModel, EmailStr
from typing import Optional

class LeadCreate(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None

class LeadResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    phone: Optional[str]