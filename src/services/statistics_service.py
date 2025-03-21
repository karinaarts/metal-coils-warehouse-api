from src.database import SessionDep
from src.schemas.statistics_schema import (
    StatisticsPeriodSchema,
    StatisticsResponse,
)
from src.repositories.coil_repository import CoilRepository


class StatisticsService:
    def __init__(self):
        self.coil_repository = CoilRepository()

    async def get_statistics(
        self, session: SessionDep, filter_params: StatisticsPeriodSchema
    ) -> StatisticsResponse:
        statistics = await self.coil_repository.get_statistics(
            session, filter_params.start_date, filter_params.end_date
        )

        return StatisticsResponse(**statistics)
