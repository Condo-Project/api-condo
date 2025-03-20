"""
Models Module
"""

# pylint: disable=R0903,E0401,C0103
import enum
from sqlalchemy import Boolean, Column, DECIMAL, String, UUID, Enum, ForeignKey, Integer
from sqlalchemy.orm import relationship  # , declarative_settings.DBBaseModel


# from app.core.config import settings
from models.base import BaseModel, BaseModelWithUser

class HousingType(enum.Enum):
    """
    HOUSING TYPE
    """

    CENTRALIDADE = "CENTRALIDADE"
    CONDOMINIO = "CONDOMINIO"
    BLOCO = "BLOCO"
    PREDIO = "PREDIO"
    APARTAMENTO = "APARTAMENTO"

class HousingModel(BaseModelWithUser):
    __tablename__ = "housing"

    name = Column(String, index=True, nullable=False)
    housing_type = Column(
        Enum(HousingType),
        default=HousingType.APARTAMENTO.value,
        nullable=False,
    )
    locality_uuid = Column(UUID, ForeignKey("localities.uuid"), nullable=True)
    parent_uuid = Column(UUID, ForeignKey("housing.uuid"), nullable=True)

    # Relacionamento recursivo
    # parent = relationship("HousingModel", remote_side=[BaseModelWithUser.uuid], backref="sub_housing")








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