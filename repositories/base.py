
from uuid import UUID
from sqlalchemy.future import select
from sqlalchemy import column, FetchedValue, and_, distinct, func, text, extract, between, UUID as sqlalchemy_uuid
from sqlalchemy.ext.asyncio import AsyncSession
from db.decorators import postgres_db
from schemas.exports import (
    FilterSchema
)

from sqlalchemy import (
    column,
    String,
    Boolean,
    Enum
)


class BaseRepository:
    def __init__(self, model):
        self.model = model

    @postgres_db
    async def get(self, uuid:UUID, db: AsyncSession):
        query = (
            select(self.model)
            .filter(
                self.model.is_active,
                self.model.uuid==uuid
            )
        )
        result = await db.execute(query)
        return result.scalar()

    @postgres_db
    async def find_all_by_saved_by(self, uuid:UUID, db: AsyncSession):
        query = (
            select(self.model)
            .filter(
                self.model.is_active,
                self.model.saved_by==uuid
            )
        )
        result = await db.execute(query)
        return result.scalars().unique().all()

    @postgres_db
    async def get_one_by_filter(self, filter:FilterSchema, db: AsyncSession):

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

                elif isinstance(column.type, sqlalchemy_uuid):
                    filter_clause = column == filter.filter_value
                else:
                    filter_clause = column.ilike(f"{filter.filter_value}%")
        
        filter_condition = and_(self.model.is_active)
        
        # Aplicando a condição de filtro apenas se necessário
        if filter_clause is not None:
            filter_condition = and_(filter_condition, filter_clause)
        query = (
            select(self.model)
            .filter(filter_condition)
            .offset(filter.skip*filter.limit)
            .order_by(order_clause)
            .limit(filter.limit)
        )
        result = await db.execute(query)
        return result.scalar()

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
        query = (
            select(self.model)
            .filter(filter_condition)
            .offset(filter.skip*filter.limit)
            .order_by(order_clause)
            .limit(filter.limit)
        )
        result = await db.execute(query)
        return result.scalars().all()
    

    @postgres_db
    async def get_all_include_deleted(self, filter:FilterSchema, db: AsyncSession):

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
                else:
                    filter_clause = column.ilike(f"{filter.filter_value}%")
        
        filter_condition = and_(True)
        
        # Aplicando a condição de filtro apenas se necessário
        if filter_clause is not None:
            filter_condition = and_(filter_condition, filter_clause)
        query = (
            select(self.model)
            .filter(filter_condition)
            .offset(filter.skip*filter.limit)
            .order_by(order_clause)
            .limit(filter.limit)
        )
        result = await db.execute(query)
        return result.scalars().all()
    
    def set_attrs(self, entity, updated_attrs, 
    throw_error_if_data_type_not_same:bool = True, 
    throw_error_if_attr_not_in_entity:bool = True):

        # simple one
        for attr in updated_attrs:
            has_attr = hasattr(entity, attr)
            if has_attr:
                setattr(entity, attr, updated_attrs[attr])

        # complex one
        # attrs = []
        # for attr in updated_attrs:
        #     has_attr = hasattr(entity, attr)
        #     if has_attr:
        #         expected_type = type(getattr(entity, attr))
        #         inputed_type = type(updated_attrs[attr])
        #         is_same_type =  inputed_type == expected_type
        #         if is_same_type:
        #             attrs.append(attr)
        #         else:
        #             if throw_error_if_data_type_not_same:
        #                 raise TypeError(f"The expected value type of attr \
        #                 '{attr}' is '{expected_type}' of entity, \
        #                 where inputted value type is '{inputed_type}'.")
        #     else:
        #         if throw_error_if_attr_not_in_entity:
        #             raise TypeError(f"attr '{attr}' is not found in entity.")
                  
        # for attr in attrs:
        #     setattr(entity, attr, updated_attrs[attr])   
        # return entity

    @postgres_db
    async def save(self, db_obj, db:AsyncSession):
        # db_obj = self.model(**obj_in.dict())
        if db_obj.uuid:
            await db.merge(db_obj)
        else:
            db.add(db_obj)
        # await db.commit()
        await db.flush()
        await db.refresh(db_obj)
        return db_obj
    
    @postgres_db
    async def save_all(self, db_obj, db:AsyncSession):
        db.add_all(db_obj)
        await db.flush()
        return db_obj