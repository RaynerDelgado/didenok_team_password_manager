"""
This module contains integration tests for the password-related API endpoints.

Methods:
    - test_post_password: Tests the creation of a new password.
    - test_get_password: Tests retrieving a specific password by its service.
    - test_search_password: Tests retrieving a password by its part of service name.
"""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_post_password(client: AsyncClient):
    """
    Test API for post password
    """
    password_data = {
        "service_name": "test_service",
        "password": "1234567890qwerty",
    }
    response = await client.post("/password/", json=password_data)
    assert response.status_code == 201
    data = response.json()
    assert data["service_name"] == "test_service"
    assert data["password"] == "1234567890qwerty"


@pytest.mark.asyncio
async def test_invalid_post_password(client: AsyncClient):
    """
    Test API for invalid post password
    """
    password_data = {
        "service_name": "test_service",
        "password": "123",
    }
    response = await client.post("/password/", json=password_data)
    assert response.status_code == 422
    message = response.json()["detail"][0]["msg"]
    assert message == "String should have at least 8 characters"


@pytest.mark.asyncio
async def test_get_password(client: AsyncClient):
    """
    Test API for search password
    """
    service_name = "gmail"
    response = await client.get(f"/password/{service_name}")
    assert response.status_code == 200
    data = response.json()
    assert data["service_name"] == "gmail"
    assert data["password"] == "gmailgmailgmail"


@pytest.mark.asyncio
async def test_get_unexist_password(client: AsyncClient):
    """
    Test API for search unexist password
    """
    service_name = "mail"
    response = await client.get(f"/password/{service_name}")
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Password(s) not found"


@pytest.mark.asyncio
async def test_search_password(client: AsyncClient):
    """
    Test API for search password
    """
    service_name = "yan"
    response = await client.get(f"/password/?service_name={service_name}")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["service_name"] == "yandex"
    assert data[0]["password"] == "09876543210ytr"


@pytest.mark.asyncio
async def test_search_unexist_password(client: AsyncClient):
    """
    Test API for search unexist password
    """
    service_name = "opl"
    response = await client.get(f"/password/?service_name={service_name}")
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Password(s) not found"
