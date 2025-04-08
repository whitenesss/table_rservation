from sqlalchemy import Integer, String
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base




class Table(AsyncAttrs, Base):
    __tablename__="tables"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=True)
    seats: Mapped[int] = mapped_column(Integer, nullable=True)
    location: Mapped[str] = mapped_column(String)



