from fastapi import APIRouter
from services.email_services import fetch_unread_emails, analyze_email
from pydantic import BaseModel

router = APIRouter()

# Define request model
class EmailRequest(BaseModel):
    subject: str
    body: str
    sender: str

# API to fetch unread emails & analyze them
@router.get("/fetch_and_analyze")
async def fetch_and_analyze():
    emails = fetch_unread_emails()
    results = []
    for email in emails:
        analysis = analyze_email(email)
        results.append({"email": email, "analysis": analysis})
    return results

# API to analyze a single email manually
@router.post("/analyze_email")
async def analyze_email_api(email: EmailRequest):
    return analyze_email(email.dict())
