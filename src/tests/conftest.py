import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta, timezone

from src.main import app
from src.database import Base, get_db
from src.models.table import Table
from src.models.reservation import Reservation

# Настройка тестовой базы
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

@pytest.fixture
async def engine():
    engine = create_async_engine(TEST_DATABASE_URL)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    await engine.dispose()

@pytest.fixture
async def db(engine):
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        yield session

@pytest.fixture
async def client(db):
    app.dependency_overrides[get_db] = lambda: db
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as client:
        yield client
    app.dependency_overrides.clear()

@pytest.fixture
async def test_table(db):
    table = Table(name="Столик 1", seats=4, location="Зал 1")
    db.add(table)
    await db.commit()
    await db.refresh(table)
    return table

@pytest.fixture
async def test_table1(db):
    table = Table(name="Тестовый столик", seats=4, location="Тестовый зал")
    db.add(table)
    await db.commit()
    await db.refresh(table)
    return table


@pytest.fixture
async def test_reservation(db, test_table):
    reservation_time = datetime.now(timezone.utc) + timedelta(hours=1)
    reservation = Reservation(
        customer_name="Тестовый Клиент",
        table_id=test_table.id,
        reservation_time=reservation_time,
        duration_minutes=90  # Просто число
    )
    db.add(reservation)
    await db.commit()
    await db.refresh(reservation)
    return reservation
