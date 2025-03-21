from typing import TypeVar, Generic, List, Type

from sqlalchemy import select

from src.database import SessionDep

ModelType = TypeVar("ModelType")


class BaseRepository(Generic[ModelType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def get_all(self, session: SessionDep) -> List[ModelType]:
        query = select(self.model)
        result = await session.execute(query)
        return list(result.scalars().all())

    async def add(self, session: SessionDep, data: dict) -> ModelType:
        new_model = self.model(**data)
        session.add(new_model)
        await session.commit()
        await session.refresh(new_model)
        return new_model
