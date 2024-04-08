# Table of Contents

* [openeo\_fastapi.client.core](#openeo_fastapi.client.core)
  * [OpenEOCore](#openeo_fastapi.client.core.OpenEOCore)
    * [\_\_attrs\_post\_init\_\_](#openeo_fastapi.client.core.OpenEOCore.__attrs_post_init__)
    * [get\_capabilities](#openeo_fastapi.client.core.OpenEOCore.get_capabilities)
    * [get\_conformance](#openeo_fastapi.client.core.OpenEOCore.get_conformance)
    * [get\_file\_formats](#openeo_fastapi.client.core.OpenEOCore.get_file_formats)
    * [get\_health](#openeo_fastapi.client.core.OpenEOCore.get_health)
    * [get\_user\_info](#openeo_fastapi.client.core.OpenEOCore.get_user_info)
    * [get\_well\_known](#openeo_fastapi.client.core.OpenEOCore.get_well_known)
    * [get\_udf\_runtimes](#openeo_fastapi.client.core.OpenEOCore.get_udf_runtimes)

<a id="openeo_fastapi.client.core"></a>

# openeo\_fastapi.client.core

Class and model to define the framework and partial application logic for interacting with Jobs.

Classes:
    - OpenEOCore: Framework for defining the application logic that will passed onto the OpenEO Api.

<a id="openeo_fastapi.client.core.OpenEOCore"></a>

## OpenEOCore Objects

```python
@define
class OpenEOCore()
```

Client for defining the application logic for the OpenEO Api.

<a id="openeo_fastapi.client.core.OpenEOCore.__attrs_post_init__"></a>

#### \_\_attrs\_post\_init\_\_

```python
def __attrs_post_init__()
```

Post init hook to set the client registers, if none where provided by the user set to the defaults!

<a id="openeo_fastapi.client.core.OpenEOCore.get_capabilities"></a>

#### get\_capabilities

```python
def get_capabilities() -> Capabilities
```

Get the capabilities of the api.

**Returns**:

- `Capabilities` - The capabilities of the api based off what the user provided.

<a id="openeo_fastapi.client.core.OpenEOCore.get_conformance"></a>

#### get\_conformance

```python
def get_conformance() -> ConformanceGetResponse
```

Get the capabilities of the api.

**Returns**:

- `ConformanceGetResponse` - The conformance classes that this Api wil of the api based off what the user provided.

<a id="openeo_fastapi.client.core.OpenEOCore.get_file_formats"></a>

#### get\_file\_formats

```python
def get_file_formats() -> FileFormatsGetResponse
```

Get the supported file formats for processing input and output.

**Returns**:

- `FileFormatsGetResponse` - The response defining the input and output formats.

<a id="openeo_fastapi.client.core.OpenEOCore.get_health"></a>

#### get\_health

```python
def get_health()
```

Basic health endpoint expected to return status code 200.

**Returns**:

- `Response` - Status code 200.

<a id="openeo_fastapi.client.core.OpenEOCore.get_user_info"></a>

#### get\_user\_info

```python
def get_user_info(user: User = Depends(
    Authenticator.validate)) -> MeGetResponse
```

Get the supported file formats for processing input and output.

**Returns**:

- `MeGetResponse` - The user information for the validated user.

<a id="openeo_fastapi.client.core.OpenEOCore.get_well_known"></a>

#### get\_well\_known

```python
def get_well_known() -> WellKnownOpeneoGetResponse
```

Get the supported file formats for processing input and output.

**Returns**:

- `WellKnownOpeneoGetResponse` - The api/s which are exposed at this server.

<a id="openeo_fastapi.client.core.OpenEOCore.get_udf_runtimes"></a>

#### get\_udf\_runtimes

```python
def get_udf_runtimes() -> UdfRuntimesGetResponse
```

Get the supported file formats for processing input and output.

**Raises**:

- `HTTPException` - Raises an exception with relevant status code and descriptive message of failure.
  

**Returns**:

- `UdfRuntimesGetResponse` - The metadata for the requested BatchJob.

