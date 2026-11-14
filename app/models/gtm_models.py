import datetime
from typing import List, Optional
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.database import Base

class Account(Base):
    __tablename__ = "accounts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    domain: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    industry: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    employee_count: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=lambda: datetime.datetime.utcnow())

    buying_intents: Mapped[List["BuyingIntent"]] = relationship("BuyingIntent", back_populates="account")
    outreach_briefs: Mapped[List["OutreachBrief"]] = relationship("OutreachBrief", back_populates="account")

class BuyingIntent(Base):
    __tablename__ = "buying_intents"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    account_id: Mapped[int] = mapped_column(Integer, ForeignKey("accounts.id"), nullable=False)
    intent_score: Mapped[int] = mapped_column(Integer, nullable=False)
    intent_category: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=lambda: datetime.datetime.utcnow())

    account: Mapped["Account"] = relationship("Account", back_populates="buying_intents")

class OutreachBrief(Base):
    __tablename__ = "outreach_briefs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    account_id: Mapped[int] = mapped_column(Integer, ForeignKey("accounts.id"), nullable=False)
    brief_content: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=lambda: datetime.datetime.utcnow())

    account: Mapped["Account"] = relationship("Account", back_populates="outreach_briefs")
