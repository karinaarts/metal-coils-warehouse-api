from datetime import datetime, timedelta, timezone
from unittest.mock import AsyncMock

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import Base, engine
from src.main import app as main_app
from src.models.coil_model import CoilModel
from src.repositories.coil_repository import CoilRepository
from src.services.coil_service import CoilService
from src.services.statistics_service import StatisticsService


@pytest.fixture
def mock_session():
    session = AsyncMock(spec=AsyncSession)
    session.commit = AsyncMock()
    session.refresh = AsyncMock()
    return session


@pytest.fixture
def sample_coil_data():
    return {
        "length": 100.0,
        "weight": 500.0,
    }


@pytest.fixture
def sample_coil_model():
    now = datetime.now(timezone.utc)
    return CoilModel(
        id=1, length=100.0, weight=500.0, creation_date=now, deletion_date=None
    )


@pytest.fixture
def deleted_coil_model():
    now = datetime.now(timezone.utc)
    return CoilModel(
        id=2,
        length=150.0,
        weight=750.0,
        creation_date=now - timedelta(days=5),
        deletion_date=now,
    )


@pytest.fixture
def mock_coil_repository():
    repository = AsyncMock(spec=CoilRepository)
    return repository


@pytest.fixture
def coil_service(mock_coil_repository):
    service = CoilService()
    service.repository = mock_coil_repository
    return service


@pytest.fixture
def statistics_service(mock_coil_repository):
    service = StatisticsService()
    service.coil_repository = mock_coil_repository
    return service


@pytest.fixture
def sample_statistics_data():
    return {
        "added_coils_count": 10,
        "removed_coils_count": 3,
        "avg_length": 120.5,
        "avg_weight": 550.75,
        "min_length": 80.0,
        "max_length": 200.0,
        "min_weight": 300.0,
        "max_weight": 800.0,
        "total_weight": 5507.5,
        "min_storage_time": 3600.0,
        "max_storage_time": 86400.0,
        "min_coils_date": datetime.now().date(),
        "min_coils_count": 2,
        "max_coils_date": datetime.now().date(),
        "max_coils_count": 15,
        "min_weight_date": datetime.now().date(),
        "min_weight_total": 1500.0,
        "max_weight_date": datetime.now().date(),
        "max_weight_total": 8000.0,
    }


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def drop_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture()
async def client():
    await drop_tables()
    await create_tables()
    async with AsyncClient(
        transport=ASGITransport(main_app), base_url="http://test"
    ) as test_client:
        yield test_client
