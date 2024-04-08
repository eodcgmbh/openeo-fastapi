# Table of Contents

* [openeo\_fastapi.client.psql.models](#openeo_fastapi.client.psql.models)
  * [UserORM](#openeo_fastapi.client.psql.models.UserORM)
    * [user\_id](#openeo_fastapi.client.psql.models.UserORM.user_id)
    * [oidc\_sub](#openeo_fastapi.client.psql.models.UserORM.oidc_sub)
    * [created\_at](#openeo_fastapi.client.psql.models.UserORM.created_at)
  * [JobORM](#openeo_fastapi.client.psql.models.JobORM)
    * [job\_id](#openeo_fastapi.client.psql.models.JobORM.job_id)
    * [process](#openeo_fastapi.client.psql.models.JobORM.process)
    * [status](#openeo_fastapi.client.psql.models.JobORM.status)
    * [user\_id](#openeo_fastapi.client.psql.models.JobORM.user_id)
    * [created](#openeo_fastapi.client.psql.models.JobORM.created)
    * [title](#openeo_fastapi.client.psql.models.JobORM.title)
    * [description](#openeo_fastapi.client.psql.models.JobORM.description)
    * [synchronous](#openeo_fastapi.client.psql.models.JobORM.synchronous)
  * [UdpORM](#openeo_fastapi.client.psql.models.UdpORM)
    * [id](#openeo_fastapi.client.psql.models.UdpORM.id)
    * [user\_id](#openeo_fastapi.client.psql.models.UdpORM.user_id)
    * [process\_graph](#openeo_fastapi.client.psql.models.UdpORM.process_graph)
    * [created](#openeo_fastapi.client.psql.models.UdpORM.created)
    * [parameters](#openeo_fastapi.client.psql.models.UdpORM.parameters)
    * [returns](#openeo_fastapi.client.psql.models.UdpORM.returns)
    * [summary](#openeo_fastapi.client.psql.models.UdpORM.summary)
    * [description](#openeo_fastapi.client.psql.models.UdpORM.description)

<a id="openeo_fastapi.client.psql.models"></a>

# openeo\_fastapi.client.psql.models

ORM definitions for defining and storing the associated data in the databse.

<a id="openeo_fastapi.client.psql.models.UserORM"></a>

## UserORM Objects

```python
class UserORM(BASE)
```

ORM for the user table.

<a id="openeo_fastapi.client.psql.models.UserORM.user_id"></a>

#### user\_id

UUID of the user.

<a id="openeo_fastapi.client.psql.models.UserORM.oidc_sub"></a>

#### oidc\_sub

OIDC substring of the user.

<a id="openeo_fastapi.client.psql.models.UserORM.created_at"></a>

#### created\_at

The datetime the user was created.

<a id="openeo_fastapi.client.psql.models.JobORM"></a>

## JobORM Objects

```python
class JobORM(BASE)
```

ORM for the job table.

<a id="openeo_fastapi.client.psql.models.JobORM.job_id"></a>

#### job\_id

UUID of the job.

<a id="openeo_fastapi.client.psql.models.JobORM.process"></a>

#### process

The process graph for this job.

<a id="openeo_fastapi.client.psql.models.JobORM.status"></a>

#### status

The status of the Job.

<a id="openeo_fastapi.client.psql.models.JobORM.user_id"></a>

#### user\_id

The UUID of the user that owns this job.

<a id="openeo_fastapi.client.psql.models.JobORM.created"></a>

#### created

The datetime the job was created.

<a id="openeo_fastapi.client.psql.models.JobORM.title"></a>

#### title

The title of the job.

<a id="openeo_fastapi.client.psql.models.JobORM.description"></a>

#### description

The job description.

<a id="openeo_fastapi.client.psql.models.JobORM.synchronous"></a>

#### synchronous

If the Job is synchronous.

<a id="openeo_fastapi.client.psql.models.UdpORM"></a>

## UdpORM Objects

```python
class UdpORM(BASE)
```

ORM for the UDPS table.

<a id="openeo_fastapi.client.psql.models.UdpORM.id"></a>

#### id

The string name of the UDP. CPK with user_id. Different users can use the same string for id.

<a id="openeo_fastapi.client.psql.models.UdpORM.user_id"></a>

#### user\_id

The UUID of the user that owns this UDP.

<a id="openeo_fastapi.client.psql.models.UdpORM.process_graph"></a>

#### process\_graph

The process graph of the UDP.

<a id="openeo_fastapi.client.psql.models.UdpORM.created"></a>

#### created

The datetime the UDP was created.

<a id="openeo_fastapi.client.psql.models.UdpORM.parameters"></a>

#### parameters

The parameters of the UDP.

<a id="openeo_fastapi.client.psql.models.UdpORM.returns"></a>

#### returns

The return types of the UDP.

<a id="openeo_fastapi.client.psql.models.UdpORM.summary"></a>

#### summary

A summary of the UPD.

<a id="openeo_fastapi.client.psql.models.UdpORM.description"></a>

#### description

A description of what the UDP is intended to do.

