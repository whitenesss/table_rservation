import pytest
from datetime import datetime, timedelta, timezone
from httpx import AsyncClient
from fastapi import status


@pytest.mark.asyncio
async def test_create_reservation(client: AsyncClient, test_table):
    reservation_time = (datetime.now(timezone.utc) + timedelta(hours=1)).isoformat()
    reservation_data = {
        "customer_name": "Иван Иванов",
        "table_id": test_table.id,
        "reservation_time": reservation_time,
        "duration_minutes": 120
    }

    response = await client.post("/reservations/", json=reservation_data)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert "id" in data
    assert data["customer_name"] == "Иван Иванов"
    assert data["table_id"] == test_table.id


@pytest.mark.asyncio
async def test_create_conflicting_reservation(client: AsyncClient, test_reservation):
    conflict_time = (test_reservation.reservation_time + timedelta(minutes=30)).isoformat()
    reservation_data = {
        "customer_name": "Петр Петров",
        "table_id": test_reservation.table_id,
        "reservation_time": conflict_time,
        "duration_minutes": 60
    }

    response = await client.post("/reservations/", json=reservation_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "already booked" in response.json()["detail"]


@pytest.mark.asyncio
async def test_get_all_reservations(client: AsyncClient, test_reservation):
    response = await client.get("/reservations/")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0


@pytest.mark.asyncio
async def test_get_reservation_by_id(client: AsyncClient, test_reservation):
    response = await client.get(f"/reservations/{test_reservation.id}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == test_reservation.id


@pytest.mark.asyncio
async def test_delete_reservation(client: AsyncClient, test_reservation):

    response = await client.delete(f"/reservations/{test_reservation.id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT

    response = await client.get(f"/reservations/{test_reservation.id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_get_reservations_for_table(client: AsyncClient, test_reservation):
    response = await client.get(f"/reservations/table/{test_reservation.table_id}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    assert any(r["id"] == test_reservation.id for r in data)


@pytest.mark.asyncio
async def test_create_reservation_for_nonexistent_table(client: AsyncClient):
    reservation_data = {
        "customer_name": "Иван Иванов",
        "table_id": 9999,
        "reservation_time": (datetime.now(timezone.utc) + timedelta(hours=1)).isoformat(),
        "duration_minutes": 60
    }

    response = await client.post("/reservations/", json=reservation_data)
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_get_nonexistent_reservation(client: AsyncClient):
    response = await client.get("/reservations/9999")
    assert response.status_code == status.HTTP_404_NOT_FOUND


