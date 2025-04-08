from fastapi import APIRouter, Depends, Query, status, HTTPException, Response

from sqlalchemy.ext.asyncio import AsyncSession

from src.crud.table import crud_table
from src.database import get_db
from src.models.table import Table
from src.schemas.table import TableCreate, TableResponse

router = APIRouter(prefix="/tables")


@router.post("/create", response_model=TableResponse)
async def create_table(
        table: TableCreate,
        db: AsyncSession = Depends(get_db)
):
    new_table = await crud_table.create(db=db, create_schema=table)
    return new_table


@router.get("/all_tables",response_model=list[TableResponse])
async def get_tables(
        db: AsyncSession = Depends(get_db)
):
    return await crud_table.get_all_tables(db)


@router.delete(
    "/delete/{table_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        204: {"description": "Table successfully deleted"},
        404: {"description": "Table not found"}
    }
)
async def delete_table(
        table_id: int,
        db: AsyncSession = Depends(get_db),
):

    table = await db.get(Table, table_id)
    if not table:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Table with id {table_id} not found"
        )


    success = await crud_table.delete(db=db, id=table_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete table"
        )

    return Response(status_code=status.HTTP_204_NO_CONTENT)