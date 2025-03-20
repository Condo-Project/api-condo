
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
    BaseRepository,
)


from models.exports import (
    UserModel,
    HousingType,
    HousingModel
)
from schemas.user import (
    UserSchema,
)
from schemas.exports import (
    BlockCreate,
    BuildingCreate,
    CentralityCreate,
    CentralityResponse,
    FilterSchema,
    FlatCreate,
    HousingCreate,
    HousingResponse,
)



class HousingService:
    def __init__(self, target = None):
        self.housing_repository = BaseRepository(HousingModel)
    
    @postgres_transactional
    async def get_all( self )-> HousingResponse:
        """
        Get All Localities
        """
        filter = FilterSchema()
        return await self.housing_repository.get_all(filter)
    
    @postgres_transactional
    async def get_all_centralities( self )-> HousingResponse:
        """
        Get All Centralities
        """
        filter = FilterSchema(
            filter_column="housing_type",
            filter_value=HousingType.CENTRALIDADE.value
        )
        return await self.housing_repository.get_all(filter)
    
    @postgres_transactional
    async def get_all_blocks( self )-> HousingResponse:
        """
        Get All Blocks
        """
        filter = FilterSchema(
            filter_column="housing_type",
            filter_value=HousingType.BLOCO.value
        )
        return await self.housing_repository.get_all(filter)
    
    @postgres_transactional
    async def get_all_building( self )-> HousingResponse:
        """
        Get All Localities
        """
        filter = FilterSchema(
            filter_column="housing_type",
            filter_value=HousingType.PREDIO.value
        )
        return await self.housing_repository.get_all(filter)
    
    @postgres_transactional
    async def get_all_flats( self )-> HousingResponse:
        """
        Get All Flats
        """
        filter = FilterSchema(
            filter_column="housing_type",
            filter_value=HousingType.APARTAMENTO.value
        )
        return await self.housing_repository.get_all(filter)

    
    @postgres_transactional
    async def create_housing(self, housing_data: HousingCreate, user: UserSchema):

        try:

            new_housing: HousingModel = HousingModel()
            self.housing_repository.set_attrs(new_housing, housing_data.dict(exclude_unset=True))
            new_housing.saved_by = user.uuid
            return await self.housing_repository.save(new_housing)
        except IntegrityError as e:
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
                detail="Já existe um utilizador com este username registado.",
            ) from e
    
    @postgres_transactional
    async def create_centrality(self, housing_data: CentralityCreate, user: UserSchema):

        try:

            new_housing: HousingModel = HousingModel()
            self.housing_repository.set_attrs(new_housing, housing_data.dict(exclude_unset=True))
            new_housing.saved_by = user.uuid
            new_housing.housing_type = HousingType.CENTRALIDADE
            return await self.housing_repository.save(new_housing)
        except IntegrityError as e:
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
                detail="Já existe uma centralidade com este nome registado.",
            ) from e
    
    
    @postgres_transactional
    async def create_block(self, housing_data: BlockCreate, user: UserSchema):

        try:

            new_housing: HousingModel = HousingModel()
            self.housing_repository.set_attrs(new_housing, housing_data.dict(exclude_unset=True))
            new_housing.saved_by = user.uuid
            new_housing.parent_uuid = housing_data.centrality_uuid
            new_housing.housing_type = HousingType.BLOCO
            return await self.housing_repository.save(new_housing)
        except IntegrityError as e:
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
                detail="Já existe uma bloco com este nome registado.",
            ) from e
    
    
    @postgres_transactional
    async def create_building(self, housing_data: BuildingCreate, user: UserSchema):

        try:

            new_housing: HousingModel = HousingModel()
            self.housing_repository.set_attrs(new_housing, housing_data.dict(exclude_unset=True))
            new_housing.saved_by = user.uuid
            new_housing.parent_uuid = housing_data.block_uuid
            new_housing.housing_type = HousingType.PREDIO
            return await self.housing_repository.save(new_housing)
        except IntegrityError as e:
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
                detail="Já existe uma predio com este nome registado.",
            ) from e
    
    
    @postgres_transactional
    async def create_flat(self, housing_data: FlatCreate, user: UserSchema):

        try:

            new_housing: HousingModel = HousingModel()
            self.housing_repository.set_attrs(new_housing, housing_data.dict(exclude_unset=True))
            new_housing.saved_by = user.uuid
            new_housing.parent_uuid = housing_data.building_uuid
            new_housing.housing_type = HousingType.APARTAMENTO
            return await self.housing_repository.save(new_housing)
        except IntegrityError as e:
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
                detail="Já existe uma apartamento com este nome registado.",
            ) from e
    

housing_service = HousingService()