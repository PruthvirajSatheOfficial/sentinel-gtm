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

load_dotenv()


router = APIRouter(
    prefix="/outreach-briefs",
)

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
    

@router.get("/{account_id}", response_model=List[OutreachBriefSchema])
def get_outreach_briefs(account_id: int, db: Session = Depends(get_db)):
    db_outreach_briefs = db.query(OutreachBriefModel).filter(OutreachBriefModel.account_id == account_id).all()
    if not db_outreach_briefs:
        raise HTTPException(status_code=404, detail="Outreach briefs not found")
    return db_outreach_briefs

@router.post("/{account_id}", response_model=OutreachBriefSchema)
def create_outreach_brief(account_id: int, outreach_brief: OutreachBriefSchema, db: Session = Depends(get_db)):
    account = db.query(AccountModel).filter(AccountModel.id == account_id).first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")    
    outreach_brief_instance = generate_outreach_brief(account)

    db.add(outreach_brief_instance)
    db.commit()
    db.refresh(outreach_brief_instance)
    return outreach_brief_instance