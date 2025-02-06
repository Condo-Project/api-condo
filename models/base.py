"""
No presente ficheiro serão criado as classes abtracts relacionadas comas models
"""

# pylint: disable=R0903,E0401,C0103,E1102
import uuid
from sqlalchemy import UUID, Boolean, Column, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship, foreign
from sqlalchemy.ext.declarative import declared_attr

from core.config import settings


class BaseModel(settings.DBBaseModel):
    """
    A presente class tem como objectivo add os campos abaixo nos class filhas
    """

    __abstract__ = True
    uuid = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False,
        index=True,
    )
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())


class BaseModelWithUser(BaseModel):
    """
    A presente class tem como objectivo add os campos abaixo nos class filhas
    """

    __abstract__ = True
    saved_by = Column(UUID, ForeignKey("users.uuid"))

    # @declared_attr
    # def user(cls):
    #     return relationship("UserModel", foreign_keys=[cls.saved_by])