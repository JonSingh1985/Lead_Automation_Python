from pydantic import BaseModel, EmailStr
from typing import Optional

class Lead(BaseModel):
    name: str
    email: str
    phone: str

class LeadResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    phone: Optional[str]