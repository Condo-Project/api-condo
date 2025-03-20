# from uuid import UUID
from pydantic import BaseModel, UUID4
from typing import List, Optional
from models.exports import HousingType

class FlatBase(BaseModel):
    name: str
    locality_uuid: Optional[UUID4] = None

class FlatCreate(FlatBase):
    building_uuid: UUID4

class FlatResponse(FlatBase):
    uuid: UUID4
    sub_housing: List["FlatResponse"] = []

    class Config:
        orm_mode = True