import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport

from src.main import create_app
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from src.database import Base, engine

# Фикстура для асинхронной сессии базы данных
@pytest_asyncio.fixture
async def async_session() -> AsyncSession:
    session = sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    async with session() as s:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        yield s

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine.dispose()


@pytest_asyncio.fixture
async def client(async_session: AsyncSession):
    test_app = create_app()
    async with AsyncClient(transport=ASGITransport(app=test_app), base_url="http://0.0.0.0:8000") as client:
        yield client

