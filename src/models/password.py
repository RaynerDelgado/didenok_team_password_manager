"""
This module defines the Password db models class

Classes:
    Password: Password db model class
"""
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from src.models.base import Base


class Password(Base):
    """
    Represents a password in the database.

    Attributes:
        id (int): The unique identifier for the password, auto-incremented.
        service (str): The title of the password.
        password (str): A detailed description of the password.
    """
    __tablename__ = "password"

    id: Mapped[int] = mapped_column(Integer,
                                    primary_key=True,
                                    autoincrement=True)
    service_name: Mapped[str] = mapped_column(String(30),
                                              index=True,
                                              nullable=False,
                                              unique=True)
    password: Mapped[str] = mapped_column(String(50),
                                                 index=False,
                                                 nullable=False,
                                                 unique=False)
    hashed_password: Mapped[str] = mapped_column(String(255),
                                                 index=False,
                                                 nullable=False,
                                                 unique=False)
