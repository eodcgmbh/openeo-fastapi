import datetime

from sqlalchemy import VARCHAR, Column, DateTime
from sqlalchemy.dialects.postgresql import UUID

from openeo_fastapi.client.psql.settings import BASE


class User(BASE):
    """ORM for the user table."""

    __tablename__ = "users"
    __table_args__ = {"extend_existing": True}

    user_id = Column(UUID(as_uuid=True), primary_key=True, unique=True)
    oidc_sub = Column(VARCHAR, unique=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow(), nullable=False)
