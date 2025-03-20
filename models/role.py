"""
Models Module
"""

# pylint: disable=R0903,E0401,C0103
import enum
from sqlalchemy import Boolean, Column, DECIMAL, String, UUID, Enum, ForeignKey
from sqlalchemy.orm import relationship  # , declarative_settings.DBBaseModel


# from app.core.config import settings
from models.base import BaseModel, BaseModelWithUser

# Base = declarative_base()

class RoleModel(BaseModel):
    """
    Role Model Class
    """

    __tablename__ = "roles"

    name = Column(String(256), index=True, unique=True)
    description = Column(String, index=True)