from datetime import datetime, timedelta

from fastapi import APIRouter, Query

from src.services.statistics_service import StatisticsService
from src.schemas.statistics_schema import (
    StatisticsPeriodSchema,
    StatisticsResponse,
)
from src.database import SessionDep

router = APIRouter(prefix="/statistics", tags=["statistics"])
service = StatisticsService()


@router.get("/", response_model=StatisticsResponse)
async def get_statistics(
    session: SessionDep,
    start_date: datetime = Query(
        default_factory=lambda: (datetime.now() - timedelta(days=30)),
        description=("Start date in timestamp format (default: 30 days ago)"),
    ),
    end_date: datetime = Query(
        default_factory=lambda: datetime.now(),
        description=("End date in timestamp format (default: current date)"),
    ),
):
    filter_params = StatisticsPeriodSchema(
        start_date=start_date, end_date=end_date
    )
    return await service.get_statistics(session, filter_params)
