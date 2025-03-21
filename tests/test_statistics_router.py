from datetime import datetime, timedelta

import pytest
from fastapi import status


@pytest.mark.asyncio
async def test_get_statistics(client):
    response_get_coils = await client.get("/api/coils/")

    coil_data_1 = {"length": 100.0, "weight": 500.0}
    coil_data_2 = {"length": 150.0, "weight": 750.0}

    response1 = await client.post("/api/coils/", json=coil_data_1)
    response2 = await client.post("/api/coils/", json=coil_data_2)

    assert response1.status_code == status.HTTP_201_CREATED
    assert response2.status_code == status.HTTP_201_CREATED

    response_get_coils = await client.get("/api/coils/")
    assert response_get_coils.status_code == status.HTTP_200_OK
    assert len(response_get_coils.json()) == 2
    assert response_get_coils.json()[0]["id"] == response1.json()["id"]
    assert response_get_coils.json()[1]["id"] == response2.json()["id"]

    response = await client.get("/api/statistics/")

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["added_coils_count"] == 2
    assert response.json()["removed_coils_count"] == 0
    assert response.json()["avg_length"] == 125.0
    assert response.json()["avg_weight"] == 625.0
    assert response.json()["total_weight"] == 1250.0


@pytest.mark.asyncio
async def test_get_statistics_with_date_params(client):
    coil_data = {"length": 100.0, "weight": 500.0}

    response1 = await client.post("/api/coils/", json=coil_data)
    await client.post("/api/coils/", json=coil_data)

    coil_id = response1.json()["id"]
    await client.delete(f"/api/coils/{coil_id}")

    start_date = (
        datetime.now()
        .replace(hour=0, minute=0, second=0, microsecond=0)
        .isoformat()
    )
    end_date = (
        (datetime.now() + timedelta(days=1))
        .replace(hour=0, minute=0, second=0, microsecond=0)
        .isoformat()
    )

    response = await client.get(
        f"/api/statistics/?start_date={start_date}&end_date={end_date}"
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["added_coils_count"] == 2
    assert response.json()["removed_coils_count"] == 1


@pytest.mark.asyncio
async def test_get_statistics_empty_data(client):
    response = await client.get("/api/statistics/")

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["added_coils_count"] == 0
    assert response.json()["removed_coils_count"] == 0
    assert response.json()["total_weight"] == 0.0


@pytest.mark.asyncio
async def test_get_statistics_invalid_date_format(client):
    invalid_date = "2023/05/01"
    response = await client.get(f"/api/statistics/?start_date={invalid_date}")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
async def test_get_statistics_start_date_after_end_date(client):
    start_date = "2023-06-01T00:00:00"
    end_date = "2023-05-01T00:00:00"

    response = await client.get(
        f"/api/statistics/?start_date={start_date}&end_date={end_date}"
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Invalid date range" in response.json()["detail"]


@pytest.mark.asyncio
async def test_get_statistics_with_single_date(client):
    coil_data = {"length": 100.0, "weight": 500.0}
    response_create = await client.post("/api/coils/", json=coil_data)
    assert response_create.status_code == status.HTTP_201_CREATED

    start_date = (
        datetime.now()
        .replace(hour=0, minute=0, second=0, microsecond=0)
        .isoformat()
    )
    response_start = await client.get(
        f"/api/statistics/?start_date={start_date}"
    )
    assert response_start.status_code == status.HTTP_200_OK
    assert response_start.json()["added_coils_count"] == 1

    end_date = (
        (datetime.now() + timedelta(days=1))
        .replace(hour=0, minute=0, second=0, microsecond=0)
        .isoformat()
    )
    response_end = await client.get(f"/api/statistics/?end_date={end_date}")
    assert response_end.status_code == status.HTTP_200_OK
    assert response_end.json()["added_coils_count"] == 1
