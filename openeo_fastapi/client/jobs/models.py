import datetime
import uuid
from typing import Optional

from pydantic import BaseModel, Extra, Field, validator

from openeo_fastapi.client.models import Link, RFC3339Datetime, Status
from openeo_fastapi.client.processes.models import Process, ProcessGraphWithMetadata
from openeo_fastapi.client.psql.models import JobORM


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
        extra = Extra.ignore

    @classmethod
    def get_orm(cls):
        return JobORM

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


class UsageMetric(BaseModel):
    value: float
    unit: str


class Usage(BaseModel):
    class Config:
        extra = Extra.allow

    cpu: Optional[UsageMetric] = Field(
        None,
        description="Specifies the CPU usage, usually in a unit such as `cpu-seconds`.",
    )
    memory: Optional[UsageMetric] = Field(
        None,
        description="Specifies the memory usage, usually in a unit such as `mb-seconds` or `gb-hours`.",
    )
    duration: Optional[UsageMetric] = Field(
        None,
        description="Specifies the wall time, usually in a unit such as `seconds`, `minutes` or `hours`.",
    )
    network: Optional[UsageMetric] = Field(
        None,
        description="Specifies the network transfer usage (incoming and outgoing), usually in a unit such as `b` (bytes), `kb` (kilobytes), `mb` (megabytes) or `gb` (gigabytes).",
    )
    disk: Optional[UsageMetric] = Field(
        None,
        description="Specifies the amount of input (read) and output (write) operations on the storage such as disks, usually in a unit such as `b` (bytes), `kb` (kilobytes), `mb` (megabytes) or `gb` (gigabytes).",
    )
    storage: Optional[UsageMetric] = Field(
        None,
        description="Specifies the usage of storage space, usually in a unit such as `b` (bytes), `kb` (kilobytes), `mb` (megabytes) or `gb` (gigabytes).",
    )


class BatchJob(BaseModel):
    job_id: uuid.UUID = Field(default=None, alias="id")
    title: Optional[str] = None
    description: Optional[str] = None
    process: Optional[ProcessGraphWithMetadata] = None
    status: Status
    progress: Optional[float] = Field(
        None,
        description="Indicates the process of a running batch job in percent.\nCan also be set for a job which stopped due to an error or was canceled by the user. In this case, the value indicates the progress at which the job stopped. The Property may not be available for the status codes `created` and `queued`.\nSubmitted and queued jobs only allow the value `0`, finished jobs only allow the value `100`.",
        example=75.5,
    )
    created: RFC3339Datetime
    updated: Optional[RFC3339Datetime] = None
    plan: Optional[str] = None
    costs: Optional[float] = None
    budget: Optional[float] = None
    usage: Optional[Usage] = Field(
        None,
        description="Metrics about the resource usage of the batch job.\n\nBack-ends are not expected to update the metrics while processing data,\nso the metrics can only be available after the job has been finished\nor has errored.\nFor usage metrics during processing, metrics can better be added to the\nlogs (e.g. `GET /jobs/{job_id}/logs`) with the same schema.",
    )

    @validator("job_id", pre=True, always=True)
    def as_str(cls, v):
        if isinstance(v, str):
            return v
        elif isinstance(v, uuid.UUID):
            return v.__str__()
        else:
            raise ValueError(f"Job id can only be of type UUID or str.")

    class Config:
        allow_population_by_field_name = True


class JobsGetResponse(BaseModel):
    jobs: list[BatchJob]
    links: list[Link]
