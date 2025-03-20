
from uuid import UUID
from sqlalchemy.future import select
from sqlalchemy import column, FetchedValue, case, and_, distinct, func, text, extract, between, UUID as sqlalchemy_uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from db.decorators import postgres_db
from schemas.exports import (
    FilterSchema
)
from repositories.base import BaseRepository
from models.exports import (
    RoleModel,
    UserRoleModel,
    UserModel
)
from sqlalchemy import (
    column,
    String,
    Boolean
)


class UserRoleRepository(BaseRepository):
    def __init__(self):
        super().__init__(UserRoleModel)

    @postgres_db
    async def get_my_roles(self, user_uuid:UUID, db: AsyncSession):
        query = (
            select(
                self.model.user_uuid,  
                self.model.role_uuid,
                RoleModel.name,
            )
            .filter(
                self.model.is_active,
                self.model.user_uuid==user_uuid
            )
            .join(
                RoleModel,
                RoleModel.uuid == self.model.role_uuid,
            )
        )
        result = await db.execute(query)
        return result.mappings().all()

    @postgres_db
    async def get_users_by_role(self, role_uuid:UUID, db: AsyncSession):
        query = (
            select(
                self.model.user_uuid,  
                self.model.role_uuid,
                self.model.created_at,
                RoleModel.name.label("role_name"),
                UserModel.username,
            )
            .distinct()
            .filter(
                self.model.is_active,
                self.model.role_uuid==role_uuid
            )
            .join(
                RoleModel,
                RoleModel.uuid == self.model.role_uuid,
            )
            .join(
                UserModel,
                UserModel.uuid == self.model.user_uuid,
            )
        )
        result = await db.execute(query)
        return result.mappings().all()