# Table of Contents

* [openeo\_fastapi.api.types](#openeo_fastapi.api.types)
  * [STACConformanceClasses](#openeo_fastapi.api.types.STACConformanceClasses)
  * [DinensionEnum](#openeo_fastapi.api.types.DinensionEnum)
  * [Type5](#openeo_fastapi.api.types.Type5)
  * [Method](#openeo_fastapi.api.types.Method)
  * [Status](#openeo_fastapi.api.types.Status)
  * [Level](#openeo_fastapi.api.types.Level)
  * [GisDataType](#openeo_fastapi.api.types.GisDataType)
  * [Role](#openeo_fastapi.api.types.Role)
  * [RFC3339Datetime](#openeo_fastapi.api.types.RFC3339Datetime)
  * [Endpoint](#openeo_fastapi.api.types.Endpoint)
  * [Plan](#openeo_fastapi.api.types.Plan)
  * [Billing](#openeo_fastapi.api.types.Billing)
  * [File](#openeo_fastapi.api.types.File)
  * [UsageMetric](#openeo_fastapi.api.types.UsageMetric)
  * [Usage](#openeo_fastapi.api.types.Usage)
  * [Link](#openeo_fastapi.api.types.Link)
  * [LogEntry](#openeo_fastapi.api.types.LogEntry)
  * [Process](#openeo_fastapi.api.types.Process)
  * [Error](#openeo_fastapi.api.types.Error)
  * [FileFormat](#openeo_fastapi.api.types.FileFormat)
  * [Storage](#openeo_fastapi.api.types.Storage)
  * [Version](#openeo_fastapi.api.types.Version)
  * [StacProvider](#openeo_fastapi.api.types.StacProvider)
  * [Dimension](#openeo_fastapi.api.types.Dimension)
  * [Spatial](#openeo_fastapi.api.types.Spatial)
  * [Temporal](#openeo_fastapi.api.types.Temporal)
  * [Extent](#openeo_fastapi.api.types.Extent)

<a id="openeo_fastapi.api.types"></a>

# openeo\_fastapi.api.types

Pydantic Models and Enums describining different attribute types used by the models in openeo_fastapi.api.models.

<a id="openeo_fastapi.api.types.STACConformanceClasses"></a>

## STACConformanceClasses Objects

```python
class STACConformanceClasses(Enum)
```

Available conformance classes with STAC.

<a id="openeo_fastapi.api.types.DinensionEnum"></a>

## DinensionEnum Objects

```python
class DinensionEnum(Enum)
```

Dimension enum.

<a id="openeo_fastapi.api.types.Type5"></a>

## Type5 Objects

```python
class Type5(Enum)
```

Catalog enum.

<a id="openeo_fastapi.api.types.Method"></a>

## Method Objects

```python
class Method(Enum)
```

HTTP Methods enum.

<a id="openeo_fastapi.api.types.Status"></a>

## Status Objects

```python
class Status(Enum)
```

Job Status enum.

<a id="openeo_fastapi.api.types.Level"></a>

## Level Objects

```python
class Level(Enum)
```

Log level enum.

<a id="openeo_fastapi.api.types.GisDataType"></a>

## GisDataType Objects

```python
class GisDataType(Enum)
```

Data type enum.

<a id="openeo_fastapi.api.types.Role"></a>

## Role Objects

```python
class Role(Enum)
```

Role for collection provider.

<a id="openeo_fastapi.api.types.RFC3339Datetime"></a>

## RFC3339Datetime Objects

```python
class RFC3339Datetime(BaseModel)
```

Model to consistently represent datetimes as strings compliant to RFC3339Datetime.

<a id="openeo_fastapi.api.types.Endpoint"></a>

## Endpoint Objects

```python
class Endpoint(BaseModel)
```

Model to capture the available endpoint and it's accepted models.

<a id="openeo_fastapi.api.types.Plan"></a>

## Plan Objects

```python
class Plan(BaseModel)
```

Model to capture the the plan the user has subscribe to.

<a id="openeo_fastapi.api.types.Billing"></a>

## Billing Objects

```python
class Billing(BaseModel)
```

Model to capture the billing options that are available at the backend.

<a id="openeo_fastapi.api.types.File"></a>

## File Objects

```python
class File(BaseModel)
```

Model to capture the stat information of a file stored at the backend.

<a id="openeo_fastapi.api.types.UsageMetric"></a>

## UsageMetric Objects

```python
class UsageMetric(BaseModel)
```

Model to capture the value and unit of a given metric.

<a id="openeo_fastapi.api.types.Usage"></a>

## Usage Objects

```python
class Usage(BaseModel)
```

Model to capture the usage of a job.

<a id="openeo_fastapi.api.types.Link"></a>

## Link Objects

```python
class Link(BaseModel)
```

Model to describe the information for a provided URL.

<a id="openeo_fastapi.api.types.LogEntry"></a>

## LogEntry Objects

```python
class LogEntry(BaseModel)
```

Model to describe the information for a given log line in job logs.

<a id="openeo_fastapi.api.types.Process"></a>

## Process Objects

```python
class Process(BaseModel)
```

Model to describe a process that is exposed by the api.

<a id="openeo_fastapi.api.types.Error"></a>

## Error Objects

```python
class Error(BaseModel)
```

Model to describe the information of a captured exception by the api.

<a id="openeo_fastapi.api.types.FileFormat"></a>

## FileFormat Objects

```python
class FileFormat(BaseModel)
```

Model to describe a file format supported by the processing backend.

<a id="openeo_fastapi.api.types.Storage"></a>

## Storage Objects

```python
class Storage(BaseModel)
```

Model to describe the storage resources available to a given user.

<a id="openeo_fastapi.api.types.Version"></a>

## Version Objects

```python
class Version(BaseModel)
```

Model to describe the version of an api that is available.

<a id="openeo_fastapi.api.types.StacProvider"></a>

## StacProvider Objects

```python
class StacProvider(BaseModel)
```

Model to describe the provider of a given stac resource.

<a id="openeo_fastapi.api.types.Dimension"></a>

## Dimension Objects

```python
class Dimension(BaseModel)
```

Model to describe the dimension of some data.

<a id="openeo_fastapi.api.types.Spatial"></a>

## Spatial Objects

```python
class Spatial(BaseModel)
```

Model to describe the spatial extent of a collection.

<a id="openeo_fastapi.api.types.Temporal"></a>

## Temporal Objects

```python
class Temporal(BaseModel)
```

Model to describe the temporal range of a collection.

<a id="openeo_fastapi.api.types.Extent"></a>

## Extent Objects

```python
class Extent(BaseModel)
```

Model to describe the complete spatiotemporal extent of a collection.

