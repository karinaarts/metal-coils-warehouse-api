import pytest
from unittest.mock import patch, AsyncMock
from fastapi.testclient import TestClient
from fastapi import status, HTTPException
from datetime import datetime

from src.main import app


client = TestClient(app)


@pytest.mark.asyncio
async def test_get_statistics(sample_statistics_data):
    with patch(
        "src.services.statistics_service.StatisticsService.get_statistics",
        new_callable=AsyncMock,
    ) as mock_get_stats:
        stats_json = sample_statistics_data.copy()
        for key in [
            "min_coils_date",
            "max_coils_date",
            "min_weight_date",
            "max_weight_date",
        ]:
            if stats_json.get(key):
                if isinstance(stats_json[key], datetime):
                    stats_json[key] = stats_json[key].date()
                stats_json[key] = (
                    stats_json[key].isoformat()
                    if hasattr(stats_json[key], "isoformat")
                    else stats_json[key]
                )

        mock_get_stats.return_value = stats_json

        response = client.get("/api/statistics/")

        assert response.status_code == status.HTTP_200_OK
        assert (
            response.json()["added_coils_count"]
            == sample_statistics_data["added_coils_count"]
        )
        assert (
            response.json()["min_coils_count"]
            == sample_statistics_data["min_coils_count"]
        )
        assert (
            response.json()["max_coils_count"]
            == sample_statistics_data["max_coils_count"]
        )


@pytest.mark.asyncio
async def test_get_statistics_with_date_params():
    start_date = "2023-05-01T00:00:00"
    end_date = "2023-06-01T00:00:00"

    with patch(
        "src.services.statistics_service.StatisticsService.get_statistics",
        new_callable=AsyncMock,
    ) as mock_get_stats:
        mock_get_stats.return_value = {
            "added_coils_count": 5,
            "removed_coils_count": 2,
            "avg_length": 100.0,
            "avg_weight": 500.0,
            "min_length": 80.0,
            "max_length": 120.0,
            "min_weight": 400.0,
            "max_weight": 600.0,
            "total_weight": 2500.0,
            "min_storage_time": 3600.0,
            "max_storage_time": 86400.0,
            "min_coils_date": "2023-05-02",
            "min_coils_count": 10,
            "max_coils_date": "2023-05-25",
            "max_coils_count": 20,
            "min_weight_date": "2023-05-03",
            "min_weight_total": 400.0,
            "max_weight_date": "2023-05-20",
            "max_weight_total": 600.0,
        }

        response = client.get(
            f"/api/statistics/?start_date={start_date}&end_date={end_date}"
        )

        assert response.status_code == status.HTTP_200_OK
        mock_get_stats.assert_called_once()


@pytest.mark.asyncio
async def test_get_statistics_empty_data():
    with patch(
        "src.services.statistics_service.StatisticsService.get_statistics",
        new_callable=AsyncMock,
    ) as mock_get_stats:
        mock_get_stats.return_value = {
            "added_coils_count": 0,
            "removed_coils_count": 0,
            "avg_length": 0.0,
            "avg_weight": 0.0,
            "min_length": 0.0,
            "max_length": 0.0,
            "min_weight": 0.0,
            "max_weight": 0.0,
            "total_weight": 0.0,
            "min_storage_time": 0.0,
            "max_storage_time": 0.0,
            "min_coils_date": None,
            "max_coils_date": None,
            "min_weight_date": None,
            "max_weight_date": None,
            "min_coils_count": None,
            "max_coils_count": None,
            "min_weight_total": None,
            "max_weight_total": None,
        }

        response = client.get("/api/statistics/")

        assert response.status_code == status.HTTP_200_OK
        assert response.json()["added_coils_count"] == 0
        assert response.json()["removed_coils_count"] == 0


@pytest.mark.asyncio
async def test_get_statistics_invalid_date_format():
    invalid_date = "2023/05/01"

    response = client.get(f"/api/statistics/?start_date={invalid_date}")

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
async def test_get_statistics_start_date_after_end_date():
    start_date = "2023-06-01T00:00:00"
    end_date = "2023-05-01T00:00:00"

    with patch(
        "src.services.statistics_service.StatisticsService.get_statistics",
        new_callable=AsyncMock,
    ) as mock_get_stats:
        mock_get_stats.side_effect = HTTPException(
            status_code=400,
            detail="Invalid date range: start date is after end date",
        )

        response = client.get(
            f"/api/statistics/?start_date={start_date}&end_date={end_date}"
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Invalid date range" in response.json()["detail"]


@pytest.mark.asyncio
async def test_get_statistics_only_start_date():
    start_date = "2023-05-01T00:00:00"

    with patch(
        "src.services.statistics_service.StatisticsService.get_statistics",
        new_callable=AsyncMock,
    ) as mock_get_stats:
        mock_get_stats.return_value = {
            "added_coils_count": 10,
            "removed_coils_count": 5,
            "avg_length": 100.0,
            "avg_weight": 500.0,
            "min_length": 80.0,
            "max_length": 120.0,
            "min_weight": 400.0,
            "max_weight": 600.0,
            "total_weight": 5000.0,
            "min_storage_time": 3600.0,
            "max_storage_time": 86400.0,
            "min_coils_date": "2023-05-01",
            "max_coils_date": "2023-12-31",
            "min_weight_date": "2023-05-01",
            "max_weight_date": "2023-12-31",
        }

        response = client.get(f"/api/statistics/?start_date={start_date}")

        assert response.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_get_statistics_only_end_date():
    end_date = "2023-05-01T00:00:00"

    with patch(
        "src.services.statistics_service.StatisticsService.get_statistics",
        new_callable=AsyncMock,
    ) as mock_get_stats:
        mock_get_stats.return_value = {
            "added_coils_count": 10,
            "removed_coils_count": 5,
            "avg_length": 100.0,
            "avg_weight": 500.0,
            "min_length": 80.0,
            "max_length": 120.0,
            "min_weight": 400.0,
            "max_weight": 600.0,
            "total_weight": 5000.0,
            "min_storage_time": 3600.0,
            "max_storage_time": 86400.0,
            "min_coils_date": "2023-05-01",
            "max_coils_date": "2023-12-31",
            "min_weight_date": "2023-05-01",
            "max_weight_date": "2023-12-31",
        }

        response = client.get(f"/api/statistics/?end_date={end_date}")

        assert response.status_code == status.HTTP_200_OK
