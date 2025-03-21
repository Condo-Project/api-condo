"""
Profile Schema
"""

from uuid import UUID
from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date
from decimal import Decimal

from models.profile import ProfileStatusEnum, ProfileDocumentEnum

class ProfileSchema(BaseModel):
    uuid: Optional[UUID]
    first_name: Optional[str]
    last_name: Optional[str]
    user_uuid: UUID

    document_identification: Optional[str]
    birth_date: Optional[date]
    document_type: Optional[ProfileDocumentEnum]
    status: Optional[ProfileStatusEnum]

    balance: Optional[Decimal] = 0.0
    total_investment: Optional[Decimal] = 0.0
    terms_conditions: Optional[bool]
    avatar: Optional[str]

    bank_name: Optional[str]
    bank_account: Optional[str]
    bank_iban: Optional[str]
    profession: Optional[str]
    company: Optional[str]


    class Config:
        orm_mode = True

class ProfileUpdateSchema(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]

    document_identification: Optional[str]
    birth_date: Optional[date]
    document_type: Optional[ProfileDocumentEnum]
    status: Optional[ProfileStatusEnum]

    balance: Optional[Decimal] = 0.0
    total_investment: Optional[Decimal] = 0.0
    terms_conditions: Optional[bool]
    avatar: Optional[str]

    bank_name: Optional[str]
    bank_account: Optional[str]
    bank_iban: Optional[str]
    profession: Optional[str]
    company: Optional[str]


    class Config:
        orm_mode = True


