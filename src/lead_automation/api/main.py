from fastapi import FastAPI

# # 🔥 STEP 1 — import models FIRST (VERY IMPORTANT)
# import lead_automation.db.models

# # 🔥 STEP 2 — then import DB
# from lead_automation.db.database import engine, Base

# # 🔥 STEP 3 — then create tables
# Base.metadata.create_all(bind=engine)

# # 🔥 ADD DEBUG HERE
# print("Tables detected:", Base.metadata.tables.keys())

# 🔥 STEP 4 — then import routes
from lead_automation.api.routes import leads

app = FastAPI()



@app.get("/")
def root():
    return {"message": "Lead Automation API is running"}





@app.get("/health")
def health_check():
    return{"status": "ok"}


app.include_router(leads.router)