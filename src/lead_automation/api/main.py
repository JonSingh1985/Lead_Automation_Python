from fastapi import FastAPI
from src.lead_automation.api.routes import leads

app = FastAPI()



@app.get("/")
def root():
    return {"message": "Lead Automation API is running"}





@app.get("/health")
def health_check():
    return{"status": "ok"}


app.include_router(leads.router)