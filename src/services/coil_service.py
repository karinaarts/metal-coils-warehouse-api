from typing import List

from src.schemas.coil_schema import CoilAddSchema, CoilSchema, CoilFilterSchema
from src.repositories.coil_repository import CoilRepository
from src.database import SessionDep


class CoilService:
    def __init__(self):
        self.repository = CoilRepository()

    async def create(
        self, session: SessionDep, data: CoilAddSchema
    ) -> CoilSchema:
        coil_dict = data.model_dump()
        coil = await self.repository.add(session, coil_dict)
        return CoilSchema.model_validate(coil, from_attributes=True)

    async def delete(self, session: SessionDep, id: int) -> CoilSchema:
        coil = await self.repository.delete(session, id)
        return CoilSchema.model_validate(coil, from_attributes=True)

    async def get_all(self, session: SessionDep) -> List[CoilSchema]:
        coils = await self.repository.get_all(session)
        return [
            CoilSchema.model_validate(coil, from_attributes=True)
            for coil in coils
        ]

    async def get_filtered(
        self, session: SessionDep, data: CoilFilterSchema
    ) -> List[CoilSchema]:
        filter_dict = data.model_dump()
        coils = await self.repository.get_filtered(session, filter_dict)
        return [
            CoilSchema.model_validate(coil, from_attributes=True)
            for coil in coils
        ]
