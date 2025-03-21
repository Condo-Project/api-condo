
from uuid import UUID
from sqlalchemy.future import select
from sqlalchemy import column, FetchedValue, case, and_, distinct, func, text, extract, between, UUID as sqlalchemy_uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, aliased
from db.decorators import postgres_db
from schemas.exports import (
    FilterSchema
)
from repositories.base import BaseRepository
from models.exports import (
    LocalityModel
)
from sqlalchemy import (
    column,
    String,
    Boolean,
    Enum
)


class LocalityRepository(BaseRepository):
    def __init__(self):
        super().__init__(LocalityModel)

    @postgres_db
    async def get_all(self, filter:FilterSchema, db: AsyncSession):

        order_clause = None
        if filter.order_by:
            column = getattr(self.model, filter.order_by[1:]) if filter.order_by.startswith('-') else getattr(self.model, filter.order_by)
            order_clause = column.desc() if filter.order_by.startswith('-') else column
        
        filter_clause = None
        if filter.filter_column and filter.filter_value:
            column = getattr(self.model, filter.filter_column, None)

            if column:
                if isinstance(column.type, Boolean):
                    filter_clause = column == bool(int(filter.filter_value))

                elif isinstance(column.type, Enum) or isinstance(column.type, sqlalchemy_uuid):
                    filter_clause = column == filter.filter_value
                else:
                    filter_clause = column.ilike(f"{filter.filter_value}%")
        
        filter_condition = and_(self.model.is_active)
        
        # Aplicando a condição de filtro apenas se necessário
        if filter_clause is not None:
            filter_condition = and_(filter_condition, filter_clause)

        # Criando um alias para evitar conflito de nomes
        parent_locality = aliased(LocalityModel)
        query = (
            select(
                self.model.name,
                self.model.uuid,
                self.model.locality_type,
                self.model.parent_uuid,
                parent_locality.name.label("parent_name")
            )
            .select_from(self.model)
            .filter(filter_condition)
            .join(
                parent_locality,  # Utilizando o alias
                parent_locality.uuid == self.model.parent_uuid,
            )
            .offset(filter.skip*filter.limit)
            .order_by(order_clause)
            .limit(filter.limit)
        )
        result = await db.execute(query)
        # print(result.mappings().all()[0])
        return result.mappings().all()