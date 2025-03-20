# from uuid import UUID
from pydantic import BaseModel, UUID4
from typing import List, Optional
from models.exports import HousingType

class BuildingBase(BaseModel):
    name: str
    locality_uuid: Optional[UUID4] = None

class BuildingCreate(BuildingBase):
    block_uuid: UUID4

class BuildingResponse(BuildingBase):
    uuid: UUID4
    sub_housing: List["BuildingResponse"] = []

    class Config:
        orm_mode = True