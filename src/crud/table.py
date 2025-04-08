from typing import TypeVar, Type

from pydantic import BaseModel
from sqlalchemy import select, delete
from sqlalchemy.dialects.mysql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase

from src.models.table import Table

ModelType = TypeVar("ModelType", bound=DeclarativeBase)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)


class CRUDTable:
    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def create(self,
             db: AsyncSession,
             *,
             create_schema: CreateSchemaType,
             commit: bool = True
    ) -> ModelType:
        data = create_schema.model_dump(exclude_unset=True)
        stmt = insert(self.model).values(**data).returning(self.model)
        res = await db.execute(stmt)
        obj = res.scalars().first()
        if commit:
            await db.commit()
            await db.refresh(obj)
        return obj

    async def get_all_tables(self,
            db: AsyncSession,
    ):
        statement = select(self.model)
        result = await db.execute(statement)
        return result.scalars().all()

    async def delete(
            self,
            db: AsyncSession,
            *,
            id: int,
            commit: bool = True
    ) -> bool:
        stmt = delete(self.model).where(self.model.id == id)
        result = await db.execute(stmt)

        if commit:
            await db.commit()

        # Возвращаем True если была удалена хотя бы одна запись
        return result.rowcount > 0


crud_table = CRUDTable(Table)
