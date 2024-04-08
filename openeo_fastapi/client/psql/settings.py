"""Defining the settings to be used at the application layer of the API for database interaction."""
from pathlib import Path

from pydantic import BaseSettings, SecretStr
from sqlalchemy.orm import declarative_base

BASE = declarative_base()

class DataBaseSettings(BaseSettings):
    """Appliction DataBase settings to interact with PSQL."""
    POSTGRES_USER: SecretStr
    """The name of the postgres user."""
    POSTGRES_PASSWORD: SecretStr
    """The pasword for the postgres user."""
    POSTGRESQL_HOST: SecretStr
    """The host the database runs on."""
    POSTGRESQL_PORT: SecretStr
    """The post on the host the database is available on."""
    POSTGRES_DB: SecretStr
    """The name of the databse being used on the host."""

    ALEMBIC_DIR: Path
    """The path leading to the alembic directory to be used."""
