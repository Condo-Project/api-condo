
from uuid import UUID
from typing import List

from fastapi import status, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm

from core.auth import authentication, create_access
from decimal import Decimal
from datetime import datetime, date
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from db.decorators import postgres_transactional
from core.config import settings
from core.security import password_generator

from repositories.exports import (
    BaseRepository,
)

from models.exports import (
    RoleModel,
)
from schemas.exports import (
    RoleSchema,
    FilterSchema,
)


class RoleService:
    def __init__(self, target = None):
        self.role_repository = BaseRepository(RoleModel)

    @postgres_transactional
    async def get_all(
        self,
    )-> RoleSchema:
        """
        Get All Roles
        """

        return await self.role_repository.get_all(FilterSchema())

    @postgres_transactional
    async def get(
        self,
        role_uuid:UUID
    )-> RoleSchema:
        """
        Get Role by UUID
        """

        return await self.role_repository.get(role_uuid)

    @postgres_transactional
    async def get_by_name(
        self,
        name:str
    )-> RoleSchema:
        """
        Get Role by Name
        """

        return await self.role_repository.get_one_by_filter(
            FilterSchema(
                filter_column="name",
                filter_value=name
            )
        )

role_service = RoleService()