from typing import Any, List, Union

from pydantic import BaseModel
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker

from openeo_fastapi.client.psql.settings import DataBaseSettings


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


class Filter(BaseModel):
    """Filter class to assist with providing a filter by funciton with values across different cases."""

    column_name: str
    value: Any


def create(create_object: BaseModel) -> bool:
    """Add the values from a pydantic model to the database using its respective object relational mapping."""
    db = sessionmaker(get_engine())

    orm = create_object._schema(**create_object.dict())

    with db.begin() as session:
        session.add(orm)
    return True


def get(get_model: BaseModel, primary_key: Any) -> Union[None, BaseModel]:
    """Get the relevant entry for a given model using the provided primary key value."""
    db = sessionmaker(get_engine())

    with db.begin() as session:
        if isinstance(primary_key, list):
            found = session.get(get_model._schema, primary_key)
        else:
            found = session.get(get_model._schema, str(primary_key))

        if not found:
            return None
        obj = get_model.from_orm(found)
    return obj


def get_first_or_default(get_model: BaseModel, filter_with: Filter) -> BaseModel:
    user_exists = list(filter_with=filter_with, list_model=get_model)
    if user_exists:
        return user_exists[0]
    return None


def list(list_model: BaseModel, filter_with: Filter) -> list[BaseModel]:
    """List all relevant entries for a given model for a given filter."""
    db = sessionmaker(get_engine())

    with db.begin() as session:
        # Sessions API has no list function, so prepare the statement with select and apply to scalar.
        if filter_with == None:
            query_statement = select(list_model._schema)
        else:
            query_statement = select(list_model._schema).filter_by(
                **{filter_with.column_name: filter_with.value}
            )
        job_objs = session.scalars(query_statement)
        jobs = [list_model.from_orm(job_obj) for job_obj in job_objs]
    return jobs


def modify(modify_object: BaseModel) -> bool:
    """Modify the relevant entries for a given model instance."""
    db = sessionmaker(get_engine())

    with db.begin() as session:
        session.merge(modify_object._schema(**modify_object.dict()))
    return True
