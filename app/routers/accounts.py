from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.gtm_models import Account as AccountModel
from app.schemas.gtm_schemas import Account as AccountSchema, AccountCreate as AccountCreateSchema

router = APIRouter(
    prefix="/accounts",
    tags=["accounts"])

@router.post("/create", response_model=AccountSchema)
def create_account(account: AccountCreateSchema, db: Session = Depends(get_db)):
    existing_account = db.query(AccountModel).filter(AccountModel.domain == account.domain).first()
    if existing_account:
        raise HTTPException(status_code=400, detail="Account with this domain already exists")
    db_account = AccountModel(**account.model_dump())
    db.add(db_account)
    db.commit()
    db.refresh(db_account)
    return db_account
