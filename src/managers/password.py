"""
This module defines the PasswordManager class for managing password-related operations.

Classes:
    PasswordManager: Handles password creation, retrieval, updating, and deletion.

Methods:
    get_password_manager: Dependency to retrieve a PasswordManager instance.
    is_password_data_empty: Raise HTTPException if password(s) not found
"""

from typing import List

from fastapi import Depends, HTTPException
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.config.dependencies import get_async_session
from src.models.password import Password
from src.schemas.password import PasswordCreate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class PasswordManager:
    """
    PasswordManager class for handling password-related operations.

    This class provides methods to create, retrieve, search passwords
    associated with the user identified by user id.

    Attributes:
        session (AsyncSession): The SQLAlchemy session for database operations.
    """

    def __init__(self, session: AsyncSession):
        self.session = session

    @staticmethod
    def get_password_hash(password: str) -> str:
        """Generate a hashed password."""
        return pwd_context.hash(password)

    async def get_password(self, service_name: str) -> Password:
        """
        Retrieves a specific password by its service name.

        Args:
            service_name (str): The name of the service to retrieve.

        Returns:
            Password: The password associated with the given service.

        Raises:
            HTTPException: If the passwords is not found.
        """
        query = select(Password).where(Password.service_name == service_name)
        existing_password = await self.session.execute(query)
        existing_password = existing_password.scalars().first()
        is_password_data_empty(existing_password)
        return existing_password

    async def search_password(self, service_name: str) -> List[Password]:
        """
        Retrieves a specific password by its service name.

        Args:
            service_name (str): The part of name of the service to retrieve.

        Returns:
            Password: The password associated with the given service.

        Raises:
            HTTPException: If the password is not found.
        """
        query = select(Password).where(Password.service_name.contains(service_name))
        existing_password = await self.session.execute(query)
        existing_password = existing_password.scalars().all()
        is_password_data_empty(existing_password)
        return existing_password

    async def create_password(self, password: PasswordCreate) -> Password:
        """
        Creates a new password for the service.

        Args:
            password (PasswordCreate): The password data to create.

        Returns:
            Password: The newly created password.

        Raises:
            HTTPException: If the data invalid.
        """
        new_password = Password(
            service_name=password.service_name,
            password=password.password,
            hashed_password=PasswordManager.get_password_hash(password.password),
        )
        self.session.add(new_password)
        await self.session.commit()
        await self.session.refresh(new_password)
        return password


async def get_password_manager(session: AsyncSession = Depends(get_async_session)):
    """
    Dependency to retrieve a PasswordManager instance.

    Args:
        session (AsyncSession): The SQLAlchemy session for database operations.

    Returns:
        PasswordManager: An instance of PasswordManager for the user.
    """
    yield PasswordManager(session)


def is_password_data_empty(data):
    """
    Checks if the provided data is empty. If the data is empty, raises an HTTPException.

    Args:
        data (Any): The data to check. This can be of any type, including lists, dictionaries, strings, etc.

    Raises:
        HTTPException:
            - If the data is empty (e.g., empty list, empty string, empty dictionary),
              raises an HTTPException with status code 404 and detail "Password(s) not found".

    Return:
        None
    """
    if not data:
        raise HTTPException(status_code=404, detail="Password(s) not found")
