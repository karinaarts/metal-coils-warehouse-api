from typing import List

from fastapi import APIRouter, Depends

from src.services.coil_service import CoilService
from src.schemas.coil_schema import CoilAddSchema, CoilSchema, CoilFilterSchema
from src.database import SessionDep

router = APIRouter(prefix="/coils", tags=["coils"])
service = CoilService()


@router.post("/", response_model=CoilSchema, status_code=201)
async def add_coil(data: CoilAddSchema, session: SessionDep):
    return await service.create(session, data)


@router.delete("/{id}", response_model=CoilSchema)
async def delete_coil(id: int, session: SessionDep):
    return await service.delete(session, id)


@router.get("/filtered", response_model=List[CoilSchema])
async def get_filtered_coils(
    session: SessionDep, filter_params: CoilFilterSchema = Depends()
):
    return await service.get_filtered(session, filter_params)


@router.get("/", response_model=List[CoilSchema])
async def get_coils(session: SessionDep):
    return await service.get_all(session)
