import pytest
from unittest.mock import patch, AsyncMock
from fastapi.testclient import TestClient
from fastapi import status

from src.main import app


client = TestClient(app)


@pytest.mark.asyncio
async def test_add_coil(sample_coil_data, sample_coil_model):
    with patch(
        "src.api.coil_router.service.create", new_callable=AsyncMock
    ) as mock_create:
        mock_create.return_value = sample_coil_model
        mock_create.return_value = {
            "id": 1,
            "length": 100.0,
            "weight": 500.0,
            "creation_date": "2023-06-10T12:00:00",
            "deletion_date": None,
        }

        response = client.post("/api/coils/", json=sample_coil_data)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()["id"] == 1
        assert response.json()["length"] == 100.0
        assert response.json()["weight"] == 500.0


@pytest.mark.asyncio
async def test_delete_coil():
    coil_id = 1
    with patch(
        "src.services.coil_service.CoilService.delete", new_callable=AsyncMock
    ) as mock_delete:
        mock_delete.return_value.model_dump.return_value = {
            "id": coil_id,
            "length": 100.0,
            "weight": 500.0,
            "creation_date": "2023-06-10T12:00:00",
            "deletion_date": "2023-06-15T12:00:00",
        }

        response = client.delete(f"/api/coils/{coil_id}")

        assert response.status_code == status.HTTP_200_OK
        assert response.json()["id"] == coil_id
        assert response.json()["deletion_date"] is not None


@pytest.mark.asyncio
async def test_get_all_coils():
    with patch(
        "src.services.coil_service.CoilService.get_all", new_callable=AsyncMock
    ) as mock_get_all:
        mock_get_all.return_value = [
            {
                "id": 1,
                "length": 100.0,
                "weight": 500.0,
                "creation_date": "2023-06-10T12:00:00",
                "deletion_date": None,
            },
            {
                "id": 2,
                "length": 150.0,
                "weight": 750.0,
                "creation_date": "2023-06-05T12:00:00",
                "deletion_date": "2023-06-15T12:00:00",
            },
        ]

        response = client.get("/api/coils/")

        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) == 2


@pytest.mark.asyncio
async def test_get_filtered_coils():
    with patch(
        "src.services.coil_service.CoilService.get_filtered",
        new_callable=AsyncMock,
    ) as mock_get_filtered:
        mock_get_filtered.return_value = [
            {
                "id": 1,
                "length": 100.0,
                "weight": 500.0,
                "creation_date": "2023-06-10T12:00:00",
                "deletion_date": None,
            }
        ]

        filter_params = {"length_min": 50.0, "weight_max": 1000.0}

        response = client.get("/api/coils/filtered", params=filter_params)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) == 1
        assert response.json()[0]["length"] == 100.0


@pytest.mark.asyncio
async def test_add_coil_invalid_data():
    invalid_data = {"length": -10.0, "weight": 500.0}

    response = client.post("/api/coils/", json=invalid_data)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
