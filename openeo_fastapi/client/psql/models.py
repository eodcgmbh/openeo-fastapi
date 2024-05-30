"""ORM definitions for defining and storing the associated data in the databse.
"""
import datetime

from sqlalchemy import BOOLEAN, VARCHAR, Column, DateTime
from sqlalchemy.dialects.postgresql import ENUM, JSON, UUID

from openeo_fastapi.api.types import Status
from openeo_fastapi.client.psql.settings import BASE


class UserORM(BASE):
    """ORM for the user table."""

    __tablename__ = "users"
    __table_args__ = {"extend_existing": True}

    user_id = Column(UUID(as_uuid=True), primary_key=True, unique=True)
    """UUID of the user."""
    oidc_sub = Column(VARCHAR, unique=True)
    """OIDC substring of the user."""
    created_at = Column(DateTime, default=datetime.datetime.utcnow(), nullable=False)
    """The datetime the user was created."""


class JobORM(BASE):
    """ORM for the job table."""

    __tablename__ = "jobs"
    __table_args__ = {"extend_existing": True}

    job_id = Column(UUID(as_uuid=True), primary_key=True)
    """UUID of the job."""
    process = Column(JSON, nullable=False)
    """The process graph for this job."""
    status = Column(ENUM(Status), nullable=False)
    """The status of the Job."""
    user_id = Column(UUID(as_uuid=True), nullable=False)
    """The UUID of the user that owns this job."""
    created = Column(DateTime, default=datetime.datetime.utcnow(), nullable=False)
    """The datetime the job was created."""
    title = Column(VARCHAR)
    """The title of the job."""
    description = Column(VARCHAR)
    """The job description."""
    synchronous = Column(BOOLEAN, default=False, nullable=False)
    """If the Job is synchronous."""


class UdpORM(BASE):
    """ORM for the UDPS table."""

    __tablename__ = "udps"
    __table_args__ = {"extend_existing": True}

    id = Column(VARCHAR, primary_key=True, nullable=False)
    """The string name of the UDP. CPK with user_id. Different users can use the same string for id."""
    user_id = Column(UUID(as_uuid=True), primary_key=True, nullable=False)
    """The UUID of the user that owns this UDP."""
    process_graph = Column(JSON, nullable=False)
    """The process graph of the UDP."""
    created = Column(DateTime, default=datetime.datetime.utcnow(), nullable=False)
    """The datetime the UDP was created."""
    parameters = Column("parameters", JSON)
    """The parameters of the UDP."""
    returns = Column("returns", JSON)
    """The return types of the UDP."""
    summary = Column("summary", VARCHAR)
    """A summary of the UPD."""
    description = Column("description", VARCHAR)
    """A description of what the UDP is intended to do."""
