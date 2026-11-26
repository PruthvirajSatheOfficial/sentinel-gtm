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

def generate_buying_intents(db: Session, account: AccountModel, nums_intent: int = 3):
    existing_intents = {i.intent_category.strip().lower() for i in account.buying_intents}
    
    system_prompt = """
    You are a B2B sales analyst. Generate new buying intents for a target account.
    Do not repeat categories that already exist for the account.
    Keep intent categories short and clear, and score each one from 0 to 100.
    """

    user_prompt = f"""
    Account: {account.name}
    Domain: {account.domain}
    Industry: {account.industry}
    Existing categories to skip: {", ".join(existing_intents)}
    Create up to {nums_intent} new buying intents.
    """
   
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=user_prompt,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            response_mime_type="application/json",
            response_schema=IntentListResponse,
        ),
    )

    if not isinstance(response.parsed, IntentListResponse):
        return []

    created = []
    for item in response.parsed.intents:
        key = item.intent_category.strip().lower()
        if key in existing_intents:
            continue

        existing_intents.add(key)
        row = BuyingIntentModel(
            account_id=account.id,
            intent_category=item.intent_category.strip(),
            # add your other fields from `item` here
        )
        created.append(row)

    db.add_all(created)
    db.commit()
    return created