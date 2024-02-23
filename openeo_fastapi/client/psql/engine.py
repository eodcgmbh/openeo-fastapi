from sqlalchemy import create_engine

from openeo_fastapi.client.psql.settings import BASE, DataBaseSettings


def get_engine():
    """Return default session using config from pydantic settings."""
    db_settings = DataBaseSettings()

    engine = create_engine(
        url="postgresql://{}:{}@{}:{}/{}".format(
            db_settings.POSTGRES_USER._secret_value,
            db_settings.POSTGRES_PASSWORD._secret_value,
            db_settings.POSTGRESQL_HOST._secret_value,
            db_settings.POSTGRESQL_PORT._secret_value,
            db_settings.POSTGRES_DB._secret_value,
        )
    )
    return engine


def create_all():
    """ """
    BASE.metadata.create_all(get_engine())
