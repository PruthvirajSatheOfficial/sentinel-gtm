from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.gtm_models import Account as AccountModel
from app.schemas.gtm_schemas import Account as AccountSchema, AccountCreate as AccountCreateSchema, AccountUpdate as AccountUpdateSchema

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

@router.get("/{account_id}", response_model=AccountSchema)
def get_account(account_id: int, db: Session = Depends(get_db)):
    db_account = db.query(AccountModel).filter(AccountModel.id == account_id).first()
    if db_account is None:
        raise HTTPException(status_code=404, detail="Account not found")
    return db_account

@router.get("/", response_model=List[AccountSchema])
def get_accounts(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    accounts = db.query(AccountModel).offset(skip).limit(limit).all()
    return accounts

@router.put("/{account_id}", response_model=AccountSchema)
def update_account(account_id: int, account: AccountUpdateSchema , db : Session = Depends(get_db)):
    db_account = db.query(AccountModel).filter(AccountModel.id == account_id).first()
    if db_account is None:
        raise HTTPException(status_code=404, detail="Account not found")
    updated_account = account.model_dump(exclude_unset=True)
    for key, value in updated_account.items():
        setattr(db_account, key, value)
    db.commit()
    db.refresh(db_account) 
    return db_account