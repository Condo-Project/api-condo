# from uuid import UUID
from pydantic import BaseModel, UUID4
from typing import List, Optional
from models.exports import HousingType

class BlockBase(BaseModel):
    name: str
    locality_uuid: Optional[UUID4] = None

class BlockCreate(BlockBase):
    centrality_uuid: UUID4

class BlockResponse(BlockBase):
    uuid: UUID4
    sub_housing: List["BlockResponse"] = []

    class Config:
        orm_mode = True