"""
This module contains fixtures and utilities for testing the FastAPI application.

It provides tools for setting up and tearing down a test database, creating an 
asynchronous HTTP client, and obtaining authorization tokens for authenticated requests.

Methods:
    - override_get_async_session: override async session
    - client: Creates an asynchronous HTTP client for making requests to the FastAPI app.
    - db_session: Provides an asynchronous database session for interacting with the test database.
    - setup_db: Sets up and tears down the test database with initial password data before and after tests.
"""

import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import (async_sessionmaker, create_async_engine)

from src.config.dependencies import get_async_session
from src.config.settings import settings
from src.main import app
from src.models.base import Base
from src.models.password import Password

TEST_DB_URL = settings.DATABASE_URL_TEST
test_engine = create_async_engine(TEST_DB_URL)
TestingSessionLocal = async_sessionmaker(bind=test_engine,
                                         expire_on_commit=False,
                                         autocommit=False)


async def override_get_async_session():
    """
    Function to override the dependency for getting an asynchronous session

    Returns an asynchronous session for testing
    """
    async with TestingSessionLocal() as session:
        yield session


app.dependency_overrides[get_async_session] = override_get_async_session


@pytest_asyncio.fixture
async def client():
    """
    Fixture to create an asynchronous HTTP client

    Creates a client using ASGITransport to test the FastAPI application

    Yields:
        AsyncClient: Asynchronous client for making HTTP requests to the application
    """
    async with AsyncClient(transport=ASGITransport(app=app),
                           base_url="http://test") as ac:
        yield ac


@pytest_asyncio.fixture
async def db_session():
    """
    Fixture to create an asynchronous database session

    Returns a session for interacting with the test database and closes it after use

    Yields:
        AsyncSession: Asynchronous session for working with the database
    """
    async with TestingSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


@pytest_asyncio.fixture(autouse=True)
async def setup_db(db_session):
    """
    Fixture to set up and tear down the test database with initial data
      
    Args:
        db_session (AsyncSession): Injected database session fixture
    
    Yields:
        None: Fixture pauses execution while tests run
    """
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    initial_passwords = [
        Password(service_name="default",
                 hashed_password="hashed_1234567890qwe",
                 password="1234567890qwe"),
        Password(service_name="yandex",
                 hashed_password="hashed_09876543210ytr",
                 password="09876543210ytr"),
        Password(service_name="gmail",
                 hashed_password="hashed_gmailgmailgmail",
                 password="gmailgmailgmail")
    ]
    for pwd in initial_passwords:
        db_session.add(pwd)
    await db_session.commit()

    yield

    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await test_engine.dispose()
