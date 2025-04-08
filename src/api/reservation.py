from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from src.models.table import Table
from src.schemas.reservation import ReservationCreate, ReservationResponse
from src.crud.reservation import crud_reservation
from src.database import get_db

router = APIRouter(prefix="/reservations", tags=["reservations"])


@router.post(
    "/",
    response_model=ReservationResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {"description": "Reservation successfully created"},
        400: {"description": "Time slot already booked"},
        404: {"description": "Table not found"}
    }
)
async def create_reservation(
    reservation_data: ReservationCreate,
    db: AsyncSession = Depends(get_db)
) -> ReservationResponse:  # Явное указание возвращаемого типа
    table = await db.get(Table, reservation_data.table_id)
    if not table:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Table not found"
        )

    reservation = await crud_reservation.create(db, create_schema=reservation_data)
    if not reservation:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This time slot is already booked"
        )

    return reservation


@router.get(
    "/",
    response_model=List[ReservationResponse],
    summary="Получить список всех бронирований"
)
async def read_reservations(
        skip: int = 0,
        limit: int = 100,
        db: AsyncSession = Depends(get_db)
):
    """
    Получить список бронирований с пагинацией.

    - **skip**: Сколько записей пропустить
    - **limit**: Максимальное количество записей (по умолчанию 100)
    """
    return await crud_reservation.get_all(db, skip=skip, limit=limit)


@router.get(
    "/{reservation_id}",
    response_model=ReservationResponse,
    responses={
        404: {"description": "Reservation not found"}
    }
)
async def read_reservation(
        reservation_id: int,
        db: AsyncSession = Depends(get_db)
):
    """
    Получить информацию о конкретном бронировании по ID.
    """
    reservation = await crud_reservation.get_by_id(db, id=reservation_id)
    if not reservation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Reservation with id {reservation_id} not found"
        )
    return reservation


@router.delete(
    "/{reservation_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        404: {"description": "Reservation not found"}
    }
)
async def delete_reservation(
        reservation_id: int,
        db: AsyncSession = Depends(get_db)
):
    """
    Удалить бронирование по ID.
    """
    success = await crud_reservation.delete(db, id=reservation_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Reservation with id {reservation_id} not found"
        )
    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content=None)


@router.get(
    "/table/{table_id}",
    response_model=List[ReservationResponse],
    summary="Получить бронирования для конкретного столика"
)
async def get_reservations_for_table(
        table_id: int,
        date: datetime | None = None,
        db: AsyncSession = Depends(get_db)
):
    """
    Получить все бронирования для указанного столика.

    - **table_id**: ID столика
    - **date**: Опциональная дата для фильтрации (формат YYYY-MM-DD)
    """
    reservations = await crud_reservation.get_by_table(db, table_id=table_id, date=date)
    return reservations

