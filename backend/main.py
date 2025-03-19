import logging
from fastapi import FastAPI
from routes.email_routes import router as email_router

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

logger.info("🚀 Initializing FastAPI application...")

# Initialize FastAPI app
app = FastAPI()

logger.info("✅ FastAPI instance created.")

# Include Email Routes
app.include_router(email_router)
logger.info("📩 Email routes included.")

@app.get("/")
def home():
    logger.info("🏠 Root endpoint accessed.")
    return {"message": "API is running"}

# Run API
if __name__ == "__main__":
    import uvicorn
    logger.info("🔄 Starting Uvicorn server on 0.0.0.0:8000...")
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
