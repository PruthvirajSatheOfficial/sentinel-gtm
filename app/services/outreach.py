from typing import List
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.gtm_models import OutreachBrief as OutreachBriefModel, Account as AccountModel
from app.schemas.gtm_schemas import OutreachBrief as OutreachBriefSchema
from google import genai
from google.genai import types

client = genai.Client()

def generate_outreach_brief(account) -> OutreachBriefModel:
    intents = account.buying_intents
    intent_text = ", ".join([i.intent_category for i in intents]) if intents else "General Market Research"
    prompt = f"""


    """
    response = client.models.generate_content(
        model = "gemini-2.5-flash",
        contents= prompt,
        config=types.GenerateContentConfig(
            system_instruction="",
            temperature=0.9
        )

    )
    return OutreachBriefModel(
        account_id = account.id,
        brief_content = response.text
    )