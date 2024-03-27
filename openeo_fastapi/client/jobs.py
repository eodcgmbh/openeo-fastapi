import datetime
import uuid
from typing import Optional

from fastapi import Depends, Response
from fastapi.exceptions import HTTPException
from pydantic import BaseModel, Extra

from openeo_fastapi.api.requests import JobsRequest
from openeo_fastapi.api.responses import (
    BatchJob,
    JobsGetResponse,
    ProcessGraphWithMetadata,
)
from openeo_fastapi.api.types import Endpoint, Error, Status
from openeo_fastapi.client.auth import Authenticator, User
from openeo_fastapi.client.processes import ProcessGraph
from openeo_fastapi.client.psql.engine import Filter, _list, create, get, modify
from openeo_fastapi.client.psql.models import JobORM
from openeo_fastapi.client.register import EndpointRegister

JOBS_ENDPOINTS = [
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
    Endpoint(
        path="/jobs/{job_id}/results",
        methods=["GET"],
    ),
    Endpoint(
        path="/jobs/{job_id}/results",
        methods=["POST"],
    ),
    Endpoint(
        path="/jobs/{job_id}/results",
        methods=["DELETE"],
    ),
]


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


class JobsRegister(EndpointRegister):
    def __init__(self, settings, links) -> None:
        super().__init__()
        self.endpoints = self._initialize_endpoints()
        self.settings = settings
        self.links = links

    def _initialize_endpoints(self) -> list[Endpoint]:
        return JOBS_ENDPOINTS

    def list_jobs(
        self, limit: Optional[int] = 10, user: User = Depends(Authenticator.validate)
    ):
        """_summary_

        Args:
            job_id (JobId): _description_
            body (JobsRequest): _description_
            user (User): _description_

        Raises:
            HTTPException: _description_
            HTTPException: _description_
            HTTPException: _description_
            HTTPException: _description_

        Returns:
            _type_: _description_
        """
        # Invoke list function from handler
        _filter = Filter(column_name="user_id", value=user.user_id)

        job_list = _list(list_model=Job, filter_with=_filter)

        # TODO BatchJob and Job describe the same thing, these want to be harmonized.
        jobs = [BatchJob(**job.dict()) for job in job_list if not job.synchronous]

        return JobsGetResponse(jobs=jobs, links=[])

    def create_job(
        self, body: JobsRequest, user: User = Depends(Authenticator.validate)
    ):
        """_summary_

        Args:
            job_id (JobId): _description_
            body (JobsRequest): _description_
            user (User): _description_

        Raises:
            HTTPException: _description_
            HTTPException: _description_
            HTTPException: _description_
            HTTPException: _description_

        Returns:
            _type_: _description_
        """
        job_id = uuid.uuid4()

        if not body.process.process_graph_id:
            auto_name_size = 16
            body.process.process_graph_id = uuid.uuid4().hex[:auto_name_size].upper()

        # Create the job
        job = Job(
            job_id=job_id,
            process_graph_id=body.process.process_graph_id,
            status=Status.created,
            user_id=user.user_id,
            created=datetime.datetime.now(),
        )

        # Create the process graph
        process_graph = ProcessGraph(
            user_id=user.user_id, created=datetime.datetime.now(), **body.process.dict()
        )

        # Call engine create
        created = create(create_object=process_graph)
        if not created:
            raise HTTPException(
                status_code=500,
                detail="Job creation could not add the process graph for this job.",
            )

        created_job = create(create_object=job)

        if not created_job:
            raise HTTPException(
                status_code=500,
                detail="Job creation could not add the job to the database.",
            )
        return Response(
            status_code=201,
            headers={
                "Location": f"{self.settings.API_DNS}{self.settings.OPENEO_PREFIX}/jobs/{job_id.__str__()}",
                "OpenEO-Identifier": job_id.__str__(),
                "access-control-allow-headers": "Accept-Ranges, Content-Encoding, Content-Range, Link, Location, OpenEO-Costs, OpenEO-Identifier",
                "access-control-expose-headers": "Accept-Ranges, Content-Encoding, Content-Range, Link, Location, OpenEO-Costs, OpenEO-Identifier",
            },
        )

    def update_job(
        self,
        job_id: uuid.UUID,
        body: JobsRequest,
        user: User = Depends(Authenticator.validate),
    ):
        """_summary_

        Args:
            job_id (JobId): _description_
            body (JobsRequest): _description_
            user (User): _description_

        Raises:
            HTTPException: _description_
            HTTPException: _description_
            HTTPException: _description_
            HTTPException: _description_

        Returns:
            _type_: _description_
        """
        # Patch the job with any changes
        job = get(get_model=Job, primary_key=job_id)
        # TODO Add check to ensure user owns job.
        # TODO Add job locked raise if status is running or queued.
        patched_job = job.patch(body)

        # Get process graph with metadata
        process_graph = get(
            get_model=ProcessGraph,
            primary_key=job.process_graph_id,
        )
        # If there is a new process graph in the request body, and it already exists try to update the one in memory. Else create a new one!
        if body.process:
            if process_graph.id == body.process.id:
                patched_process_graph = process_graph.patch(body.process)
                # if it's changed call engine to modify
                if process_graph != patched_process_graph:
                    modified = modify(modify_object=patched_process_graph)
                    if not modified:
                        raise HTTPException(
                            status_code=500,
                            detail="Server could not update the the job with the new process graph.",
                        )
            else:
                # Create the new process graph
                new_process_graph = ProcessGraph(
                    user_id=user.user_id,
                    created=datetime.datetime.now(),
                    **body.process.dict(),
                )

                # Check a process graph with this id does not already exist
                existing_process_graph = get(
                    get_model=ProcessGraph,
                    primary_key=new_process_graph.id,
                )
                if existing_process_graph:
                    raise HTTPException(
                        status_code=500,
                        detail=f"Server could not create new process graph, Process graph with {existing_process_graph.process_graph_id} already exists!",
                    )

                # Call engine create
                created = create(create_object=new_process_graph)
                if not created:
                    raise HTTPException(
                        status_code=500,
                        detail="Server could not create a new process graph for the job.",
                    )

                # Update job id with new process_graph_id
                patched_job.process_graph_id = new_process_graph.id

        # Call engine modify with a new model!
        modified = modify(modify_object=patched_job)
        if not modified:
            raise HTTPException(
                status_code=500,
                detail="Server could not update the the job with the new process graph.",
            )

        return Response(
            status_code=204, content="Changes to the job applied successfully."
        )

    def get_job(self, job_id: uuid.UUID, user: User = Depends(Authenticator.validate)):
        """_summary_

        Args:
            job_id (JobId): _description_
            body (JobsRequest): _description_
            user (User): _description_

        Raises:
            HTTPException: _description_
            HTTPException: _description_
            HTTPException: _description_
            HTTPException: _description_

        Returns:
            _type_: _description_
        """
        job = get(get_model=Job, primary_key=job_id)
        if not job:
            raise HTTPException(
                status_code=404, detail=f"No job found with id: {job_id}"
            )

        pg = get(
            get_model=ProcessGraph,
            primary_key=job.process_graph_id,
        )
        process_graph = ProcessGraphWithMetadata(**pg.dict(by_alias=False))

        return BatchJob(id=job.job_id.__str__(), process=process_graph, **job.dict())

    def delete_job(
        self, job_id: uuid.UUID, user: User = Depends(Authenticator.validate)
    ):
        """_summary_

        Args:
            job_id (JobId): _description_
            body (JobsRequest): _description_
            user (User): _description_

        Raises:
            HTTPException: _description_
            HTTPException: _description_
            HTTPException: _description_
            HTTPException: _description_

        Returns:
            _type_: _description_
        """
        raise HTTPException(
            status_code=501,
            detail=Error(code="FeatureUnsupported", message="Feature not supported."),
        )

    def estimate(self, job_id: uuid.UUID, user: User = Depends(Authenticator.validate)):
        """_summary_

        Args:
            job_id (JobId): _description_
            body (JobsRequest): _description_
            user (User): _description_

        Raises:
            HTTPException: _description_
            HTTPException: _description_
            HTTPException: _description_
            HTTPException: _description_

        Returns:
            _type_: _description_
        """
        raise HTTPException(
            status_code=501,
            detail=Error(code="FeatureUnsupported", message="Feature not supported."),
        )

    def logs(self, job_id: uuid.UUID, user: User = Depends(Authenticator.validate)):
        """_summary_

        Args:
            job_id (JobId): _description_
            body (JobsRequest): _description_
            user (User): _description_

        Raises:
            HTTPException: _description_
            HTTPException: _description_
            HTTPException: _description_
            HTTPException: _description_

        Returns:
            _type_: _description_
        """
        raise HTTPException(
            status_code=501,
            detail=Error(code="FeatureUnsupported", message="Feature not supported."),
        )

    def get_results(
        self, job_id: uuid.UUID, user: User = Depends(Authenticator.validate)
    ):
        """_summary_

        Args:
            job_id (JobId): _description_
            body (JobsRequest): _description_
            user (User): _description_

        Raises:
            HTTPException: _description_
            HTTPException: _description_
            HTTPException: _description_
            HTTPException: _description_

        Returns:
            _type_: _description_
        """
        raise HTTPException(
            status_code=501,
            detail=Error(code="FeatureUnsupported", message="Feature not supported."),
        )

    def start_job(
        self, job_id: uuid.UUID, user: User = Depends(Authenticator.validate)
    ):
        """_summary_

        Args:
            job_id (JobId): _description_
            body (JobsRequest): _description_
            user (User): _description_

        Raises:
            HTTPException: _description_
            HTTPException: _description_
            HTTPException: _description_
            HTTPException: _description_

        Returns:
            _type_: _description_
        """
        raise HTTPException(
            status_code=501,
            detail=Error(code="FeatureUnsupported", message="Feature not supported."),
        )

    def cancel_job(
        self, job_id: uuid.UUID, user: User = Depends(Authenticator.validate)
    ):
        """_summary_

        Args:
            job_id (JobId): _description_
            body (JobsRequest): _description_
            user (User): _description_

        Raises:
            HTTPException: _description_
            HTTPException: _description_
            HTTPException: _description_
            HTTPException: _description_

        Returns:
            _type_: _description_
        """
        raise HTTPException(
            status_code=501,
            detail=Error(code="FeatureUnsupported", message="Feature not supported."),
        )

    def delete_job(
        self, job_id: uuid.UUID, user: User = Depends(Authenticator.validate)
    ):
        """_summary_

        Args:
            job_id (JobId): _description_
            body (JobsRequest): _description_
            user (User): _description_

        Raises:
            HTTPException: _description_
            HTTPException: _description_
            HTTPException: _description_
            HTTPException: _description_

        Returns:
            _type_: _description_
        """
        raise HTTPException(
            status_code=501,
            detail=Error(code="FeatureUnsupported", message="Feature not supported."),
        )

    def process_sync_job(self, user: User = Depends(Authenticator.validate)):
        """_summary_

        Args:
            job_id (JobId): _description_
            body (JobsRequest): _description_
            user (User): _description_

        Raises:
            HTTPException: _description_
            HTTPException: _description_
            HTTPException: _description_
            HTTPException: _description_

        Returns:
            _type_: _description_
        """
        raise HTTPException(
            status_code=501,
            detail=Error(code="FeatureUnsupported", message="Feature not supported."),
        )
