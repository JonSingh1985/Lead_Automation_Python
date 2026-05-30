from sqlalchemy import Column, Integer, String
from src.lead_automation.db.database import Base

class Lead(Base):
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    phone = Column(String, nullable=False)

    company = Column(String, nullable=True)
    city = Column(String, nullable=True)

    lead_score = Column(String, nullable=True)
    reason = Column(String, nullable=True)