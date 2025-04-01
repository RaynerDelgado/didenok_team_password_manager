"""
This module defines the Base db models class

Classes:
    Base: Base db model class
"""
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """
    Base class for all SQLAlchemy models.
    """
    pass
