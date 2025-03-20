
from uuid import UUID
from typing import List

from fastapi import status, HTTPException
from sqlalchemy.exc import IntegrityError

from db.decorators import postgres_transactional

from repositories.exports import (
    UserRoleRepository,
    BaseRepository
)

from models.exports import (
    UserRoleModel,
    RoleModel
)
from schemas.exports import (
    UserRoleSchema,
    FilterSchema,
    RoleSchema,
)

from services.role import role_service

class BaseUserRoleService:
    def __init__(self, model):
        self.model = model


class UserRoleService:
    def __init__(self, target = None):
        self.repository = UserRoleRepository()
        self.role_repository = BaseRepository(RoleModel)

    @postgres_transactional
    async def create(self, data: UserRoleSchema):
        try:
            new_object: UserRoleSchema = UserRoleModel()
            self.repository.set_attrs(new_object, data.dict(exclude_unset=True))
            return await self.repository.save(new_object)
        except IntegrityError as e:
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
                detail="Erro ao registar Entidade.",
            ) from e
    
    @postgres_transactional
    async def get_role( self, uuid: UUID )-> UserRoleSchema:
        """
        Get Role
        """
        return await self.repository.get(uuid)
    
    @postgres_transactional
    async def get_residents( self )-> UserRoleSchema:
        """
        Get All Residents
        """
        filter:FilterSchema = FilterSchema(
            filter_column="name",
            filter_value="Morador"
        )
        role: RoleSchema = await self.role_repository.get_one_by_filter(filter)
        if not role:
            return []
        return await self.repository.get_users_by_role(role.uuid)

    @postgres_transactional
    async def my_roles(
        self, 
        user_uuid: UUID
    ):

        return await self.repository.get_my_roles(user_uuid)


user_role_service = UserRoleService()   