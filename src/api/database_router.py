from fastapi import APIRouter

from src.database import Base, engine

router = APIRouter(tags=["database"])


@router.post("/setup_database")
async def setup_database():
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)
        await connection.run_sync(Base.metadata.create_all)
    return {"success": True, "message": "База данных успешно создана"}
