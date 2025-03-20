# from uuid import UUID
from pydantic import BaseModel, UUID4
from typing import List, Optional
from datetime import datetime, date
from models.exports import HousingType

class CentralityBase(BaseModel):
    name: str
    locality_uuid: Optional[UUID4] = None

class CentralityCreate(CentralityBase):
    pass

class CentralityResponse(CentralityBase):
    uuid: UUID4
    created_at: datetime
    updated_at: datetime
    sub_housing: List["CentralityResponse"] = []

    class Config:
        orm_mode = True