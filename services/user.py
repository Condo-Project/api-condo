
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
)
from schemas.user import (
    UserSchema,
    UserCreate as UserSchemaCreate,
    UserChangePassword,
)
from schemas.exports import (
    FilterSchema,
)



class UserService:
    def __init__(self, target = None):
        self.user_repository = BaseRepository(UserModel)
    
    @postgres_transactional
    async def get_all( self )-> UserSchema:
        """
        Get All Users
        """
        filter = FilterSchema()
        return await self.user_repository.get_all(filter)
    
    @postgres_transactional
    async def verify_username( self, username:str )-> UserSchema:
        """
        Get All Users
        """
        filter = FilterSchema(
            filter_column="username",
            filter_value=username,
        )
        if (await self.user_repository.get_one_by_filter(filter)):
            return {"is_valid": True}
        return {"is_valid": False}

    
    @postgres_transactional
    async def create_user(self, user_data: UserSchemaCreate):

        try:

            new_user: UserModel = UserModel()
            self.user_repository.set_attrs(new_user, user_data.dict(exclude_unset=True))
            new_user.secret_key = otp_service.generate_secret_key()
            user = await self.user_repository.save(new_user)

            # if user:      
            #     await user_role_service.create(
            #         UserRoleSchema(
            #             user_uuid=user.uuid, 
            #             role_uuid=role_uuid
            #         )
            #     )
            #     otp = otp_service.generate_code(user.secret_key)
            #     self.notity_user(
            #         OTPValidation(
            #             username=user.username,
            #             otp=otp
            #         )
            #     )
            return user
        except IntegrityError as e:
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
                detail="Já existe um utilizador com este username registado.",
            ) from e
    
    
    @postgres_transactional
    async def login(
        self,
        form_data: OAuth2PasswordRequestForm,
    ):
        """
        Login
        """

        user: UserWithRoles = await authentication(
            email=form_data.username, password=form_data.password
        )

        if not user:
            raise HTTPException(
                detail="Dados de acesso incorretos.",
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        # user.addresses = await AddressRepository.get_all(user.uuid, db)

        return JSONResponse(
            content={
                "access_token": create_access(sub=str(user.uuid)),
                "token_type": "bearer",
                "data": jsonable_encoder(user),
            },
            status_code=status.HTTP_200_OK,
        )
    
    @postgres_transactional
    async def get_current_user(
        self,
        current_user: UserSchema
    )-> UserSchema:
        """
        Login
        """
        # current_user.roles = await user_role_service.my_roles(current_user.uuid)
        # current_user.profile = await profile_service.get_current_profile(current_user.uuid)
        return current_user

user_service = UserService()