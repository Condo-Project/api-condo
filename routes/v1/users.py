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
    UserCreate as UserSchemaCreate,
    UserChangePassword,

)

from services.exports import (
    user_service,
)

from common.pagination import (
    PaginatedResponse,
)

router = APIRouter()


# GET all user
@router.get("/")
async def get_all(
    current_user: UserSchema = Depends(get_current_user)
):
    """
    Return the all users
    """
    return await user_service.get_all()


# GET current user
@router.get("/current_user")
async def get_logged_user(
    current_user: UserSchema = Depends(get_current_user)
):
    """
    Return the current logged user
    """
    return await user_service.get_current_user(current_user)


# POST CREATE USER  
# @router.post("/", response_model=UserWithRoles, status_code=201)
@router.post("/", status_code=201)
async def create_user(
    user_data: UserSchemaCreate
):
    """
    CREATE USER

    * Required field:

        - name
        - password
    """
    return await user_service.create_user(user_data)

@router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends()
):
    """
    Login
    """

    return await user_service.login(form_data)
