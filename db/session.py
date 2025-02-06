"""
Session
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings


# Configuração do SQLAlchemy para uso assíncrono (usado para endpoints)
postgres_async_engine = create_async_engine(settings.POSTGRES_URL)
AsyncPostgreSession = sessionmaker(
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
    class_=AsyncSession,
    bind=postgres_async_engine,
)

# Configuração do SQLAlchemy para uso síncrono (usado para tarefas)
postgres_sync_engine = create_engine(settings.POSTGRES_URL_SYNC)
SyncPostgreSession = sessionmaker(
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
    bind=postgres_sync_engine,
)
