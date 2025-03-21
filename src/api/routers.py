from fastapi import APIRouter

from src.database import create_database_if_not_exists
from src.api.coil_router import router as coils_router
from src.api.statistics_router import router as statistics_router


all_routers = [coils_router, statistics_router]
main_router = APIRouter(prefix="/api")


@main_router.on_event("startup")
async def startup():
    await create_database_if_not_exists()


for router in all_routers:
    main_router.include_router(router)
