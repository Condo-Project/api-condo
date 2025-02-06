
from uuid import UUID
from typing import List
from fastapi import status
from decimal import Decimal
from datetime import datetime, date
from sqlalchemy.ext.asyncio import AsyncSession

from db.decorators import postgres_transactional
from core.config import settings

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

# from services.token_service import token_service
# from core.hashing import Hasher
# from exceptions.exports import (
#     DEACTIVATED_STORE_EXCEPTION,
#     STORE_NO_CONTENT_EXCEPTION,
#     STORE_NOT_FOUND_EXCEPTION
# )
# EXTERNAL_AGENTS = 'AGENTES_EXTERNOS'
# PAYMENT_BY_EXTERNAL_AGENT = 'PAYMENT_BY_EXTERNAL_AGENT'
# ELECTRONIC_PAYMENT = 'ELECTRONIC_PAYMENT'

class StartUpService:
    def __init__(self, target = None):
        self.role_repository = BaseRepository(RoleModel)
    
    @postgres_transactional
    async def create_role(self):
        # base_roles = {"Agricultor", "Investidor", "Administrador"}
        roles = {"Agricultor", "Investidor", "Administrador"}.difference({role.name for role in await self.role_repository.get_all_include_deleted(FilterSchema())})
        new_roles:List[RoleModel] = [
            RoleModel(
                name=role_name,
                description=role_name
            ) for role_name in roles
        ]
        if new_roles:
            print("Criando as Roles...")
            await self.role_repository.save_all(new_roles)
            print("Roles criadas com sucesso.")

startup_service = StartUpService()