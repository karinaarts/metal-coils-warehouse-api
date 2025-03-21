import pytest
from datetime import datetime, timedelta
from fastapi import HTTPException

from src.schemas.statistics_schema import StatisticsPeriodSchema


@pytest.mark.asyncio
async def test_get_statistics(
    statistics_service, mock_session, sample_statistics_data
):
    start_date = datetime.now() - timedelta(days=30)
    end_date = datetime.now()
    period = StatisticsPeriodSchema(start_date=start_date, end_date=end_date)

    statistics_service.coil_repository.get_statistics.return_value = (
        sample_statistics_data
    )

    result = await statistics_service.get_statistics(mock_session, period)

    statistics_service.coil_repository.get_statistics.assert_called_once_with(
        mock_session, start_date, end_date
    )
    assert (
        result.added_coils_count == sample_statistics_data["added_coils_count"]
    )
    assert (
        result.removed_coils_count
        == sample_statistics_data["removed_coils_count"]
    )
    assert result.avg_length == sample_statistics_data["avg_length"]
    assert result.avg_weight == sample_statistics_data["avg_weight"]
    assert result.total_weight == sample_statistics_data["total_weight"]
    assert result.min_coils_date == sample_statistics_data["min_coils_date"]
    assert result.max_coils_date == sample_statistics_data["max_coils_date"]


@pytest.mark.asyncio
async def test_get_statistics_empty_result(statistics_service, mock_session):
    start_date = datetime.now() - timedelta(days=30)
    end_date = datetime.now()
    period = StatisticsPeriodSchema(start_date=start_date, end_date=end_date)

    statistics_service.coil_repository.get_statistics.return_value = None

    result = await statistics_service.get_statistics(mock_session, period)

    assert result.added_coils_count == 0
    assert result.removed_coils_count == 0
    assert result.avg_length == 0
    assert result.avg_weight == 0


@pytest.mark.asyncio
async def test_statistics_invalid_date_range(statistics_service, mock_session):
    start_date = datetime.now()
    end_date = datetime.now() - timedelta(days=30)
    period = StatisticsPeriodSchema(start_date=start_date, end_date=end_date)

    with pytest.raises(HTTPException) as exc_info:
        await statistics_service.get_statistics(mock_session, period)

    assert exc_info.value.status_code == 400
    assert "date range" in exc_info.value.detail.lower()
