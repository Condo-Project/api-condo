"""
User Schemas
"""

# pylint: disable=R0903,W0107,E0611
from typing import Optional, List, Any
from uuid import UUID
from enum import Enum
from datetime import date, datetime, time
from pydantic import UUID1, BaseModel, EmailStr
from decimal import Decimal
# from schemas.base import BaseSchema 
# from app.schemas.address import (
#     AddressSchemaBase,
# )

class RoleSchema(BaseModel):

    uuid: UUID
    name: str
    description: Optional[str]
    is_active: Optional[bool]
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class RoleColumnEnum(str, Enum):
    Agricultor = "Agricultor"
    Investidor = "Investidor"
    Administrador = "Administrador"