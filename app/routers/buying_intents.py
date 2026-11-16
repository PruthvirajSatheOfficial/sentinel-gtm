from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.gtm_models import OutreachBrief

router = APIRouter()

@router.get("/outreach-briefs", response_model=List[OutreachBrief])
def get_outreach_briefs(db: Session = Depends(get_db)):
    pass