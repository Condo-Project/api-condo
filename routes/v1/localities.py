from fastapi import Query, APIRouter, Depends, HTTPException
from typing import Optional, List
from sqlalchemy.orm import Session
from core.deps import get_current_user
from services.exports import locality_service
from schemas.exports import LocalityCreate, LocalityResponse, FilterSchema
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
async def list_locality_route(
    skip: int = Query(0, alias="page", ge=0),
    limit: int = Query(10, le=100),
    filter_column = Query(None, title="filter_column", description="Column to filter by"),
    # filter_column: Optional[InvoiceColumnEnum] = Query(None, title="filter_column", description="Column to filter by"),
    filter_value: str = Query(None, alias="filter_value", description="Value to filter by"),
    order_by: str = Query(None, alias="order_by", description="Field to order by, use '-' for descending order"),
    current_user: UserSchema = Depends(get_current_user)
):
    """
    ### Descrição:
    Rota para listar Localidades respeitando a hierarquia.

    ### Parâmetros:
    - **page** (`int`, padrão = 0): Número da página de resultados, usado para controle de paginação.
    - **limit** (`int`, padrão = 10, máximo = 100): Quantidade de itens por página.
    - **filter_column** (`Optional[InvoiceColumnEnum]`, opcional): Coluna pela qual deseja aplicar o filtro, como `date` ou `amount`.
    - **filter_value** (`str`, obrigatório se `filter_column` for usado): O valor a ser filtrado na coluna especificada.
    - **order_by** (`str`, opcional): Campo para ordenar os resultados. Para ordenar de forma decrescente, utilize o prefixo `-`, como `-amount`.
    - **db**: Sessão de banco de dados (injetada pelo FastAPI via `Depends`).
    - **current_wallet**: Objeto carteira corrente (injetado pelo FastAPI via `Depends`).
    """
    filter = FilterSchema(
        skip=skip,
        limit=limit,
        filter_column=filter_column,
        filter_value=filter_value,
        order_by=order_by
    )
    return await locality_service.get_all(filter)
