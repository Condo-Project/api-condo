"""
UserRole Schemas
"""

from uuid import UUID
from pydantic import BaseModel

class UserRoleSchema(BaseModel):
    user_uuid: UUID
    role_uuid: UUID

    class Config:
        orm_mode = True

class UserRoleMappingSchema(UserRoleSchema):
    name: str
