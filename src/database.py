import os
from typing import Annotated, AsyncGenerator
from dotenv import load_dotenv
from fastapi import Depends
from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    AsyncSession,
    create_async_engine,
)
from sqlalchemy.orm import declarative_base


load_dotenv()
DATABASE_URL = f"postgresql+asyncpg://{os.getenv('DB_USER')}@{
    os.getenv('DB_HOST')
}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"

engine = create_async_engine(DATABASE_URL)
new_session = async_sessionmaker(engine, expire_on_commit=False)
Base = declarative_base()


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with new_session() as session:
        yield session


SessionDep = Annotated[AsyncSession, Depends(get_session)]
