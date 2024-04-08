# Table of Contents

* [openeo\_fastapi.client.processes](#openeo_fastapi.client.processes)
  * [UserDefinedProcessGraph](#openeo_fastapi.client.processes.UserDefinedProcessGraph)
    * [Config](#openeo_fastapi.client.processes.UserDefinedProcessGraph.Config)
    * [get\_orm](#openeo_fastapi.client.processes.UserDefinedProcessGraph.get_orm)
  * [ProcessRegister](#openeo_fastapi.client.processes.ProcessRegister)
    * [\_\_init\_\_](#openeo_fastapi.client.processes.ProcessRegister.__init__)
    * [get\_available\_processes](#openeo_fastapi.client.processes.ProcessRegister.get_available_processes)
    * [list\_processes](#openeo_fastapi.client.processes.ProcessRegister.list_processes)
    * [list\_user\_process\_graphs](#openeo_fastapi.client.processes.ProcessRegister.list_user_process_graphs)
    * [get\_user\_process\_graph](#openeo_fastapi.client.processes.ProcessRegister.get_user_process_graph)
    * [put\_user\_process\_graph](#openeo_fastapi.client.processes.ProcessRegister.put_user_process_graph)
    * [delete\_user\_process\_graph](#openeo_fastapi.client.processes.ProcessRegister.delete_user_process_graph)
    * [validate\_user\_process\_graph](#openeo_fastapi.client.processes.ProcessRegister.validate_user_process_graph)

<a id="openeo_fastapi.client.processes"></a>

# openeo\_fastapi.client.processes

Class and model to define the framework and partial application logic for interacting with Process and Process Graphs.

Classes:
    - ProcessRegister: Framework for defining and extending the logic for working with Processes and Process Graphs.

<a id="openeo_fastapi.client.processes.UserDefinedProcessGraph"></a>

## UserDefinedProcessGraph Objects

```python
class UserDefinedProcessGraph(BaseModel)
```

Pydantic model representing an OpenEO User Defined Process Graph.

<a id="openeo_fastapi.client.processes.UserDefinedProcessGraph.Config"></a>

## Config Objects

```python
class Config()
```

Pydantic model class config.

<a id="openeo_fastapi.client.processes.UserDefinedProcessGraph.get_orm"></a>

#### get\_orm

```python
@classmethod
def get_orm(cls)
```

Get the ORM model for this pydantic model.

<a id="openeo_fastapi.client.processes.ProcessRegister"></a>

## ProcessRegister Objects

```python
class ProcessRegister(EndpointRegister)
```

The ProcessRegister to regulate the application logic for the API behaviour.

<a id="openeo_fastapi.client.processes.ProcessRegister.__init__"></a>

#### \_\_init\_\_

```python
def __init__(links) -> None
```

Initialize the ProcessRegister.

**Arguments**:

- `links` _Links_ - The Links to be used in some function responses.

<a id="openeo_fastapi.client.processes.ProcessRegister.get_available_processes"></a>

#### get\_available\_processes

```python
@functools.cache
def get_available_processes()
```

Returns the pre-defined process from the process registry.

**Returns**:

- `list[Process]` - A list of Processes.

<a id="openeo_fastapi.client.processes.ProcessRegister.list_processes"></a>

#### list\_processes

```python
def list_processes() -> Union[ProcessesGetResponse, None]
```

Returns Supported predefined processes defined by openeo-processes-dask.

**Returns**:

- `ProcessesGetResponse` - A list of available processes.

<a id="openeo_fastapi.client.processes.ProcessRegister.list_user_process_graphs"></a>

#### list\_user\_process\_graphs

```python
def list_user_process_graphs(
    limit: Optional[int] = 10,
    user: User = Depends(Authenticator.validate)
) -> Union[ProcessGraphsGetResponse, None]
```

Lists all of a user's user-defined process graphs from the back-end.

**Arguments**:

- `limit` _int_ - The limit to apply to the length of the list.
- `user` _User_ - The User returned from the Authenticator.
  

**Returns**:

- `ProcessGraphsGetResponse` - A list of the user's UserDefinedProcessGraph as a ProcessGraphWithMetadata.

<a id="openeo_fastapi.client.processes.ProcessRegister.get_user_process_graph"></a>

#### get\_user\_process\_graph

```python
def get_user_process_graph(
    process_graph_id: str, user: User = Depends(Authenticator.validate)
) -> Union[ProcessGraphWithMetadata, None]
```

Lists all information about a user-defined process, including its process graph.

**Arguments**:

- `process_graph_id` _str_ - The process graph id.
- `user` _User_ - The User returned from the Authenticator.
  

**Raises**:

- `HTTPException` - Raises an exception with relevant status code and descriptive message of failure.
  

**Returns**:

- `ProcessGraphWithMetadata` - Retruns the UserDefinedProcessGraph as a ProcessGraphWithMetadata.

<a id="openeo_fastapi.client.processes.ProcessRegister.put_user_process_graph"></a>

#### put\_user\_process\_graph

```python
def put_user_process_graph(process_graph_id: str,
                           body: ProcessGraphWithMetadata,
                           user: User = Depends(Authenticator.validate))
```

Stores a provided user-defined process with process graph that can be reused in other processes.

**Arguments**:

- `process_graph_id` _str_ - The process graph id.
- `body` _ProcessGraphWithMetadata_ - The ProcessGraphWithMetadata should be used to create the new BatchJob.
- `user` _User_ - The User returned from the Authenticator.
  

**Raises**:

- `HTTPException` - Raises an exception with relevant status code and descriptive message of failure.
  

**Returns**:

- `Response` - A general FastApi response to signify resource was created as expected.

<a id="openeo_fastapi.client.processes.ProcessRegister.delete_user_process_graph"></a>

#### delete\_user\_process\_graph

```python
def delete_user_process_graph(process_graph_id: str,
                              user: User = Depends(Authenticator.validate))
```

Deletes the data related to this user-defined process, including its process graph.

**Arguments**:

- `process_graph_id` _str_ - The process graph id.
- `user` _User_ - The User returned from the Authenticator.
  

**Raises**:

- `HTTPException` - Raises an exception with relevant status code and descriptive message of failure.
  

**Returns**:

- `Response` - A general FastApi response to signify resource was created as expected.

<a id="openeo_fastapi.client.processes.ProcessRegister.validate_user_process_graph"></a>

#### validate\_user\_process\_graph

```python
def validate_user_process_graph(
    body: ProcessGraphWithMetadata,
    user: User = Depends(Authenticator.validate)
) -> ValidationPostResponse
```

Validates the ProcessGraphWithMetadata that is provided by the user.

**Arguments**:

- `process_graph_id` _str_ - The process graph id.
- `body` _ProcessGraphWithMetadata_ - The ProcessGraphWithMetadata should be used to validate the new BatchJob.
- `user` _User_ - The User returned from the Authenticator.
  

**Raises**:

- `HTTPException` - Raises an exception with relevant status code and descriptive message of failure.
  

**Returns**:

- `ValidationPostResponse` - A response to list an errors that where encountered when .

