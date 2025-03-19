import joblib
from googleapiclient.discovery import build
from google.oauth2 import service_account
from transformers import pipeline
import json

# Load models
phishing_model = joblib.load("models/emotion_model.pkl")
emotion_classifier = pipeline("text-classification", model="distilbert-base-uncased-finetuned-sst-2-english")

# Gmail API authentication
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]
SERVICE_ACCOUNT_FILE = "credentials.json"

def authenticate_gmail():
    creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    return build("gmail", "v1", credentials=creds)

# Fetch unread emails
def fetch_unread_emails():
    service = authenticate_gmail()
    results = service.users().messages().list(userId="me", labelIds=["INBOX"], q="is:unread", maxResults=5).execute()
    messages = results.get("messages", [])
    
    emails = []
    for msg in messages:
        msg_data = service.users().messages().get(userId="me", id=msg["id"]).execute()
        headers = msg_data["payload"]["headers"]

        subject = next(header["value"] for header in headers if header["name"] == "Subject")
        sender = next(header["value"] for header in headers if header["name"] == "From")
        email_body = msg_data["snippet"]  # Fetch email snippet

        emails.append({"subject": subject, "body": email_body, "sender": sender})
    
    return emails

# Detect phishing
def detect_phishing(email_text):
    return phishing_model.predict([email_text])[0]  # Returns 0 (safe) or 1 (phishing)

# Detect emotional manipulation
def detect_emotional_manipulation(email_text):
    result = emotion_classifier(email_text)
    return result[0]['label'], result[0]['score']

# Analyze email
def analyze_email(email):
    email_text = email["subject"] + " " + email["body"]
    phishing_result = detect_phishing(email_text)
    emotion_label, emotion_score = detect_emotional_manipulation(email_text)

    risk_level = "High" if phishing_result == 1 or emotion_score > 0.75 else "Low"

    return {
        "phishing_risk": "Phishing Detected" if phishing_result == 1 else "Safe",
        "emotional_manipulation": f"{emotion_label} ({emotion_score:.2f})",
        "risk_level": risk_level,
        "recommendation": "Do not click links or share personal details." if risk_level == "High" else "Email seems safe."
    }
