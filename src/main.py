"""
This module serves as the entry point for the FastAPI application.

It initializes the FastAPI app and includes the routers for password management.

Routers:
    - passwordroute: Handles password endpoints.

Endpoints:
    - Password-related endpoints are available under the `/password` path.

Usage:
    Run this module to start the FastAPI application. The application will be accessible 
    at the specified host and port (e.g., http://localhost:8000).
"""
from fastapi import FastAPI

from src.routers.password import passwordroute

app = FastAPI()
app.include_router(
    passwordroute,
    prefix="/password",
    tags=["password"],
)
