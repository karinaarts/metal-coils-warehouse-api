from typing import List

from src.models.coil_model import CoilModel
from src.schemas.coil_schema import CoilAddSchema, CoilSchema
from src.repositories.coil_repository import CoilRepository
from src.database import SessionDep


class CoilMapper:
    def to_schema(self, model: CoilModel) -> CoilSchema:
        return CoilSchema(
            id=model.id,
            length=model.length,
            width=model.width,
            creation_date=model.creation_date,
            deletion_date=model.deletion_date,
        )

    def to_dict(self, schema: CoilSchema) -> dict:
        return schema.model_dump()


class CoilService:
    def __init__(self):
        self.repository = CoilRepository()
        self.mapper = CoilMapper()

    async def create(
        self, session: SessionDep, data: CoilAddSchema
    ) -> CoilSchema:
        coil_dict = self.mapper.to_dict(data)
        coil = await self.repository.add(session, coil_dict)
        return self.mapper.to_schema(coil)

    async def get_all(self, session: SessionDep) -> List[CoilSchema]:
        coils = await self.repository.get_all(session)
        return [self.mapper.to_schema(coil) for coil in coils]
