"""
---
"""

# pylint: disable=C0103,E0401
from typing import List, Optional
from uuid import UUID
from datetime import date, datetime
from fastapi import APIRouter, status, Depends, HTTPException, Query  # , Response
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy import and_, distinct, func, text, extract, between
from sqlalchemy.ext.asyncio import session, AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload, joinedload, contains_eager, subqueryload
from sqlalchemy.exc import IntegrityError
from core.auth import authentication, create_access
from core.deps import get_session, get_current_user
from core.security import password_generator, verify_password
from core.hashing import Hasher
from models.user import UserModel
from schemas.user import (
    UserSchema,
    UserCreate as UserSchemaCreate
)

from core.deps import (
    get_current_user,
    is_admin,
)

from schemas.exports import (
    RoleSchema,
    UserRoleSchema,
    UserRoleMappingSchema
)

from services.exports import (
    role_service,
    user_role_service
)

from common.pagination import (
    PaginatedResponse,
)

router = APIRouter(prefix="/roles", tags=["Perfis"])


@router.post(
    "/", 
    status_code=201
)
async def create_user_role(
    data: UserRoleSchema,
    current_user: UserSchema = Depends(is_admin)
):
    """
    CREATE
    * Required field:
        - user_uuid
        - role_uuid
    """
    roles = await user_role_service.my_roles(data.user_uuid)

    #return roles
    any_role = [item for item in roles if item['role_uuid'] == data.role_uuid]

    if not any_role:
        return await user_role_service.create(data)
    raise HTTPException(
        detail="Já existe um nível de acesso associado", 
        status_code=status.HTTP_501_NOT_IMPLEMENTED
    )

@router.get(
    "/my-roles", 
    response_model=List[UserRoleMappingSchema]
)
async def get_my_roles(
    current_user: UserSchema = Depends(get_current_user)
):
    """
    Return My Roles
    """
    return await user_role_service.my_roles(current_user.uuid)


@router.get("/", response_model=List[RoleSchema])
async def get_all_roles(
    current_user: UserSchema = Depends(is_admin)):
    """
    Return All Roles
    """
    return await role_service.get_all()

