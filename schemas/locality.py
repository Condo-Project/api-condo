# from uuid import UUID
from pydantic import BaseModel, UUID4
from typing import List, Optional
from datetime import datetime, date
from models.exports import LocalityType

class LocalityBase(BaseModel):
    name: str
    locality_type: LocalityType
    parent_uuid: Optional[UUID4] = None

class LocalityCreate(LocalityBase):
    pass

class LocalityResponse(LocalityBase):
    uuid: UUID4
    parent_name: Optional[str] = None
    sub_localities: List["LocalityResponse"] = []

    class Config:
        orm_mode = True
