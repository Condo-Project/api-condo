from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from core.deps import get_current_user
from services.exports import housing_service
from schemas.exports import (
    HousingCreate, 
    HousingResponse,
    CentralityCreate,
    CentralityResponse,
    BlockCreate,
    BlockResponse,
    BuildingCreate,
    BuildingResponse,
    FlatCreate,
    FlatResponse,
)
from schemas.user import (
    UserSchema,
)

router = APIRouter(prefix="/housing", tags=["Habitação"])

@router.post("/", response_model=HousingResponse)
async def create_housing_route(housing_data: HousingCreate, 
        current_user: UserSchema = Depends(get_current_user)
    ):
    """
    Rota para criar um novo registro de habitação respeitando a hierarquia.
    """
    return await housing_service.create_housing(housing_data, current_user)

@router.post(r"/create-centrality", response_model=CentralityResponse)
async def create_centrality(housing_data: CentralityCreate, 
        current_user: UserSchema = Depends(get_current_user)
    ):
    """
    Rota para criar um novo registro de centralidade respeitando a hierarquia.
    """
    return await housing_service.create_centrality(housing_data, current_user)

@router.post(r"/create-block", response_model=BlockResponse)
async def create_block(housing_data: BlockCreate, 
        current_user: UserSchema = Depends(get_current_user)
    ):
    """
    Rota para criar um novo registro de bloco respeitando a hierarquia.
    """
    return await housing_service.create_block(housing_data, current_user)

@router.post(r"/create-building", response_model=BuildingResponse)
async def create_building(housing_data: BuildingCreate, 
        current_user: UserSchema = Depends(get_current_user)
    ):
    """
    Rota para criar um novo registro de predio respeitando a hierarquia.
    """
    return await housing_service.create_building(housing_data, current_user)

@router.post(r"/create_flat", response_model=FlatResponse)
async def create_flat(housing_data: FlatCreate, 
        current_user: UserSchema = Depends(get_current_user)
    ):
    """
    Rota para criar um novo registro de apartamento respeitando a hierarquia.
    """
    return await housing_service.create_flat(housing_data, current_user)

@router.get("/", response_model=List[HousingResponse])
async def list_housing_route(current_user: UserSchema = Depends(get_current_user)):
    """
    Rota para listar habitações respeitando a hierarquia.
    """
    return await housing_service.get_all()

@router.get(r"/list-centralities", response_model=List[HousingResponse])
async def list_centralities(current_user: UserSchema = Depends(get_current_user)):
    """
    Rota para listar habitações respeitando a hierarquia.
    """
    return await housing_service.get_all_centralities()

@router.get(r"/list-blocks", response_model=List[HousingResponse])
async def list_blocks(current_user: UserSchema = Depends(get_current_user)):
    """
    Rota para listar habitações respeitando a hierarquia.
    """
    return await housing_service.get_all_blocks()

@router.get(r"/list-buildings", response_model=List[HousingResponse])
async def list_buildings(current_user: UserSchema = Depends(get_current_user)):
    """
    Rota para listar habitações respeitando a hierarquia.
    """
    return await housing_service.get_all_building()

@router.get(r"/list-flats", response_model=List[HousingResponse])
async def list_flats(current_user: UserSchema = Depends(get_current_user)):
    """
    Rota para listar habitações respeitando a hierarquia.
    """
    return await housing_service.get_all_flats()
