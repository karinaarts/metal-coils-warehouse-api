import pytest
from fastapi import status


@pytest.mark.asyncio
async def test_coil_router_add_delete(client, sample_coil_data):
    response_coil_1 = await client.post("/api/coils/", json=sample_coil_data)
    coil_id = response_coil_1.json()["id"]
    assert response_coil_1.status_code == status.HTTP_201_CREATED
    assert response_coil_1.json()["id"] == 1, (
        f"id: {response_coil_1.json()['id']}"
    )
    assert response_coil_1.json()["length"] == 100.0
    assert response_coil_1.json()["weight"] == 500.0

    response_delete_coil_1 = await client.delete(f"/api/coils/{coil_id}")
    assert response_delete_coil_1.status_code == status.HTTP_200_OK
    assert response_delete_coil_1.json()["id"] == coil_id
    assert response_delete_coil_1.json()["deletion_date"] is not None

    response_get_coils = await client.get("/api/coils/")
    assert response_get_coils.status_code == status.HTTP_200_OK
    assert len(response_get_coils.json()) == 1
    assert response_get_coils.json()[0]["id"] == coil_id
    assert response_get_coils.json()[0]["deletion_date"] is not None


@pytest.mark.asyncio
async def test_coil_router_api_add(client, sample_coil_data):
    response_get_coils = await client.get("/api/coils/")
    assert response_get_coils.status_code == status.HTTP_200_OK
    assert len(response_get_coils.json()) == 0

    response_coil = await client.post("/api/coils/", json=sample_coil_data)
    coil_id = response_coil.json()["id"]
    assert response_coil.status_code == status.HTTP_201_CREATED
    assert response_coil.json()["id"] == 1, f"id: {response_coil.json()['id']}"
    assert response_coil.json()["length"] == 100.0
    assert response_coil.json()["weight"] == 500.0

    response_get_coils = await client.get("/api/coils/")
    assert response_get_coils.status_code == status.HTTP_200_OK
    assert len(response_get_coils.json()) == 1
    assert response_get_coils.json()[0]["id"] == coil_id


@pytest.mark.asyncio
async def test_coil_router_api_get_filtered(client):
    sample_coil_data_1 = {"length": 100.0, "weight": 500.0}
    sample_coil_data_2 = {"length": 150.0, "weight": 750.0}
    sample_coil_data_3 = {"length": 49.0, "weight": 1000.0}
    await client.post("/api/coils/", json=sample_coil_data_1)
    await client.post("/api/coils/", json=sample_coil_data_2)
    await client.post("/api/coils/", json=sample_coil_data_3)

    filter_params = {"length_min": 50.0, "weight_max": 1000.0}
    response_filtered_coils = await client.get(
        "/api/coils/filtered", params=filter_params
    )
    assert response_filtered_coils.status_code == status.HTTP_200_OK
    assert len(response_filtered_coils.json()) == 2
    assert response_filtered_coils.json()[0]["length"] == 100.0
    assert response_filtered_coils.json()[1]["length"] == 150.0


@pytest.mark.asyncio
async def test_add_coil_invalid_data(client):
    invalid_data = {"length": -10.0, "weight": 500.0}

    response_add_coil_invalid_data = await client.post(
        "/api/coils/", json=invalid_data
    )
    assert (
        response_add_coil_invalid_data.status_code
        == status.HTTP_422_UNPROCESSABLE_ENTITY
    )
