"""
---
"""

# pylint: disable=C0103,E0611,E0401
from fastapi import APIRouter
# from providers.exports import gb
from routes.v1 import (
    conexion,
    housing,
    localities,
    roles,
    users,
)

api_router_v1 = APIRouter()
api_router_v1.include_router(housing.router)
api_router_v1.include_router(localities.router)
api_router_v1.include_router(roles.router)
api_router_v1.include_router(conexion.router, tags=["ping"])
api_router_v1.include_router(users.router)
