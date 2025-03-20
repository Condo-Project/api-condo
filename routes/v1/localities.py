from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from core.deps import get_current_user
from services.exports import locality_service
from schemas.exports import LocalityCreate, LocalityResponse
from schemas.user import (
    UserSchema,
)

router = APIRouter(prefix="/localities", tags=["Localidades"])

@router.post("/", response_model=LocalityResponse)
async def create_locality_route(locality_data: LocalityCreate, 
        current_user: UserSchema = Depends(get_current_user)
    ):
    """
    Rota para criar um novo registro de Localidade respeitando a hierarquia.
    """
    return await locality_service.create_locality(locality_data, current_user)

@router.get("/", response_model=List[LocalityResponse])
async def list_locality_route(current_user: UserSchema = Depends(get_current_user)):
    """
    Rota para listar Localidades respeitando a hierarquia.
    """
    return await locality_service.get_all()
