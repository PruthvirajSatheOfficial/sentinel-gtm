from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.gtm_models import BuyingIntent as BuyingIntentModel , Account as AccountModel
from app.schemas.gtm_schemas import BuyingIntent as BuyingIntentSchema, IntentListResponse
from app.services.buying import generate_buying_intents

router = APIRouter(
    prefix="/buying_intents"
)


@router.get("/{account_id}", response_model = List[BuyingIntentSchema])
def get_buying_intents(account_id : int, db : Session = Depends(get_db)):
    db_buying_intents = db.query(BuyingIntentModel).filter(BuyingIntentModel.account_id == account_id).all()
    if not db_buying_intents:
        raise HTTPException(status_code=404 , detail =f"Buying Intents for Account {account_id} Not Found")
    return db_buying_intents

@router.post("/{account_id}", response_model=List[BuyingIntentSchema])
def create_buying_intent(account_id: int, db: Session = Depends(get_db)):
    account = db.query(AccountModel).filter(AccountModel.id == account_id).first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found !!!")

    buying_intents_list = generate_buying_intents(db, account)
    return buying_intents_list