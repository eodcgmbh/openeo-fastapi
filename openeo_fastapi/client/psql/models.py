import datetime
from enum import Enum

from sqlalchemy import BOOLEAN, VARCHAR, Column, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import ENUM, JSON, UUID
from sqlalchemy.orm import relationship

from openeo_fastapi.client.psql.settings import BASE


class Status(Enum):
    created = "created"
    queued = "queued"
    running = "running"
    canceled = "canceled"
    finished = "finished"
    error = "error"


class User(BASE):
    """ORM for the user table."""

    __tablename__ = "users"
    __table_args__ = {"extend_existing": True}

    user_id = Column(UUID(as_uuid=True), primary_key=True, unique=True)
    oidc_sub = Column(VARCHAR, unique=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow(), nullable=False)


class Job(BASE):
    """ORM for the job table."""

    __tablename__ = "jobs"

    job_id = Column(UUID(as_uuid=True), primary_key=True)
    process_graph_id = Column(VARCHAR, nullable=False)
    status = Column(ENUM(Status), nullable=False)
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.user_id", ondelete="CASCADE"),
        nullable=False,
    )
    created = Column(DateTime, default=datetime.datetime.utcnow(), nullable=False)
    title = Column(VARCHAR)
    description = Column(VARCHAR)
    synchronous = Column(BOOLEAN, default=False, nullable=False)  # if null assume False

    children = relationship("User")


class ProcessGraph(BASE):
    """ORM for the process graph table."""

    __tablename__ = "process_graph"

    process_graph_id = Column(VARCHAR, primary_key=True)
    process_graph = Column(JSON, nullable=False)
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.user_id", ondelete="CASCADE"),
        nullable=False,
    )
    created = Column(DateTime, default=datetime.datetime.utcnow(), nullable=False)
    children = relationship("User")


class UserDefinedProcessGraph(BASE):
    """ORM for the UDPS table."""

    __tablename__ = "udps"

    udp_id = Column(String, primary_key=True, nullable=False)
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.user_id"),
        primary_key=True,
        nullable=False,
    )
    process_graph = Column(JSON, nullable=False)
    created = Column(DateTime, default=datetime.datetime.utcnow(), nullable=False)
    parameters = Column("parameters", JSON)
    returns = Column("returns", JSON)
    summary = Column("summary", String)
    description = Column("description", String)

    children = relationship("User")
