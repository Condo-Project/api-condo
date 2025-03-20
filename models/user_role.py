"""
Models Module
"""

from sqlalchemy import Column, UUID, ForeignKey
from sqlalchemy.orm import relationship
from models.base import BaseModel

class UserRoleModel(BaseModel):
    """
    UserRole Model Class
    """
    __tablename__ = "user_roles"

    user_uuid = Column(UUID, ForeignKey('users.uuid'))
    user = relationship('UserModel')

    role_uuid = Column(UUID, ForeignKey('roles.uuid'))
    role = relationship('RoleModel')