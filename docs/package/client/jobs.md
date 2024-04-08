# Table of Contents

* [openeo\_fastapi.client.jobs](#openeo_fastapi.client.jobs)
  * [Job](#openeo_fastapi.client.jobs.Job)
    * [job\_id](#openeo_fastapi.client.jobs.Job.job_id)
    * [Config](#openeo_fastapi.client.jobs.Job.Config)
    * [get\_orm](#openeo_fastapi.client.jobs.Job.get_orm)
    * [patch](#openeo_fastapi.client.jobs.Job.patch)
  * [JobsRegister](#openeo_fastapi.client.jobs.JobsRegister)
    * [\_\_init\_\_](#openeo_fastapi.client.jobs.JobsRegister.__init__)
    * [list\_jobs](#openeo_fastapi.client.jobs.JobsRegister.list_jobs)
    * [create\_job](#openeo_fastapi.client.jobs.JobsRegister.create_job)
    * [update\_job](#openeo_fastapi.client.jobs.JobsRegister.update_job)
    * [get\_job](#openeo_fastapi.client.jobs.JobsRegister.get_job)
    * [delete\_job](#openeo_fastapi.client.jobs.JobsRegister.delete_job)
    * [estimate](#openeo_fastapi.client.jobs.JobsRegister.estimate)
    * [logs](#openeo_fastapi.client.jobs.JobsRegister.logs)
    * [get\_results](#openeo_fastapi.client.jobs.JobsRegister.get_results)
    * [start\_job](#openeo_fastapi.client.jobs.JobsRegister.start_job)
    * [cancel\_job](#openeo_fastapi.client.jobs.JobsRegister.cancel_job)
    * [delete\_job](#openeo_fastapi.client.jobs.JobsRegister.delete_job)
    * [process\_sync\_job](#openeo_fastapi.client.jobs.JobsRegister.process_sync_job)

<a id="openeo_fastapi.client.jobs"></a>

# openeo\_fastapi.client.jobs

Class and model to define the framework and partial application logic for interacting with Jobs.

Classes:
    - JobsRegister: Framework for defining and extending the logic for working with BatchJobs.
    - Job: The pydantic model used as an in memory representation of an OpenEO Job.

<a id="openeo_fastapi.client.jobs.Job"></a>

## Job Objects

```python
class Job(BaseModel)
```

Pydantic model representing an OpenEO Job.

<a id="openeo_fastapi.client.jobs.Job.job_id"></a>

#### job\_id



<a id="openeo_fastapi.client.jobs.Job.Config"></a>

## Config Objects

```python
class Config()
```

Pydantic model class config.

<a id="openeo_fastapi.client.jobs.Job.get_orm"></a>

#### get\_orm

```python
@classmethod
def get_orm(cls)
```

Get the ORM model for this pydantic model.

<a id="openeo_fastapi.client.jobs.Job.patch"></a>

#### patch

```python
def patch(patch: Any)
```

Update pydantic model with changed fields from a new model instance.

<a id="openeo_fastapi.client.jobs.JobsRegister"></a>

## JobsRegister Objects

```python
class JobsRegister(EndpointRegister)
```

The JobRegister to regulate the application logic for the API behaviour.

<a id="openeo_fastapi.client.jobs.JobsRegister.__init__"></a>

#### \_\_init\_\_

```python
def __init__(settings, links) -> None
```

Initialize the JobRegister.

**Arguments**:

- `settings` _AppSettings_ - The AppSettings that the application will use.
- `links` _Links_ - The Links to be used in some function responses.

<a id="openeo_fastapi.client.jobs.JobsRegister.list_jobs"></a>

#### list\_jobs

```python
def list_jobs(limit: Optional[int] = 10,
              user: User = Depends(Authenticator.validate))
```

List the user's most recent BatchJobs.

**Arguments**:

- `limit` _int_ - The limit to apply to the length of the list.
- `user` _User_ - The User returned from the Authenticator.
  

**Returns**:

- `JobsGetResponse` - A list of the user's BatchJobs.

<a id="openeo_fastapi.client.jobs.JobsRegister.create_job"></a>

#### create\_job

```python
def create_job(body: JobsRequest,
               user: User = Depends(Authenticator.validate))
```

Create a new BatchJob.

**Arguments**:

- `body` _JobsRequest_ - The Job Request that should be used to create the new BatchJob.
- `user` _User_ - The User returned from the Authenticator.
  

**Returns**:

- `Response` - A general FastApi response to signify the changes where made as expected. Specific response
  headers need to be set in this response to ensure certain behaviours when being used by OpenEO client modules.

<a id="openeo_fastapi.client.jobs.JobsRegister.update_job"></a>

#### update\_job

```python
def update_job(job_id: uuid.UUID,
               body: JobsRequest,
               user: User = Depends(Authenticator.validate))
```

Update the specified BatchJob with the contents of the provided JobsRequest.

**Arguments**:

- `job_id` _JobId_ - A UUID job id.
- `body` _JobsRequest_ - The Job Request that should be used to update the new BatchJob.
- `user` _User_ - The User returned from the Authenticator.
  

**Raises**:

- `HTTPException` - Raises an exception with relevant status code and descriptive message of failure.
  

**Returns**:

- `Response` - A general FastApi response to signify the changes where made as expected.

<a id="openeo_fastapi.client.jobs.JobsRegister.get_job"></a>

#### get\_job

```python
def get_job(job_id: uuid.UUID, user: User = Depends(Authenticator.validate))
```

Get and return the metadata for the BatchJob.

**Arguments**:

- `job_id` _JobId_ - A UUID job id.
- `user` _User_ - The User returned from the Authenticator.
  

**Raises**:

- `HTTPException` - Raises an exception with relevant status code and descriptive message of failure.
  

**Returns**:

- `BatchJob` - The metadata for the requested BatchJob.

<a id="openeo_fastapi.client.jobs.JobsRegister.delete_job"></a>

#### delete\_job

```python
def delete_job(job_id: uuid.UUID,
               user: User = Depends(Authenticator.validate))
```

Delete the BatchJob.

**Arguments**:

- `job_id` _JobId_ - A UUID job id.
- `body` _JobsRequest_ - The Job Request that should be used to create the new BatchJob.
- `user` _User_ - The User returned from the Authenticator.
  

**Raises**:

- `HTTPException` - Raises an exception with relevant status code and descriptive message of failure.

<a id="openeo_fastapi.client.jobs.JobsRegister.estimate"></a>

#### estimate

```python
def estimate(job_id: uuid.UUID, user: User = Depends(Authenticator.validate))
```

Estimate the cost for the BatchJob.

**Arguments**:

- `job_id` _JobId_ - A UUID job id.
- `body` _JobsRequest_ - The Job Request that should be used to create the new BatchJob.
- `user` _User_ - The User returned from the Authenticator.
  

**Raises**:

- `HTTPException` - Raises an exception with relevant status code and descriptive message of failure.

<a id="openeo_fastapi.client.jobs.JobsRegister.logs"></a>

#### logs

```python
def logs(job_id: uuid.UUID, user: User = Depends(Authenticator.validate))
```

Get the logs for the BatchJob.

**Arguments**:

- `job_id` _JobId_ - A UUID job id.
- `body` _JobsRequest_ - The Job Request that should be used to create the new BatchJob.
- `user` _User_ - The User returned from the Authenticator.
  

**Raises**:

- `HTTPException` - Raises an exception with relevant status code and descriptive message of failure.

<a id="openeo_fastapi.client.jobs.JobsRegister.get_results"></a>

#### get\_results

```python
def get_results(job_id: uuid.UUID,
                user: User = Depends(Authenticator.validate))
```

Get the results for the BatchJob.

**Arguments**:

- `job_id` _JobId_ - A UUID job id.
- `body` _JobsRequest_ - The Job Request that should be used to create the new BatchJob.
- `user` _User_ - The User returned from the Authenticator.
  

**Raises**:

- `HTTPException` - Raises an exception with relevant status code and descriptive message of failure.

<a id="openeo_fastapi.client.jobs.JobsRegister.start_job"></a>

#### start\_job

```python
def start_job(job_id: uuid.UUID, user: User = Depends(Authenticator.validate))
```

Start the processing for the BatchJob.

**Arguments**:

- `job_id` _JobId_ - A UUID job id.
- `body` _JobsRequest_ - The Job Request that should be used to create the new BatchJob.
- `user` _User_ - The User returned from the Authenticator.
  

**Raises**:

- `HTTPException` - Raises an exception with relevant status code and descriptive message of failure.

<a id="openeo_fastapi.client.jobs.JobsRegister.cancel_job"></a>

#### cancel\_job

```python
def cancel_job(job_id: uuid.UUID,
               user: User = Depends(Authenticator.validate))
```

Cancel the processing of the BatchJob.

**Arguments**:

- `job_id` _JobId_ - A UUID job id.
- `user` _User_ - The User returned from the Authenticator.
  

**Raises**:

- `HTTPException` - Raises an exception with relevant status code and descriptive message of failure.

<a id="openeo_fastapi.client.jobs.JobsRegister.delete_job"></a>

#### delete\_job

```python
def delete_job(job_id: uuid.UUID,
               user: User = Depends(Authenticator.validate))
```

Delete the BatchJob from the database.

**Arguments**:

- `job_id` _JobId_ - A UUID job id.
- `body` _JobsRequest_ - The Job Request that should be used to create the new BatchJob.
- `user` _User_ - The User returned from the Authenticator.
  

**Raises**:

- `HTTPException` - Raises an exception with relevant status code and descriptive message of failure.

<a id="openeo_fastapi.client.jobs.JobsRegister.process_sync_job"></a>

#### process\_sync\_job

```python
def process_sync_job(body: JobsRequest = JobsRequest(),
                     user: User = Depends(Authenticator.validate))
```

Start the processing of a synchronous Job.

**Arguments**:

- `body` _JobsRequest_ - The Job Request that should be used to create the new BatchJob.
- `user` _User_ - The User returned from the Authenticator.
  

**Raises**:

- `HTTPException` - Raises an exception with relevant status code and descriptive message of failure.

