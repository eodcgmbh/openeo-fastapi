"""Class and model to define the framework and partial application logic for interacting with Jobs.

Classes:
    - JobsRegister: Framework for defining and extending the logic for working with BatchJobs.
    - Job: The pydantic model used as an in memory representation of an OpenEO Job.
"""
import datetime
import uuid
from typing import Any, Optional

from fastapi import Depends, Response
from fastapi.exceptions import HTTPException
from pydantic import BaseModel, Extra
from sqlalchemy.exc import IntegrityError

from openeo_fastapi.api.models import (
    BatchJob,
    JobsGetResponse,
    JobsRequest,
    ProcessGraphWithMetadata,
)
from openeo_fastapi.api.types import Endpoint, Error, Status
from openeo_fastapi.client.auth import Authenticator, User
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
    """Pydantic model representing an OpenEO Job."""

    job_id: uuid.UUID
    """"""
    process: ProcessGraphWithMetadata
    status: Status
    user_id: uuid.UUID
    created: datetime.datetime
    title: Optional[str]
    description: Optional[str]
    synchronous: bool = False

    class Config:
        """Pydantic model class config."""
        orm_mode = True
        arbitrary_types_allowed = True
        extra = Extra.ignore

    @classmethod
    def get_orm(cls):
        """Get the ORM model for this pydantic model."""
        return JobORM

    def patch(self, patch: Any):
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
    """The JobRegister to regulate the application logic for the API behaviour.
    """

    def __init__(self, settings, links) -> None:
        """Initialize the JobRegister.

        Args:
            settings (AppSettings): The AppSettings that the application will use.
            links (Links): The Links to be used in some function responses.
        """
        super().__init__()
        self.endpoints = self._initialize_endpoints()
        self.settings = settings
        self.links = links

    def _initialize_endpoints(self) -> list[Endpoint]:
        """Initialize the endpoints for the register.

        Returns:
            list[Endpoint]: The default list of job endpoints which are packaged with the module.
        """
        return JOBS_ENDPOINTS

    # TODO Apply the limit
    def list_jobs(
        self, limit: Optional[int] = 10, user: User = Depends(Authenticator.validate)
    ):
        """List the user's most recent BatchJobs.

        Args:
            limit (int): The limit to apply to the length of the list.
            user (User): The User returned from the Authenticator.

        Returns:
            JobsGetResponse: A list of the user's BatchJobs.
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
        """Create a new BatchJob.

        Args:
            body (JobsRequest): The Job Request that should be used to create the new BatchJob.
            user (User): The User returned from the Authenticator.

        Returns:
            Response: A general FastApi response to signify the changes where made as expected. Specific response
            headers need to be set in this response to ensure certain behaviours when being used by OpenEO client modules.
        """
        job_id = uuid.uuid4()

        if not body.process.id:
            auto_name_size = 16
            body.process.id = uuid.uuid4().hex[:auto_name_size].upper()

        # Create the job
        job = Job(
            job_id=job_id,
            process=body.process,
            status=Status.created,
            title=body.title,
            description=body.description,
            user_id=user.user_id,
            created=datetime.datetime.now(),
        )

        try:
            create(create_object=job)
        except IntegrityError:
            raise HTTPException(
                status_code=500,
                detail=Error(code="Internal", message=f"The job {job.job_id} already exists."),
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
        """Update the specified BatchJob with the contents of the provided JobsRequest.

        Args:
            job_id (JobId): A UUID job id.
            body (JobsRequest): The Job Request that should be used to update the new BatchJob.
            user (User): The User returned from the Authenticator.

        Raises:
            HTTPException: Raises an exception with relevant status code and descriptive message of failure.

        Returns:
            Response: A general FastApi response to signify the changes where made as expected.
        """
        # Patch the job with any changes
        job = get(get_model=Job, primary_key=job_id)
        # TODO Add check to ensure user owns job.
        # TODO Add job locked raise if status is running or queued.
        patched_job = job.patch(body)

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
        """Get and return the metadata for the BatchJob.

        Args:
            job_id (JobId): A UUID job id.
            user (User): The User returned from the Authenticator.

        Raises:
            HTTPException: Raises an exception with relevant status code and descriptive message of failure.

        Returns:
            BatchJob: The metadata for the requested BatchJob.
        """
        job = get(get_model=Job, primary_key=job_id)
        if not job:
            raise HTTPException(
                status_code=404, detail=f"No job found with id: {job_id}"
            )

        return BatchJob(id=job.job_id.__str__(), **job.dict())

    def delete_job(
        self, job_id: uuid.UUID, user: User = Depends(Authenticator.validate)
    ):
        """Delete the BatchJob.

        Args:
            job_id (JobId): A UUID job id.
            body (JobsRequest): The Job Request that should be used to create the new BatchJob.
            user (User): The User returned from the Authenticator.

        Raises:
            HTTPException: Raises an exception with relevant status code and descriptive message of failure.

        """
        raise HTTPException(
            status_code=501,
            detail=Error(code="FeatureUnsupported", message="Feature not supported."),
        )

    def estimate(self, job_id: uuid.UUID, user: User = Depends(Authenticator.validate)):
        """Estimate the cost for the BatchJob.

        Args:
            job_id (JobId): A UUID job id.
            body (JobsRequest): The Job Request that should be used to create the new BatchJob.
            user (User): The User returned from the Authenticator.

        Raises:
            HTTPException: Raises an exception with relevant status code and descriptive message of failure.

        """
        raise HTTPException(
            status_code=501,
            detail=Error(code="FeatureUnsupported", message="Feature not supported."),
        )

    def logs(self, job_id: uuid.UUID, user: User = Depends(Authenticator.validate)):
        """Get the logs for the BatchJob.

        Args:
            job_id (JobId): A UUID job id.
            body (JobsRequest): The Job Request that should be used to create the new BatchJob.
            user (User): The User returned from the Authenticator.

        Raises:
            HTTPException: Raises an exception with relevant status code and descriptive message of failure.

        """
        raise HTTPException(
            status_code=501,
            detail=Error(code="FeatureUnsupported", message="Feature not supported."),
        )

    def get_results(
        self, job_id: uuid.UUID, user: User = Depends(Authenticator.validate)
    ):
        """Get the results for the BatchJob.

        Args:
            job_id (JobId): A UUID job id.
            body (JobsRequest): The Job Request that should be used to create the new BatchJob.
            user (User): The User returned from the Authenticator.

        Raises:
            HTTPException: Raises an exception with relevant status code and descriptive message of failure.

        """
        raise HTTPException(
            status_code=501,
            detail=Error(code="FeatureUnsupported", message="Feature not supported."),
        )

    def start_job(
        self, job_id: uuid.UUID, user: User = Depends(Authenticator.validate)
    ):
        """Start the processing for the BatchJob.

        Args:
            job_id (JobId): A UUID job id.
            body (JobsRequest): The Job Request that should be used to create the new BatchJob.
            user (User): The User returned from the Authenticator.

        Raises:
            HTTPException: Raises an exception with relevant status code and descriptive message of failure.

        """
        raise HTTPException(
            status_code=501,
            detail=Error(code="FeatureUnsupported", message="Feature not supported."),
        )

    def cancel_job(
        self, job_id: uuid.UUID, user: User = Depends(Authenticator.validate)
    ):
        """Cancel the processing of the BatchJob.

        Args:
            job_id (JobId): A UUID job id.
            user (User): The User returned from the Authenticator.

        Raises:
            HTTPException: Raises an exception with relevant status code and descriptive message of failure.

        """
        raise HTTPException(
            status_code=501,
            detail=Error(code="FeatureUnsupported", message="Feature not supported."),
        )

    def delete_job(
        self, job_id: uuid.UUID, user: User = Depends(Authenticator.validate)
    ):
        """Delete the BatchJob from the database.

        Args:
            job_id (JobId): A UUID job id.
            body (JobsRequest): The Job Request that should be used to create the new BatchJob.
            user (User): The User returned from the Authenticator.

        Raises:
            HTTPException: Raises an exception with relevant status code and descriptive message of failure.

        """
        raise HTTPException(
            status_code=501,
            detail=Error(code="FeatureUnsupported", message="Feature not supported."),
        )

    def process_sync_job(self, body: JobsRequest = JobsRequest(), user: User = Depends(Authenticator.validate)):
        """Start the processing of a synchronous Job.

        Args:
            body (JobsRequest): The Job Request that should be used to create the new BatchJob.
            user (User): The User returned from the Authenticator.

        Raises:
            HTTPException: Raises an exception with relevant status code and descriptive message of failure.
                        
        """
        raise HTTPException(
            status_code=501,
            detail=Error(code="FeatureUnsupported", message="Feature not supported."),
        )
