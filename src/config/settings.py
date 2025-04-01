"""
This module defines an settings for app 

Classes:
    - Settings: contains const settings from enviroment
"""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Settings class for managing application configuration.

    This class loads settings from an environment file (.env) 
    and provides access to database connection parameters and 
    other setting.
    
    In this implementation, the testing database and the development database differ only in name!

    Attributes:
        DB_HOST (str): Host for the database connection.
        DB_PORT (int): Port for the database connection.
        DB_USER (str): Username for the database connection.
        DB_PASS (str): Password for the database connection.
        DB_NAME (str): Name of the main database.
        DB_TEST_NAME (str): Name of the test database.
        ENV (str): Application environment mode ("TEST" - migrations for testing db, "DEV" - migrations for dev db)
    """

    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str
    DB_TEST_NAME: str
    ENV: str

    @property
    def DATABASE_URL(self) -> str:
        """
        Constructs the connection string for the main database.

        Uses the asyncpg driver for asynchronous connections.

        Returns:
            str: Connection string for the main database.
        """
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def DATABASE_URL_ALEMBIC(self) -> str:
        """
        Constructs the connection string for Alembic migrations.

        Uses the psycopg2 driver for synchronous connections.

        Returns:
            str: Connection string for the main database for Alembic.
        """
        return f"postgresql+psycopg2://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def DATABASE_URL_TEST(self) -> str:
        """
        Constructs the connection string for the test database.

        Uses the asyncpg driver for asynchronous connections.

        Returns:
            str: Connection string for the test database.
        """
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_TEST_NAME}"

    @property
    def DATABASE_URL_TEST_ALEMBIC(self) -> str:
        """
        Constructs the connection string for the test database 
        for Alembic migrations.

        Uses the psycopg2 driver for synchronous connections.

        Returns:
            str: Connection string for the test database for Alembic.
        """
        return f"postgresql+psycopg2://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_TEST_NAME}"

    @property
    def GET_SECRET(self) -> str:
        """
        Returns the secret key.

        Used for encryption and authentication.

        Returns:
            str: The secret key.
        """
        return self.SECRET

    class Config:
        """
        Configuration settings for the Settings class.
        """
        env_file = ".env"


settings = Settings()
