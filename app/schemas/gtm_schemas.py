from pydantic import BaseModel, Field
import datetime
import typing

class Account(BaseModel):
    id: int
    name: str
    email: str
    domain: str
    industry: typing.Optional[str] = None
    employee_count: typing.Optional[int] = None

    class Config:
        orm_mode = True

class BuyingIntent(BaseModel):
    id: int
    account_id: int
    intent_score: int
    intent_category: str
    created_at: datetime.datetime

    class Config:
        orm_mode = True

class OutreachBrief(BaseModel):
    id: int
    account_id: int
    brief_content: str
    created_at: datetime.datetime

    class Config:
        orm_mode = True