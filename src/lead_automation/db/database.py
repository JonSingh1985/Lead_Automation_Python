
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


DATABASE_URL = "sqlite:///./leads.db"

# Creat engine (connection to db)
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

# Session = connection instance
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

import src.lead_automation.db.models

Base.metadata.create_all(bind=engine)
print("Tables detected:", Base.metadata.tables.keys())