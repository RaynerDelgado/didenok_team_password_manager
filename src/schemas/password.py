"""
This module defines the data models and schemas related to tasks.

It includes classes and enums that represent the structure and validation rules 
for task-related data, such as task status, task creation, task reading, and task updates.

Classes:
    - TaskStatus: An enumeration representing the possible statuses of a task.
    - TaskCreate: A model representing the data required to create a new task.
    - TaskRead: A model representing a task with additional details, inheriting from TaskCreate.
    - TaskUpdate: A model representing the data required to update an existing task.
    - TaskStatus: Defines the possible statuses of a task (NEW, IN_PROGRESS, COMPLETED).
"""
from typing import Annotated, Optional

from pydantic import BaseModel, Field


class PasswordCreate(BaseModel):
    """
    Class TaskCreate represents the data required to create a new task

    Args:
        title (str): The title of the task, must be at least 4 characters long
        description (str): A detailed description of the task (default is an empty string)
        status (TaskStatus): The current status of the task (default is TaskStatus.NEW)
        name (Optional[str]): An optional name associated with the task, must be at least 4 characters long

    Raises:
        ValueError: If title is less than 4 characters long
    """
    service_name: Annotated[str, Field(min_length=2)]
    password: Annotated[str, Field(min_length=8)]


class PasswordRead(PasswordCreate):
    """
    Class Task represents a task with additional details

    Inherits from TaskCreate and adds:

    Args:
        id (int): The unique identifier for the task
        user_id (int): The identifier of the user who created the task
    """
    id: int
    password_hash: str
