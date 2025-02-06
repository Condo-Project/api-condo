"""
User Schemas
"""

# pylint: disable=R0903,W0107,E0611
from typing import Optional, List, Any
from uuid import UUID
from decimal import Decimal
from datetime import datetime, date
from pydantic import UUID1, BaseModel, EmailStr, validator
from core.security import password_generator

class UserSchemaBase(BaseModel):
    """
    Base User Schema
    """

    username: str


class UserCreate(UserSchemaBase):
    """
    Create User Schema extend UserSchemaBase
    """

    # role_uuid: UUID
    password: str

    @validator("password", pre=True, always=True)
    def hash_password(cls, password: str) -> str:
        """Valida e converte a senha para um hash bcrypt antes de enviar para o serviço."""
        if len(password) < 8:
            raise ValueError("A senha deve ter pelo menos 8 caracteres.")
        # return bcrypt.hash(password)
        return password_generator(password)

class UserChangePassword(BaseModel):
    """
    Create User Schema extend UserSchemaBase
    """

    current_password: str
    new_password: str


class UserLogin(BaseModel):
    """
    Login  User Schema
    """

    email: EmailStr
    password: str


class UserSchema(UserSchemaBase):
    """
    User Schema
    """

    uuid: UUID
    is_active: bool = True
    is_staff: bool = False
    created_at: datetime
    updated_at: datetime

    class Config:
        """
        Config User Schema
        """

        orm_mode = True
