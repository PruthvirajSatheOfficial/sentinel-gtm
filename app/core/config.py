import os 
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/sentinel_gtm")
INGESTION_API_KEY = os.getenv("INGESTION_API_KEY", "default_ingestion_api_key")
WEBHOOK_URL = os.getenv("WEBHOOK_URL", "https://default-webhook-url.com")
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "default_webhook_secret")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "default_anthropic_api_key")

DEDUPLICATION_THRESHOLD = float(os.getenv("DEDUPLICATION_THRESHOLD", 0.9))
HOT_LEAD_THRESHOLD = float(os.getenv("HOT_LEAD_THRESHOLD", 0.75))