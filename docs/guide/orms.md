## Extending the Object Relational models.

Currently it's possible to extend the object relational models that the api uses in order to support extra values a backend might want to includse in any EndpointRegisters.

## How to extend the models.

In order to effectively use the extended models, you need to update the models.py file found in the alembic directory. After updating the models.py file, you will need to manually update the endpoints where you would like the new model to be used. This is a current pain point, and it would be good to improve this in the future.

#### Original - models.py

    from openeo_fastapi.client.psql.settings import BASE
    from openeo_fastapi.client.psql.models import *

    metadata = BASE.metadata

#### Updated - models.py


    from typing import Optional
    from openeo_fastapi.client.jobs import Job
    from openeo_fastapi.client.psql.settings import BASE
    from openeo_fastapi.client.psql.models import *

    class ExtendedJobORM(JobORM):

        special_string = Column(VARCHAR, nullable=True)
        """A very special string."""


    class ExtendedJob(Job):

        special_string: Optional[str]
        """A very special string."""

        @classmethod
        def get_orm(cls):
            return ExtendedJobORM


    metadata = BASE.metadata

#### Using extended model

In order use the class ExtendedJob, we will need to extend the register. The example below extends the JobRegister and edits the create_job function to create the ExtendedJob and includes setting the value for the new parameter. You will need to version the database in order for the new model to work, and additionally add the NewJobsRegister to the app instance [See Registers](/openeo-fastapi/guide/registers/).

    ...
    from openeo_fastapi.client.jobs import JobsRegister
    from openeo_argoworkflows_api.psql.models import ExtendedJob

    class NewJobsRegister(JobsRegister):

        def __init__(self, settings, links) -> None:
            super().__init__(settings, links)


        def create_job(
            self, body: JobsRequest
        ):
            """Create a new ExtendedJob.
            """

            # Create the job
            job = ExtendedJob(
                job_id=job_id,
                process=body.process,
                status=Status.created,
                title=body.title,
                description=body.description,
                user_id=user.user_id,
                created=datetime.datetime.now(),
                special_string="A new type of job."
            )

            engine.create(create_object=job)

            return Response(
                status_code=201,
            )
