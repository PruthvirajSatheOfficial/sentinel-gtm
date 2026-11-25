from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.gtm_models import BuyingIntent as BuyingIntentModel , Account as AccountModel
from app.schemas.gtm_schemas import BuyingIntent as BuyingIntentSchema, IntentListResponse
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

client = genai.Client()

def generate_buying_intents(account: AccountModel, nums_intent: int = 3, db : Session = Depends(get_db)) -> List[BuyingIntentModel]:
    existing_intents = {i.intent_category.strip() for i in account.buying_intents}
    system_prompt = """
    
    """

    user_prompt = """

    """

    response = client.models.generate_content(
        model= "gemini-2.5-flash",
        contents= user_prompt'
        config=types.GenerateContentConfig(
            system_intruction = system_prompt,
            response_mime_type = "application/json",
            response_schema = IntentListResponse,
            temperature = 0.9
        )
    )
    parsed = response.parsed
    ... 