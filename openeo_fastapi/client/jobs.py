import datetime
import uuid
from typing import Optional

from pydantic import BaseModel, Field

from openeo_fastapi.client.models import Endpoint, Process, Status
from openeo_fastapi.client.register import EndpointRegister


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
        extra = "ignore"


class JobsRequest(BaseModel):
    """Request model for job endpoints."""

    title: str = None
    description: Optional[str] = None
    process: Optional[JobProcessGraph] = None
    plan: Optional[str] = None
    budget: Optional[str] = None


class Job(BaseModel):
    """Pydantic model manipulating jobs."""

    job_id: uuid.UUID
    process_graph_id: str
    status: Status
    user_id: uuid.UUID
    created: datetime.datetime
    title: Optional[str]
    description: Optional[str]
    synchronous: bool = False

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
        extra = "ignore"

    def patch(self, patch):
        """Update pydantic model with changed fields from a new model instance."""

        if type(patch) not in [Job, JobsRequest]:
            raise TypeError("Job only updates from a Job or JobRequest model.")
        for k, v in patch.dict().items():
            if v:
                if k in self.__fields__.keys():
                    if not (self.dict()[k] == v):
                        self.__setattr__(k, patch.dict()[k])
        return self


class JobsRegister(EndpointRegister):
    def __init__(self, database, settings) -> None:
        super().__init__()
        self.endpoints = self._initialize_endpoints()
        self.database = database
        self.settings = settings

    def _initialize_endpoints(self) -> list[Endpoint]:
        return [
            Endpoint(
                path="/jobs",
                methods=["GET"],
            ),
            Endpoint(
                path="/jobs",
                methods=["POST"],
            ),
            Endpoint(
                path="/jobs/{job_id}",
                methods=["GET"],
            ),
            Endpoint(
                path="/jobs/{job_id}",
                methods=["POST"],
            ),
            Endpoint(
                path="/jobs/{job_id}",
                methods=["DELETE"],
            ),
            Endpoint(
                path="/jobs/{job_id}/estimate",
                methods=["GET"],
            ),
            Endpoint(
                path="/jobs/{job_id}/logs",
                methods=["GET"],
            ),
        ]

    def list_jobs(self):
        pass

    def create_job(self):
        pass

    def get_job(self, job_id: str):
        pass

    def delete_job(self, job_id: str):
        pass

    def estimate(self, job_id: str):
        pass

    def logs(self, job_id: str):
        pass
