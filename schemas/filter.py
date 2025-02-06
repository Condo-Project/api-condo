"""
Wallet Schemas
"""

# pylint: disable=R0903,W0107,E0611,E0401
from typing import Optional, Any, Generic, TypeVar, Union
from uuid import UUID
from enum import Enum
from fastapi import Query
from decimal import Decimal
from pydantic import BaseModel, Field, PositiveInt
from datetime import datetime
from pydantic.generics import GenericModel
# from app.schemas.applications import ApplicationSchema

F = TypeVar('F')
class QueryParams(BaseModel, Generic[F]):
    limit: Optional[int] = Query(10, title="Limit", description="Maximum number of records to return")
    filter_value: Optional[str] = Query(None, title="Filter Value", description="Value to filter by")
    order_by: Optional[str] = Query("asc", title="Order By", description="Order results by (asc/desc)", enum=["asc", "desc"])

    # skip: PositiveInt = Field(Query(0, alias="page"))
    # limit: PositiveInt = Field(Query(10))
    # filter_value: str = Query(None, alias="filter_value", description="Value to filter by")
    # filter_column: F = Field(Query(None, alias="filter_column", description="Column to filter by"))
    # order_by: str = Field(Query(None, alias="order_by", description="Field to order by, use '-' for descending order"))

class FilterSchema(BaseModel):
    """
    Wallet JSON Schema
    """

    skip: int = 0
    limit: int = 10
    filter_value: Union[str, UUID] = None 
    filter_column: str = None
    order_by: str = None

class InvoiceColumnEnum(str, Enum):
    INVOICE_ID = "id"
    ACCOUNT_ID = "conta_id"
    CUSTOMER_ID = "cliente_id"
    CONTRACT_ID = "contrato_id"
    INVOICE_ACRONYM = "factura_sigla"

class InvoiceUniqueColumnEnum(str, Enum):
    INVOICE_ID = "id"
    INVOICE_ACRONYM = "factura_sigla"

class ReceiptColumnEnum(str, Enum):
    OPTION_ONE = "option_one"
    OPTION_TWO = "option_two"

class WalletColumnEnum(str, Enum):
    NAME = "name"
    CODE = "code"
    HAS_CREDIT = "has_credit"
    CUSTOMER_ID = "customer_id"
    SALE_BOX_ID = "sale_box_id"
    WALLET_NUMBER = "wallet_number"

class CustomerColumnEnum(str, Enum):
    CUSTOMER_ID = "id"
    PHONE_NUMBER = "telefone"
    EMAIL = "email"
    # NAME = "nome"
    CUSTOMER_NUMBER = "numero_cliente"
    IDENTIFICATION_NUMBER = "numero_identificacao"