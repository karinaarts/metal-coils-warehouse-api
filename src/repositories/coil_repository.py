from datetime import datetime, timezone, date, timedelta
from typing import List, Any, Dict, Optional
from fastapi import HTTPException
from sqlalchemy import select, func
from sqlalchemy.sql.expression import Select
from src.models.coil_model import CoilModel
from src.repositories.base import BaseRepository
from src.database import SessionDep


class CoilRepository(BaseRepository[CoilModel]):
    def __init__(self):
        super().__init__(CoilModel)

    async def delete(self, session: SessionDep, id: int) -> CoilModel:
        model = await session.get(self.model, id)
        if not model:
            raise HTTPException(status_code=404, detail="Катушка не найдена")
            
        model.deletion_date = datetime.now(timezone.utc)
        await session.commit()
        return model

    async def get_filtered(
        self, session: SessionDep, data: dict
    ) -> List[CoilModel]:
        query = select(self.model)
        query = self._apply_id_filters(query, data)
        query = self._apply_dimension_filters(query, data)
        query = self._apply_creation_date_filters(query, data)
        query = self._apply_deletion_date_filters(query, data)

        result = await session.execute(query)
        return list(result.scalars().all())

    async def get_statistics(
        self,
        session: SessionDep,
        start_date: datetime,
        end_date: datetime,
    ) -> Optional[Dict[str, Any]]:
        query = select(self.model)
        query = self._apply_period_filters(query, start_date, end_date)

        check_query = select(func.count()).select_from(query.subquery())
        result = await session.execute(check_query)
        count = result.scalar() or 0

        if count == 0:
            return None

        count_stats = await self._calculate_count_statistics(session, query)
        size_stats = await self._calculate_size_statistics(session, query)
        storage_time_stats = await self._calculate_storage_time_statistics(
            session, query
        )

        daily_stats = await self._get_statistics_by_day(
            session, start_date, end_date
        )

        return {
            **count_stats,
            **size_stats,
            **storage_time_stats,
            **daily_stats,
        }

    def _apply_range_filter(
        self, query: Select, data: dict, field_name: str, model_field: Any
    ) -> Select:
        min_key = f"{field_name}_min"
        max_key = f"{field_name}_max"

        if data.get(min_key):
            query = query.where(model_field >= data[min_key])
        if data.get(max_key):
            query = query.where(model_field <= data[max_key])
        return query

    def _apply_id_filters(self, query: Select, data: dict) -> Select:
        query = self._apply_range_filter(query, data, "id", self.model.id)
        return query

    def _apply_dimension_filters(self, query: Select, data: dict) -> Select:
        query = self._apply_range_filter(
            query, data, "length", self.model.length
        )
        query = self._apply_range_filter(
            query, data, "weight", self.model.weight
        )
        return query

    def _apply_creation_date_filters(
        self, query: Select, data: dict
    ) -> Select:
        query = self._apply_range_filter(
            query, data, "creation_date", self.model.creation_date
        )
        return query

    def _apply_deletion_date_filters(
        self, query: Select, data: dict
    ) -> Select:
        if data.get("deletion_date_min"):
            query = query.where(
                self.model.deletion_date.is_not(None),
                self.model.deletion_date >= data["deletion_date_min"],
            )
        if data.get("deletion_date_max"):
            query = query.where(
                self.model.deletion_date.is_not(None),
                self.model.deletion_date <= data["deletion_date_max"],
            )
        return query

    def _apply_period_filters(
        self,
        query: Select,
        start_date: datetime,
        end_date: datetime,
    ) -> Select:
        start_date = self._normalize_datetime(start_date)
        end_date = self._normalize_datetime(end_date)
        
        return query.where(
            (self.model.deletion_date.is_(None)) | 
            (self.model.deletion_date >= start_date)
        ).where(
            self.model.creation_date <= end_date
        )
    
    def _normalize_datetime(self, dt: datetime) -> datetime:
        return dt.replace(tzinfo=None)

    async def _calculate_count_statistics(
        self, session: SessionDep, query: Select
    ) -> Dict[str, int]:
        query = select(func.count()).select_from(query.subquery())
        result = await session.execute(query)
        added_count = result.scalar() or 0

        query = select(func.count()).where(
            self.model.deletion_date.is_not(None)
        )
        result = await session.execute(query)
        removed_count = result.scalar() or 0

        return {
            "added_coils_count": added_count,
            "removed_coils_count": removed_count,
        }

    async def _calculate_size_statistics(
        self, session: SessionDep, query: Select
    ) -> Dict[str, float]:
        query = select(
            func.avg(self.model.length).label("avg_length"),
            func.avg(self.model.weight).label("avg_weight"),
            func.max(self.model.length).label("max_length"),
            func.max(self.model.weight).label("max_weight"),
            func.min(self.model.length).label("min_length"),
            func.min(self.model.weight).label("min_weight"),
            func.sum(self.model.weight).label("total_weight"),
        ).select_from(query.subquery())

        result = await session.execute(query)
        row = result.fetchone()
        
        if not row:
            return {
                "avg_length": 0,
                "avg_weight": 0,
                "max_length": 0,
                "max_weight": 0,
                "min_length": 0,
                "min_weight": 0,
                "total_weight": 0,
            }
        
        return dict(row._mapping)

    async def _calculate_storage_time_statistics(
        self, session: SessionDep, query: Select
    ) -> Dict[str, float]:
        query = select(
            func.max(self.model.deletion_date - self.model.creation_date)
        )
        result = await session.execute(query)
        max_storage_time_delta = result.scalar() or 0
        max_storage_time = (
            max_storage_time_delta.total_seconds()
            if isinstance(max_storage_time_delta, timedelta)
            else 0
        )

        query = select(
            func.min(self.model.deletion_date - self.model.creation_date)
        )
        result = await session.execute(query)
        min_storage_time_delta = result.scalar() or 0
        min_storage_time = (
            min_storage_time_delta.total_seconds()
            if isinstance(min_storage_time_delta, timedelta)
            else 0
        )

        return {
            "max_storage_time": max_storage_time,
            "min_storage_time": min_storage_time,
        }

    async def _get_statistics_by_day(
        self,
        session: SessionDep,
        start_date: datetime,
        end_date: datetime,
    ) -> Dict[str, Any]:
        extremes = {
            "min_count": {"value": float("inf"), "day": None},
            "max_count": {"value": 0, "day": None},
            "min_weight": {"value": float("inf"), "day": None},
            "max_weight": {"value": 0, "day": None},
        }

        date_range = [
            start_date + timedelta(days=i)
            for i in range((end_date - start_date).days + 1)
        ]
        
        for current_date in date_range:
            date = current_date.date()
            day_stats = await self._get_single_day_statistics(session, date)
            self._update_extremes(extremes, date, day_stats)

        return {
            "min_coils_date": extremes["min_count"]["day"],
            "min_coils_count": extremes["min_count"]["value"],
            "max_coils_date": extremes["max_count"]["day"],
            "max_coils_count": extremes["max_count"]["value"],
            "min_weight_date": extremes["min_weight"]["day"],
            "min_weight_total": extremes["min_weight"]["value"],
            "max_weight_date": extremes["max_weight"]["day"],
            "max_weight_total": extremes["max_weight"]["value"],
        }

    async def _get_single_day_statistics(
        self, session: SessionDep, date: date
    ) -> Dict[str, float]:
        day_start = datetime.combine(date, datetime.min.time())
        day_end = datetime.combine(date, datetime.max.time())

        query = select(
            func.count().label("count"),
            func.sum(self.model.weight).label("total_weight")
        ).where(
            (self.model.creation_date <= day_end) &
            ((self.model.deletion_date.is_(None)) | 
             (self.model.deletion_date >= day_start))
        )

        result = await session.execute(query)
        stats = result.fetchone()
        
        return {
            "count": stats.count or 0,
            "total_weight": stats.total_weight or 0,
        }

    def _update_extremes(
        self,
        extremes: Dict[str, Dict[str, Any]],
        date: date,
        day_stats: Dict[str, float],
    ) -> None:
        metrics = [
        ("min_count", "count", lambda x, y: x < y),
        ("max_count", "count", lambda x, y: x > y),
        ("min_weight", "total_weight", lambda x, y: x < y),
        ("max_weight", "total_weight", lambda x, y: x > y),
        ]

        for extreme_key, stat_key, comparison in metrics:
            value = day_stats[stat_key]
            if comparison(value, extremes[extreme_key]["value"]):
                extremes[extreme_key]["value"] = value
                extremes[extreme_key]["day"] = date