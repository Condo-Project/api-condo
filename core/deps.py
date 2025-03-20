"""
Deps: is the responsable to create singleton dependecy to be checked while requests
"""

# pylint: disable=C0103,R0903,E0611
from typing import Generator, List, Optional, Annotated
from uuid import UUID

from fastapi import Depends, HTTPException, Header, status
from fastapi.security import HTTPAuthorizationCredentials
from jose import jwt, JWTError

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from pydantic import BaseModel

from db.session import AsyncPostgreSession as Session
# from core.auth import oauth2_schema
from core.config import settings
from core.auth import verify_password
from models.user import UserModel
from core.auth import oauth2_schema
from exceptions.exports import (
    CREDENTIAL_EXCEPTION,
    INVALID_TOKEN_EXCEPTION,
    TOKEN_NOT_PROVIDED_EXCEPTION,
    DEACTIVATED_WALLET_EXCEPTION,
)
from services.exports import (
    user_service,
)


class TokenData(BaseModel):
    """
    ---
    """

    username: Optional[str] = None


async def get_session() -> Generator:
    """
    Get Session
    Return the session using singleton pattern
    """

    session: AsyncSession = Session()

    try:
        yield session
    finally:
        await session.close()


async def get_current_user(
    db: Session = Depends(get_session), token: str = Depends(oauth2_schema)
) -> UserModel:
    """
    Get Current User
    Return the current user logged
    """

    credential_exception: HTTPException = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível autenticar a credencial",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=settings.ALGORITHM,
            options={"verify_aud": False},
        )
        username: str = payload.get("sub")

        if username is None:
            raise credential_exception

        token_data: TokenData = TokenData(username=username)
    except JWTError as e:
        raise credential_exception from e

    async with db as session:
        query = select(UserModel).filter(UserModel.uuid == str(token_data.username))
        result = await session.execute(query)
        user: UserModel = result.scalars().unique().one_or_none()

        if user is None:
            raise credential_exception        
        return user



def validate_client(client_id: str = Header(...), client_secret: str = Header(...)):
    """
    Get client credentials
    Return validated_data if it's valid else return None
    """
    if settings.CLIENT_ID == client_id:
        if verify_password(client_secret, settings.HASHED_SECRET):
            return True
    raise CREDENTIAL_EXCEPTION

async def is_admin(current_user: Session = Depends(get_current_user)):
    """
    is Admin
    """
    if not current_user.is_staff:
       raise HTTPException(
           status_code=status.HTTP_403_FORBIDDEN,
           detail="Permissão negada. Acesso permitido apenas para Administrador.",
       )

    return current_user
