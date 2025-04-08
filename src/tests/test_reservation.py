import pytest
from datetime import datetime, timedelta, timezone
from fastapi import status


@pytest.mark.asyncio
async def test_create_reservation(client, test_table):
    future_time = datetime.now(timezone.utc) + timedelta(days=1)
    reservation_data = {
        "customer_name": "Test Customer",
        "table_id": test_table.id,
        "reservation_time": future_time.isoformat(),
        "duration_minutes": 60
    }

    response = await client.post("/reservations/", json=reservation_data)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["customer_name"] == "Test Customer"
    assert data["table_id"] == test_table.id


@pytest.mark.asyncio
async def test_get_reservation_not_found(client):
    response = await client.get("/reservations/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND


# import pytest
# from datetime import datetime, timedelta
# from fastapi import status
#
#
# @pytest.mark.asyncio
# async def test_create_reservation(client, test_table):
#     future_time = datetime.utcnow() + timedelta(days=1)
#     reservation_data = {
#         "customer_name": "Test Customer",
#         "table_id": test_table.id,
#         "reservation_time": future_time.isoformat(),
#         "duration_minutes": 60
#     }
#
#     response = client.post("/reservations/", json=reservation_data)
#     assert response.status_code == status.HTTP_201_CREATED
#     data = response.json()
#     assert data["customer_name"] == "Test Customer"
#     assert data["table_id"] == test_table.id
#
#
# @pytest.mark.asyncio
# async def test_create_reservation_conflict(client, test_table):
#     future_time = datetime.utcnow() + timedelta(days=1)
#     reservation_data = {
#         "customer_name": "Test Customer",
#         "table_id": test_table.id,
#         "reservation_time": future_time.isoformat(),
#         "duration_minutes": 60
#     }
#
#     # Первое бронирование - успешно
#     response1 = client.post("/reservations/", json=reservation_data)
#     assert response1.status_code == status.HTTP_201_CREATED
#
#     # Второе бронирование на то же время - конфликт
#     response2 = client.post("/reservations/", json=reservation_data)
#     assert response2.status_code == status.HTTP_400_BAD_REQUEST
#     assert "already booked" in response2.json()["detail"]
#
#
# @pytest.mark.asyncio
# async def test_get_reservation(client, test_table):
#     future_time = datetime.utcnow() + timedelta(days=1)
#     reservation_data = {
#         "customer_name": "Test Customer",
#         "table_id": test_table.id,
#         "reservation_time": future_time.isoformat(),
#         "duration_minutes": 60
#     }
#
#     create_response = client.post("/reservations/", json=reservation_data)
#     reservation_id = create_response.json()["id"]
#
#     get_response = client.get(f"/reservations/{reservation_id}")
#     assert get_response.status_code == status.HTTP_200_OK
#     assert get_response.json()["id"] == reservation_id
#
#
# @pytest.mark.asyncio
# async def test_get_reservation_not_found(client):
#     response = client.get("/reservations/999")
#     assert response.status_code == status.HTTP_404_NOT_FOUND
#
#
# @pytest.mark.asyncio
# async def test_delete_reservation(client, test_table):
#     future_time = datetime.utcnow() + timedelta(days=1)
#     reservation_data = {
#         "customer_name": "Test Customer",
#         "table_id": test_table.id,
#         "reservation_time": future_time.isoformat(),
#         "duration_minutes": 60
#     }
#
#     create_response = client.post("/reservations/", json=reservation_data)
#     reservation_id = create_response.json()["id"]
#
#     delete_response = client.delete(f"/reservations/{reservation_id}")
#     assert delete_response.status_code == status.HTTP_204_NO_CONTENT
#
#     get_response = client.get(f"/reservations/{reservation_id}")
#     assert get_response.status_code == status.HTTP_404_NOT_FOUND
#
#
# @pytest.mark.asyncio
# async def test_get_reservations_for_table(client, test_table):
#     future_time = datetime.utcnow() + timedelta(days=1)
#     reservation_data = {
#         "customer_name": "Test Customer",
#         "table_id": test_table.id,
#         "reservation_time": future_time.isoformat(),
#         "duration_minutes": 60
#     }
#
#     client.post("/reservations/", json=reservation_data)
#
#     response = client.get(f"/reservations/table/{test_table.id}")
#     assert response.status_code == status.HTTP_200_OK
#     assert len(response.json()) == 1