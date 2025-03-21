"""
Models Profile
"""
import enum
from sqlalchemy import Boolean, Date, Column, DECIMAL, Integer, String, UUID, Enum, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from models.base import BaseModel

class ProfileDocumentEnum(enum.Enum):
    """
    ENUM Status
    """
    BILHETE = "BILHETE"
    PASSAPORTE = "PASSAPORTE"


class ProfileStatusEnum(enum.Enum):
    """
    ENUM Status
    """
    PENDENTE = "PENDENTE"
    SUSPENSO = "SUSPENSO"
    APROVADO = "APROVADO"
    REJEITADO = "REJEITADO"


class ProfileModel(BaseModel):
    __tablename__ = "profiles"

    #============= Identificação Básica
    first_name = Column(String)
    last_name = Column(String)
    document_identification = Column(String)
    birth_date = Column(Date)
    document_type = Column(
        Enum(ProfileDocumentEnum),
        default=ProfileDocumentEnum.BILHETE.value,
        nullable=False,
    )
    status = Column(
        Enum(ProfileStatusEnum),
        default=ProfileStatusEnum.PENDENTE.value,
        nullable=False,
    )
    avatar = Column(String, nullable=True)

    user_uuid = Column(UUID, ForeignKey('users.uuid'), unique=True, nullable=False)
    user = relationship('UserModel')