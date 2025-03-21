
from uuid import UUID
from typing import List
import random

import pyotp
import time

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
    LocalityRepository,
)


from models.exports import (
    UserModel,
    LocalityType,
    LocalityModel
)
from schemas.user import (
    UserSchema,
)
from schemas.exports import (
    FilterSchema,
    LocalityCreate,
    LocalityResponse
)



class LocalityService:
    def __init__(self, target = None):
        self.locality_repository = LocalityRepository()
    
    @postgres_transactional
    async def get_all( self, filter:FilterSchema = None )-> LocalityResponse:
        """
        Get All Localities
        """
        # filter = FilterSchema()
        return await self.locality_repository.get_all(filter)

    
    @postgres_transactional
    async def create_locality(self, locality_data: LocalityCreate, user: UserSchema):

        try:

            new_locality: LocalityModel = LocalityModel()
            self.locality_repository.set_attrs(new_locality, locality_data.dict(exclude_unset=True))
            new_locality.saved_by = user.uuid
            return await self.locality_repository.save(new_locality)
        except IntegrityError as e:
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
                detail="Já existe um utilizador com este username registado.",
            ) from e
    

locality_service = LocalityService()