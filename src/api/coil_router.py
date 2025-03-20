from fastapi import APIRouter
from typing import List

from src.services.coil_service import CoilService
from src.schemas.coil_schema import CoilAddSchema, CoilSchema
from src.database import SessionDep

router = APIRouter(prefix="/coils", tags=["coils"])
service = CoilService()


@router.post("/", response_model=CoilSchema, status_code=201)
async def add_coil(data: CoilAddSchema, session: SessionDep):
    return await service.create(session, data)


@router.get("/", response_model=List[CoilSchema])
async def get_coils(session: SessionDep):
    return await service.get_all(session)
