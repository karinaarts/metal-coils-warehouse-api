from fastapi import APIRouter

from src.api.coil_router import router as coils_router
from src.api.database_router import router as database_router


all_routers = [coils_router, database_router]
main_router = APIRouter(prefix="/api")

for router in all_routers:
    main_router.include_router(router)
