"""
Auth
"""

# pylint: disable=C0103,E0611
from typing import Optional
from datetime import datetime, timedelta
from pydantic import EmailStr, BaseModel
from pytz import timezone

from fastapi.security import OAuth2PasswordBearer, OAuth2AuthorizationCodeBearer, OAuth2PasswordRequestForm, OAuth2, HTTPBearer
from sqlalchemy import and_
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from jose import jwt
from common.utils import is_email

from models.user import UserModel
from core.config import settings
from core.security import verify_password
from db.decorators import postgres_db
from schemas.user import UserSchema

class TokenData(BaseModel):
    """
    ---
    """

    token: Optional[str] = None

oauth2_schema = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/users/login")
# oauth2_schema = HTTPBearer(description="WALLET Token")

@postgres_db
async def authentication(
    email: EmailStr or str, password: str, db: AsyncSession
) -> Optional[UserSchema]:
    """
    Authentication Function
    """

    async with db as session:
        query = select(UserModel).filter(
            and_(
                UserModel.is_active == True,
                UserModel.username == email
                # if is_email(email)
                # else 
                # UserModel.phone == email,
            )
        )
        result = await session.execute(query)
        usuario: UserSchema = result.scalar()

    if not usuario:
        return None

    if not verify_password(password, usuario.password):
        return None

    return usuario


def _create_token(token_type: str, time_to_live: timedelta, sub: str) -> str:
    payload = {}  # https://datatrucker.ietf.org/doc/html/rfc7519#section-4.1.3
    luanda = timezone("Africa/Luanda")
    expire = datetime.now(tz=luanda) + time_to_live

    payload["type"] = token_type
    payload["exp"] = expire
    payload["iat"] = datetime.now(tz=luanda)
    payload["sub"]: str = sub

    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def create_access(sub: str) -> str:
    """
    https://jwt.io
    """
    return _create_token(
        token_type="access_token",
        time_to_live=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        sub=sub,
    )
