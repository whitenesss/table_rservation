from typing import TypeVar, Type, Optional, Any
from datetime import datetime, timedelta, timezone
from datetime import datetime, timedelta

from sqlalchemy.sql.expression import cast
from pydantic import BaseModel
from sqlalchemy import select, delete, and_, func, DateTime, Integer, text

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase

from src.models.reservation import Reservation
from src.models.table import Table

ModelType = TypeVar("ModelType", bound=DeclarativeBase)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)


class CRUDReservation:
    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def has_conflict(
            self,
            db: AsyncSession,
            *,
            table_id: int,
            reservation_time: datetime,
            duration_minutes: int,
            reservation_id: int | None = None
    ) -> bool:

        if reservation_time.tzinfo is None:
            reservation_time = reservation_time.replace(tzinfo=timezone.utc)

        end_time = reservation_time + timedelta(minutes=duration_minutes)
        stmt = select(self.model).where(
            and_(
                self.model.table_id == table_id,
                self.model.reservation_time < end_time,
                self.model.reservation_time > reservation_time - timedelta(minutes=duration_minutes)
            )
        )

        if reservation_id is not None:
            stmt = stmt.where(self.model.id != reservation_id)

        result = await db.execute(stmt)
        return result.scalars().first() is not None

    async def create(
            self,
            db: AsyncSession,
            *,
            create_schema,
            commit: bool = True
    ):
        data = create_schema.model_dump(exclude_unset=True)


        if await self.has_conflict(
                db,
                table_id=data['table_id'],
                reservation_time=data['reservation_time'],
                duration_minutes=data['duration_minutes']
        ):
            return None


        db_obj = self.model(**data)
        db.add(db_obj)

        if commit:
            try:
                await db.commit()
                await db.refresh(db_obj)
            except Exception:
                await db.rollback()
                raise

        return db_obj
    async def get_all(
            self,
            db: AsyncSession,
            *,
            skip: int = 0,
            limit: int = 100
    ) -> list[ModelType]:
        statement = select(self.model).offset(skip).limit(limit)
        result = await db.execute(statement)
        return result.scalars().all()

    async def get_by_id(
            self,
            db: AsyncSession,
            *,
            id: int
    ) -> Optional[ModelType]:
        statement = select(self.model).where(self.model.id == id)
        result = await db.execute(statement)
        return result.scalars().first()

    async def delete(
            self,
            db: AsyncSession,
            *,
            id: int,
            commit: bool = True
    ) -> bool:
        stmt = delete(self.model).where(self.model.id == id)
        await db.execute(stmt)
        if commit:
            await db.commit()
        return True

    async def get_by_table(
            self,
            db: AsyncSession,
            *,
            table_id: int,
            date: datetime | None = None,
            skip: int = 0,
            limit: int = 100
    ) -> list[ModelType]:

        stmt = select(self.model).where(self.model.table_id == table_id)

        if date:
            stmt = stmt.where(
                func.date(self.model.reservation_time) == date.date()
            )

        stmt = stmt.offset(skip).limit(limit)
        result = await db.execute(stmt)
        return result.scalars().all()



crud_reservation = CRUDReservation(Reservation)