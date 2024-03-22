from typing import Optional

from pydantic import BaseModel, Extra, Field

from openeo_fastapi.api.types import Process


class JobProcessGraph(Process):
    """Model for some incoming requests to the api."""

    process_graph_id: str = Field(default=None, alias="id")
    summary: Optional[str] = None
    description: Optional[str] = None
    parameters: Optional[list] = None
    returns: Optional[dict] = None
    process_graph: dict = None

    class Config:
        allow_population_by_field_name = True
        extra = Extra.ignore


class JobsRequest(BaseModel):
    """Request model for job endpoints."""

    title: str = None
    description: Optional[str] = None
    process: Optional[JobProcessGraph] = None
    plan: Optional[str] = None
    budget: Optional[str] = None
