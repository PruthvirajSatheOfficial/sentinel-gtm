from pydantic import BaseModel, ConfigDict, Field
import datetime
import typing
from typing import List, Optional

class AccountCreate(BaseModel):
    name: str
    domain: str
    industry: Optional[str] = None
    employee_count: typing.Optional[int] = None

    model_config = ConfigDict(from_attributes=True)

class Account(BaseModel):
    id: int
    name: str
    domain: str
    industry: typing.Optional[str] = None
    employee_count: typing.Optional[int] = None
    created_at: datetime.datetime

    model_config = ConfigDict(from_attributes=True)

class BuyingIntent(BaseModel):
    id: int
    account_id: int
    intent_score: int
    intent_category: str
    created_at: datetime.datetime

    model_config = ConfigDict(from_attributes=True)

class OutreachBrief(BaseModel):
    id: int
    account_id: int
    brief_content: str
    created_at: datetime.datetime

    model_config = ConfigDict(from_attributes=True)

class AccountUpdate(BaseModel):
    name: Optional[str] = None
    domain: Optional[str] = None
    industry: Optional[str] = None
    employee_count: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)

class BuyingIntentCreate(BaseModel):
    intent_score: int
    intent_category: str

    model_config = ConfigDict(from_attributes=True)

class OutreachBriefCreate(BaseModel):
    brief_content: str

    model_config = ConfigDict(from_attributes=True)

class IntentListResponse(BaseModel):
    intents: List[BuyingIntentCreate]
    