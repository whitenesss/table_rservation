from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class TableBase(BaseModel):
    """Базовая схема столика с основными атрибутами"""
    name: str = Field(
        ...,
        min_length=2,
        max_length=50,
        description="Название столика",
        examples=["Table 1", "Барная стойка 2"]
    )
    seats: int = Field(
        ...,
        gt=0,
        le=12,
        description="Количество мест",
        examples=[2, 4, 6]
    )
    location: Optional[str] = Field(
        default=None,
        max_length=100,
        description="Расположение в ресторане",
        examples=["У окна", "Терраса", "VIP-зона"]
    )


class TableCreate(TableBase):
    """Схема для создания столика (наследует все поля TableBase)"""
    pass


class TableResponse(TableBase):
    """Схема для возврата данных о столике (с ID)"""
    id: int = Field(..., description="Уникальный идентификатор столика")


    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "name": "VIP Booth",
                "seats": 4,
                "location": "Зал с панорамным видом"
            }
        }
    )