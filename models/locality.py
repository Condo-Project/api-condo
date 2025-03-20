"""
Models Module
"""

# pylint: disable=R0903,E0401,C0103
import enum
from sqlalchemy import Boolean, Column, DECIMAL, String, UUID, Enum, ForeignKey
from sqlalchemy.orm import relationship  # , declarative_settings.DBBaseModel


# from app.core.config import settings
from models.base import BaseModel, BaseModelWithUser

class LocalityType(enum.Enum):
    """
    LOCALITY TYPE
    """

    PAIS = "PAIS"
    PROVINCIA = "PROVINCIA"
    MUNICIPIO = "MUNICIPIO"

class LocalityModel(BaseModelWithUser):
    __tablename__ = "localities"

    name = Column(String, index=True, nullable=False)
    locality_type = Column(
        Enum(LocalityType),
        default=LocalityType.MUNICIPIO.value,
        nullable=False,
    )
    parent_uuid = Column(UUID, ForeignKey("localities.uuid"), nullable=True)

    # Relacionamento recursivo
    # parent = relationship("Localidade", remote_side=[BaseModelWithUser.uuid], backref="sub_localities")







# class UserProfileModel(BaseModel):
#     """
#     User Model Class
#     """

#     __tablename__ = "user_profiles"

#     phone_number = Column(String, index=True, unique=True)
#     password = Column(String(256), nullable=False)
#     balance = Column(DECIMAL(scale=2), default=0.0, nullable=False)
#     terms_conditions = Column(Boolean, default=False)
#     avatar = Column(String)
#     is_staff = Column(Boolean, default=False)
#     first_name: Column(String, index=True)
#     last_name: Column(String, index=True)
#     gender_name: "MASCULINO",
#     birth_date: "1999-09-21",
#     father_first_name: "MUHONGO",
#     father_last_name: "CABANGA",
#     mother_first_name: "MARIA",
#     mother_last_name: "DE FATIMA CORREIA",
#     birth_province_name: "LUANDA",
#     residence_country_name: "ANGOLA",
#     residence_province_name: "LUANDA",
#     residence_municipality_name: "LUANDA",
#     residence_commune_name: "SAMBA",
#     residence_neighbor: "SAMBA GRANDE",
#     residence_address: "BAIRRO TALATONA CASA N SN"

#     # contacts = relationship('ContactModel')
#     # addresses = relationship('AddressModel')