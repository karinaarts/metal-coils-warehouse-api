from fastapi import APIRouter, Depends, Query
from datetime import datetime, timedelta
from typing import Optional

from src.services.statistics_service import StatisticsService
from src.schemas.statistics_schema import (
    StatisticsPeriodSchema,
    StatisticsResponse,
)
from src.database import SessionDep

router = APIRouter(prefix="/statistics", tags=["statistics"])
service = StatisticsService()


async def get_statistics_period(
    start_date: Optional[datetime] = Query(
        default=datetime.now() - timedelta(days=30),
        description=(
            "Дата начала периода в формате timestamp "
            "(по умолчанию: 30 дней назад)"
        ),
    ),
    end_date: Optional[datetime] = Query(
        default=datetime.now(),
        description=(
            "Дата окончания периода в формате timestamp "
            "(по умолчанию: текущая дата)"
        ),
    ),
) -> StatisticsPeriodSchema:
    return StatisticsPeriodSchema(start_date=start_date, end_date=end_date)


@router.get("/", response_model=StatisticsResponse)
async def get_statistics(
    session: SessionDep,
    filter_params: StatisticsPeriodSchema = Depends(get_statistics_period),
):
    return await service.get_statistics(session, filter_params)
