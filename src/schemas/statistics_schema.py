from datetime import datetime, date
from pydantic import BaseModel
from typing import Optional


class StatisticsPeriodSchema(BaseModel):
    start_date: Optional[datetime]
    end_date: Optional[datetime]


class StatisticsResponse(BaseModel):
    added_coils_count: int = 0
    removed_coils_count: int = 0

    avg_length: float = 0
    avg_weight: float = 0
    min_length: float = 0
    max_length: float = 0
    min_weight: float = 0
    max_weight: float = 0

    total_weight: float = 0

    min_storage_time: float = 0
    max_storage_time: float = 0

    min_coils_date: Optional[date] = None
    min_coils_count: Optional[int] = None
    max_coils_date: Optional[date] = None
    max_coils_count: Optional[int] = None
    min_weight_date: Optional[date] = None
    min_weight_total: Optional[float] = None
    max_weight_date: Optional[date] = None
    max_weight_total: Optional[float] = None
