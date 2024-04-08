# Table of Contents

* [openeo\_fastapi.api.models](#openeo_fastapi.api.models)
  * [Capabilities](#openeo_fastapi.api.models.Capabilities)
  * [MeGetResponse](#openeo_fastapi.api.models.MeGetResponse)
  * [ConformanceGetResponse](#openeo_fastapi.api.models.ConformanceGetResponse)
  * [WellKnownOpeneoGetResponse](#openeo_fastapi.api.models.WellKnownOpeneoGetResponse)
  * [UdfRuntimesGetResponse](#openeo_fastapi.api.models.UdfRuntimesGetResponse)
  * [Collection](#openeo_fastapi.api.models.Collection)
  * [Collections](#openeo_fastapi.api.models.Collections)
  * [ProcessesGetResponse](#openeo_fastapi.api.models.ProcessesGetResponse)
  * [ProcessGraphWithMetadata](#openeo_fastapi.api.models.ProcessGraphWithMetadata)
  * [ProcessGraphsGetResponse](#openeo_fastapi.api.models.ProcessGraphsGetResponse)
  * [ValidationPostResponse](#openeo_fastapi.api.models.ValidationPostResponse)
  * [BatchJob](#openeo_fastapi.api.models.BatchJob)
  * [JobsGetResponse](#openeo_fastapi.api.models.JobsGetResponse)
  * [JobsGetLogsResponse](#openeo_fastapi.api.models.JobsGetLogsResponse)
  * [JobsGetEstimateGetResponse](#openeo_fastapi.api.models.JobsGetEstimateGetResponse)
  * [JobsRequest](#openeo_fastapi.api.models.JobsRequest)
  * [FilesGetResponse](#openeo_fastapi.api.models.FilesGetResponse)
  * [FileFormatsGetResponse](#openeo_fastapi.api.models.FileFormatsGetResponse)

<a id="openeo_fastapi.api.models"></a>

# openeo\_fastapi.api.models

Pydantic Models describing different api request and response bodies.

<a id="openeo_fastapi.api.models.Capabilities"></a>

## Capabilities Objects

```python
class Capabilities(BaseModel)
```

Response model for GET (/).

<a id="openeo_fastapi.api.models.MeGetResponse"></a>

## MeGetResponse Objects

```python
class MeGetResponse(BaseModel)
```

Response model for GET (/me).

<a id="openeo_fastapi.api.models.ConformanceGetResponse"></a>

## ConformanceGetResponse Objects

```python
class ConformanceGetResponse(BaseModel)
```

Response model for GET (/conformance).

<a id="openeo_fastapi.api.models.WellKnownOpeneoGetResponse"></a>

## WellKnownOpeneoGetResponse Objects

```python
class WellKnownOpeneoGetResponse(BaseModel)
```

Response model for GET (/.well-known/openeo).

<a id="openeo_fastapi.api.models.UdfRuntimesGetResponse"></a>

## UdfRuntimesGetResponse Objects

```python
class UdfRuntimesGetResponse(BaseModel)
```

Response model for GET (/udf_runtimes).

<a id="openeo_fastapi.api.models.Collection"></a>

## Collection Objects

```python
class Collection(BaseModel)
```

Response model for GET (/collection/{collection_id})

<a id="openeo_fastapi.api.models.Collections"></a>

## Collections Objects

```python
class Collections(TypedDict)
```

Response model for GET (/collections).

<a id="openeo_fastapi.api.models.ProcessesGetResponse"></a>

## ProcessesGetResponse Objects

```python
class ProcessesGetResponse(BaseModel)
```

Response model for GET (/processes).

<a id="openeo_fastapi.api.models.ProcessGraphWithMetadata"></a>

## ProcessGraphWithMetadata Objects

```python
class ProcessGraphWithMetadata(Process)
```

Reponse model for
            GET (/process_graphs/{process_graph_id})

Request model for
        PUT (/process_graphs/{process_graph_id})
        POST (/validation)

<a id="openeo_fastapi.api.models.ProcessGraphsGetResponse"></a>

## ProcessGraphsGetResponse Objects

```python
class ProcessGraphsGetResponse(BaseModel)
```

Response model for GET (/process_graphs).

<a id="openeo_fastapi.api.models.ValidationPostResponse"></a>

## ValidationPostResponse Objects

```python
class ValidationPostResponse(BaseModel)
```

Response model for POST (/validation).

<a id="openeo_fastapi.api.models.BatchJob"></a>

## BatchJob Objects

```python
class BatchJob(BaseModel)
```

Reponse model for GET (/jobs/{job_id}).

<a id="openeo_fastapi.api.models.JobsGetResponse"></a>

## JobsGetResponse Objects

```python
class JobsGetResponse(BaseModel)
```

Reponse model for GET (/jobs).

<a id="openeo_fastapi.api.models.JobsGetLogsResponse"></a>

## JobsGetLogsResponse Objects

```python
class JobsGetLogsResponse(BaseModel)
```

Reponse model for GET (/jobs/{job_id}/logs).

<a id="openeo_fastapi.api.models.JobsGetEstimateGetResponse"></a>

## JobsGetEstimateGetResponse Objects

```python
class JobsGetEstimateGetResponse(BaseModel)
```

Reponse model for GET (/jobs/{job_id}/estimate).

<a id="openeo_fastapi.api.models.JobsRequest"></a>

## JobsRequest Objects

```python
class JobsRequest(BaseModel)
```

Request model for
POST (/jobs)
PATCH (/jobs/{job_id})
POST (/result)

<a id="openeo_fastapi.api.models.FilesGetResponse"></a>

## FilesGetResponse Objects

```python
class FilesGetResponse(BaseModel)
```

Reponse model for GET (/files).

<a id="openeo_fastapi.api.models.FileFormatsGetResponse"></a>

## FileFormatsGetResponse Objects

```python
class FileFormatsGetResponse(BaseModel)
```

Reponse model for GET (/file_formats).

