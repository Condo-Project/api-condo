
from uuid import UUID
from typing import List

import re
import unicodedata
from fastapi import UploadFile


from fastapi import status, HTTPException
from sqlalchemy.exc import IntegrityError

from services.cloudinary import (
    upload_avatar
)

from db.decorators import (
    postgres_transactional
)

from repositories.exports import (
    BaseRepository,
)

from schemas.user import UserSchema

from models.exports import (
    ProfileModel,
    StatusEnum
)

from schemas.exports import (
    ProfileSchema,
    ProfileStatusEnum,
    FilterSchema,
    ProfileUpdateSchema
)


class ProfileService:
    def __init__(self, target = None):
        self.repository = BaseRepository(ProfileModel)
    
    @postgres_transactional
    async def get_all( self )-> ProfileSchema:
        return await self.repository.get_all(FilterSchema())


    @postgres_transactional
    async def create(
        self, 
        data: ProfileSchema
    ):
        try:
            new_object: ProfileSchema = ProfileModel()
            self.repository.set_attrs(new_object, data.dict(exclude_unset=True))
        
            return await self.repository.save(new_object)
        except IntegrityError as e:
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
                detail="Erro ao registar Entidade.",
            ) from e

    @postgres_transactional
    async def update(
        self, 
        user_uuid:UUID,
        data: ProfileUpdateSchema
    ):
        try:
            profile: ProfileUpdateSchema = await profile_service.get_current_profile(user_uuid)
            self.repository.set_attrs(profile, data.dict(exclude_unset=True))
        
            return await self.repository.save(profile)
        except IntegrityError as e:
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
                detail="Erro ao registar Entidade.",
            ) from e
    

    @postgres_transactional
    async def get( self, uuid: UUID )-> ProfileSchema:
        return await self.repository.get(uuid)
    
    @postgres_transactional
    async def approve(self, uuid: UUID):
        try:
            profile: ProfileSchema = await self.repository.get( uuid )
            if profile:
                profile.status = ProfileStatusEnum.APROVADO.value                
                return await self.repository.save(profile)
            raise HTTPException(
                detail="Perfil não encontrado", 
                status_code=status.HTTP_404_NOT_FOUND
            )
        except IntegrityError as e:
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
                detail="Erro ao registar Entidade.",
            ) from e

    @postgres_transactional
    async def get_current_profile( self, user_uuid: UUID )-> ProfileSchema:
        filter = FilterSchema(
            filter_column = "user_uuid",
            filter_value = user_uuid
        )
        return await self.repository.get_one_by_filter(filter)
    
    @postgres_transactional
    async def upload_avatar(
        self, 
        profile_uuid: UUID,
        file: UploadFile
    ):
        try:
            profile: ProfileUpdateSchema = await self.repository.get(profile_uuid)
            data: ProfileUpdateSchema = ProfileUpdateSchema()

            data.avatar = await upload_avatar(file, 'sementes/avatars')
            self.repository.set_attrs(profile, data.dict(exclude_unset=True))
        
            return await self.repository.save(profile)
        except IntegrityError as e:
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
                detail="Erro ao registar Entidade.",
            ) from e
    



    async def updating_finances(
        self, 
        profile_uuid: UUID,
        current_user: UserSchema
    ):
    
        from services.transaction import transaction_service
        investments = await transaction_service.my_transactions(current_user.uuid)

        # profile = await self.repository.get(profile_uuid)
        # return profile
    
        if len(investments):
            approved_sum = sum(item.amount for item in investments if item.status == StatusEnum.APROVADO.value)

            return {
                "total": approved_sum,
                #"profile": profile
            }


profile_service = ProfileService()