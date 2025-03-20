# from uuid import UUID
from pydantic import BaseModel, UUID4
from typing import List, Optional
from datetime import datetime, date
from models.exports import HousingType

class HousingBase(BaseModel):
    name: str
    housing_type: HousingType
    parent_uuid: Optional[UUID4] = None
    locality_uuid: Optional[UUID4] = None

class HousingCreate(HousingBase):
    pass

class HousingResponse(HousingBase):
    uuid: UUID4
    created_at: datetime
    updated_at: datetime
    sub_housing: List["HousingResponse"] = []

    class Config:
        orm_mode = True
