"""
This module defines the data models and schemas related to password.

It includes classes that represent the structure and validation rules
for password-related data, such as password creation, password reading.

Classes:
    - PasswordCreate: A model representing the data required to create a new password.
    - PasswordRead: A model representing a password with additional details, inheriting from PasswordCreate.
"""
from typing import Annotated

from pydantic import BaseModel, Field


class PasswordCreate(BaseModel):
    """
    Class PasswordCreate represents the data required to create a new password

    Args:
        service_name (str): The name of the service, must be at least 2 characters long
        password (str): The password of service, must be at least 8 characters long.
    """
    service_name: Annotated[str, Field(min_length=2)]
    password: Annotated[str, Field(min_length=8)]


class PasswordRead(PasswordCreate):
    """
    Class PasswordRead represents a password with additional details

    Inherits from PasswordCreate and adds:

    Args:
        id (int): The unique identifier for the password.
        password_hash (str): Hash of password.
    """
    id: int
    password_hash: str
