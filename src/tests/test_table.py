import pytest
from httpx import AsyncClient
from fastapi import status


@pytest.mark.asyncio
async def test_create_table(client: AsyncClient):
    table_data = {
        "name": "Столик у окна",
        "seats": 4,
        "location": "Зал 1"
    }

    response = await client.post("/tables/create", json=table_data)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "id" in data
    assert data["name"] == "Столик у окна"


@pytest.mark.asyncio
async def test_get_all_tables(client: AsyncClient, test_table):
    response = await client.get("/tables/all_tables")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0


@pytest.mark.asyncio
async def test_delete_table(client: AsyncClient, test_table):

    response = await client.delete(f"/tables/delete/{test_table.id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT


    response = await client.get(f"/tables/{test_table.id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_delete_nonexistent_table(client: AsyncClient):

    response = await client.delete("/tables/delete/999999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "Table with id 999999 not found" in response.json()["detail"]