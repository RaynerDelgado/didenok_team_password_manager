"""
This module defines the password router, which handles all password-related API endpoints.

The router provides Create, Read, Search operations for password.

Endpoints:
    - GET /?service_name={service_name}: Search all password for the services name.
    - GET /{service_name}: Retrieves a specific password by its services.
    - POST /: Creates a new password.
"""
from typing import List
from fastapi import Depends, Query
from fastapi.routing import APIRouter

from src.managers.password import PasswordManager, get_password_manager
from src.schemas.password import PasswordCreate, PasswordRead

passwordroute = APIRouter()


@passwordroute.get("/{service_name}", response_model=PasswordCreate)
async def get_password(
    service_name: str,
    password_manager: PasswordManager = Depends(get_password_manager)):
    """
    Retrieves a specific password by its service.

    Args:
        service_name (str): The service name of the password to retrieve.
        password_manager (PasswordManager, optional): The password manager dependency to handle password operations.

    Returns:
        Password: The Password object representing the requested password.

    Raises:
        HTTPException: If the password with the specified service does not exist.
    """

    return await password_manager.get_password(service_name)


@passwordroute.get("/", response_model=List[PasswordCreate])
async def search_password(
        service_name: str = Query(
            ..., description="Part of service name"),
        password_manager: PasswordManager = Depends(get_password_manager)):
    """
    Search a specific by part of the service name.

    Args:
        service_name (str): The service name of the password to retrieve.
        password_manager (PasswordManager, optional): The password manager dependency to handle password operations.

    Returns:
        Password: The Password object representing the requested password.

    Raises:
        HTTPException: If the password with the specified service does not exist.
    """

    return await password_manager.search_password(service_name)


@passwordroute.post("/", response_model=PasswordCreate, status_code=201)
async def post_password(
    password: PasswordCreate,
    password_manager: PasswordManager = Depends(get_password_manager)):
    """
    Creates a new password.

    Args:
        password (PasswordCreate): The password data to create a new password.
        password_manager (PasswordManager, optional): The password manager dependency to handle password operations.

    Returns:
        Password: The created Password object.
    
    Raises:
        HTTPException: If the password data invalid.
    """
    return await password_manager.create_password(password)
