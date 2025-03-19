import joblib

# Load models
phishing_model = joblib.load("models/emotion_model.pkl")

def get_phishing_model():
    return phishing_model
