from pathlib import Path

from pydantic import BaseSettings, SecretStr
from sqlalchemy.orm import declarative_base

BASE = declarative_base()


class DataBaseSettings(BaseSettings):
    POSTGRES_USER: SecretStr
    POSTGRES_PASSWORD: SecretStr
    POSTGRESQL_HOST: SecretStr
    POSTGRESQL_PORT: SecretStr
    POSTGRES_DB: SecretStr

    ALEMBIC_DIR: Path
