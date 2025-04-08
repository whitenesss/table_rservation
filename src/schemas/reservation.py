from datetime import datetime, timezone
from pydantic import BaseModel, Field, ConfigDict, field_validator
from typing import Optional
from enum import Enum

class ReservationStatus(str, Enum):
    ACTIVE = "active"
    CANCELLED = "cancelled"
    COMPLETED = "completed"

class ReservationBase(BaseModel):
    customer_name: str = Field(..., min_length=1, max_length=100, json_schema_extra={"example": "Иван Иванов"})
    table_id: int = Field(..., gt=0, json_schema_extra={"example": 1})
    reservation_time: datetime = Field(..., json_schema_extra={"example": "2023-07-20T14:00:00Z"})
    duration_minutes: int = Field(..., gt=0, le=240, json_schema_extra={"example": 90})

    @field_validator('reservation_time', mode='before')
    def validate_reservation_time(cls, v):
        if isinstance(v, str):
            v = datetime.fromisoformat(v)
        if v.tzinfo is None:
            v = v.replace(tzinfo=timezone.utc)
        now = datetime.now(timezone.utc)
        if v < now:
            raise ValueError("Reservation time cannot be in the past")
        return v

class ReservationCreate(ReservationBase):
    pass

class ReservationInDBBase(ReservationBase):
    id: int
    status: ReservationStatus = Field(default=ReservationStatus.ACTIVE)
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
        json_encoders={
            datetime: lambda v: v.isoformat()
        }
    )

class ReservationResponse(ReservationInDBBase):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": 1,
                "customer_name": "Иван Иванов",
                "table_id": 1,
                "reservation_time": "2023-07-20T14:00:00Z",
                "duration_minutes": 90,
                "status": "active",
                "created_at": "2023-07-15T10:00:00Z",
                "updated_at": "2023-07-15T10:00:00Z"
            }
        }
    )