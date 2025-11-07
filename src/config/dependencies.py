from typing import AsyncGenerator

from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)

from src.config.settings import settings

engine = create_async_engine(settings.DATABASE_URL, echo=False)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    try:
        async with async_session_maker() as session:
            yield session
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to connect to the database: {str(e)}")
