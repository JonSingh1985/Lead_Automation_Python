from fastapi import FastAPI
from src.lead_automation.api.routes import leads

app = FastAPI()

app.include_router(leads.router)

@app.get("/health")
def health_check():
    return{"status": "ok"}