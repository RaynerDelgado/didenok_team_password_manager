"""
This module defines an async connection to the database.

It provides methods for obtaining an asynchronous database session and a user database instance.
Additionally, it includes error handling for cases where the database connection fails.

Methods:
    - get_async_session: A dependency function that provides an asynchronous database session.
"""
from typing import AsyncGenerator

from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)

from src.config.settings import settings

engine = create_async_engine(settings.DATABASE_URL, echo=False)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency to get an asynchronous database session.

    Yields:
        AsyncSession: An instance of AsyncSession for database operations.

    Raises:
        HTTPException: If the database connection fails.
    """
    try:
        async with async_session_maker() as session:
            yield session
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to connect to the database: {str(e)}")
