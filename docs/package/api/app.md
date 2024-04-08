# Table of Contents

* [openeo\_fastapi.api.app](#openeo_fastapi.api.app)
  * [OpenEOApi](#openeo_fastapi.api.app.OpenEOApi)
    * [register\_well\_known](#openeo_fastapi.api.app.OpenEOApi.register_well_known)
    * [register\_get\_capabilities](#openeo_fastapi.api.app.OpenEOApi.register_get_capabilities)
    * [register\_get\_conformance](#openeo_fastapi.api.app.OpenEOApi.register_get_conformance)
    * [register\_get\_file\_formats](#openeo_fastapi.api.app.OpenEOApi.register_get_file_formats)
    * [register\_get\_health](#openeo_fastapi.api.app.OpenEOApi.register_get_health)
    * [register\_get\_user\_info](#openeo_fastapi.api.app.OpenEOApi.register_get_user_info)
    * [register\_get\_udf\_runtimes](#openeo_fastapi.api.app.OpenEOApi.register_get_udf_runtimes)
    * [register\_validate\_user\_process\_graph](#openeo_fastapi.api.app.OpenEOApi.register_validate_user_process_graph)
    * [register\_run\_sync\_job](#openeo_fastapi.api.app.OpenEOApi.register_run_sync_job)
    * [register\_get\_collections](#openeo_fastapi.api.app.OpenEOApi.register_get_collections)
    * [register\_get\_collection](#openeo_fastapi.api.app.OpenEOApi.register_get_collection)
    * [register\_get\_collection\_items](#openeo_fastapi.api.app.OpenEOApi.register_get_collection_items)
    * [register\_get\_collection\_item](#openeo_fastapi.api.app.OpenEOApi.register_get_collection_item)
    * [register\_get\_processes](#openeo_fastapi.api.app.OpenEOApi.register_get_processes)
    * [register\_list\_user\_process\_graphs](#openeo_fastapi.api.app.OpenEOApi.register_list_user_process_graphs)
    * [register\_get\_user\_process\_graph](#openeo_fastapi.api.app.OpenEOApi.register_get_user_process_graph)
    * [register\_put\_user\_process\_graph](#openeo_fastapi.api.app.OpenEOApi.register_put_user_process_graph)
    * [register\_delete\_user\_process\_graph](#openeo_fastapi.api.app.OpenEOApi.register_delete_user_process_graph)
    * [register\_get\_jobs](#openeo_fastapi.api.app.OpenEOApi.register_get_jobs)
    * [register\_create\_job](#openeo_fastapi.api.app.OpenEOApi.register_create_job)
    * [register\_update\_job](#openeo_fastapi.api.app.OpenEOApi.register_update_job)
    * [register\_get\_job](#openeo_fastapi.api.app.OpenEOApi.register_get_job)
    * [register\_delete\_job](#openeo_fastapi.api.app.OpenEOApi.register_delete_job)
    * [register\_get\_estimate](#openeo_fastapi.api.app.OpenEOApi.register_get_estimate)
    * [register\_get\_logs](#openeo_fastapi.api.app.OpenEOApi.register_get_logs)
    * [register\_get\_results](#openeo_fastapi.api.app.OpenEOApi.register_get_results)
    * [register\_start\_job](#openeo_fastapi.api.app.OpenEOApi.register_start_job)
    * [register\_cancel\_job](#openeo_fastapi.api.app.OpenEOApi.register_cancel_job)
    * [register\_list\_files](#openeo_fastapi.api.app.OpenEOApi.register_list_files)
    * [register\_download\_file](#openeo_fastapi.api.app.OpenEOApi.register_download_file)
    * [register\_upload\_file](#openeo_fastapi.api.app.OpenEOApi.register_upload_file)
    * [register\_delete\_file](#openeo_fastapi.api.app.OpenEOApi.register_delete_file)
    * [register\_core](#openeo_fastapi.api.app.OpenEOApi.register_core)
    * [http\_exception\_handler](#openeo_fastapi.api.app.OpenEOApi.http_exception_handler)
    * [\_\_attrs\_post\_init\_\_](#openeo_fastapi.api.app.OpenEOApi.__attrs_post_init__)

<a id="openeo_fastapi.api.app"></a>

# openeo\_fastapi.api.app

OpenEO Api class for preparing the FastApi object from the client that is provided by the user.

<a id="openeo_fastapi.api.app.OpenEOApi"></a>

## OpenEOApi Objects

```python
@attr.define
class OpenEOApi()
```

Factory for creating FastApi applications conformant to the OpenEO Api specification.

<a id="openeo_fastapi.api.app.OpenEOApi.register_well_known"></a>

#### register\_well\_known

```python
def register_well_known()
```

Register well known endpoint (GET /.well-known/openeo).

<a id="openeo_fastapi.api.app.OpenEOApi.register_get_capabilities"></a>

#### register\_get\_capabilities

```python
def register_get_capabilities()
```

Register endpoint for capabilities (GET /).

<a id="openeo_fastapi.api.app.OpenEOApi.register_get_conformance"></a>

#### register\_get\_conformance

```python
def register_get_conformance()
```

Register endpoint for api conformance (GET /conformance).

<a id="openeo_fastapi.api.app.OpenEOApi.register_get_file_formats"></a>

#### register\_get\_file\_formats

```python
def register_get_file_formats()
```

Register endpoint for supported file formats (GET /file_formats).

<a id="openeo_fastapi.api.app.OpenEOApi.register_get_health"></a>

#### register\_get\_health

```python
def register_get_health()
```

Register endpoint for api health (GET /health).

<a id="openeo_fastapi.api.app.OpenEOApi.register_get_user_info"></a>

#### register\_get\_user\_info

```python
def register_get_user_info()
```

Register endpoint for user info (GET /me).

<a id="openeo_fastapi.api.app.OpenEOApi.register_get_udf_runtimes"></a>

#### register\_get\_udf\_runtimes

```python
def register_get_udf_runtimes()
```

Register endpoint to list the supported udf runtimes (GET /udf_runtimes).

<a id="openeo_fastapi.api.app.OpenEOApi.register_validate_user_process_graph"></a>

#### register\_validate\_user\_process\_graph

```python
def register_validate_user_process_graph()
```

Register endpoint for validating a user process graph (GET /validation).

<a id="openeo_fastapi.api.app.OpenEOApi.register_run_sync_job"></a>

#### register\_run\_sync\_job

```python
def register_run_sync_job()
```

Register endpoint for executing synchronous jobs (GET /result).

<a id="openeo_fastapi.api.app.OpenEOApi.register_get_collections"></a>

#### register\_get\_collections

```python
def register_get_collections()
```

Register endpoint for listing available collections (GET /collections).

<a id="openeo_fastapi.api.app.OpenEOApi.register_get_collection"></a>

#### register\_get\_collection

```python
def register_get_collection()
```

Register endpoint for getting a specific collection (GET /collections/{collection_id}).

<a id="openeo_fastapi.api.app.OpenEOApi.register_get_collection_items"></a>

#### register\_get\_collection\_items

```python
def register_get_collection_items()
```

Register endpoint for getting collection items (GET /collections/{collection_id}/items).

<a id="openeo_fastapi.api.app.OpenEOApi.register_get_collection_item"></a>

#### register\_get\_collection\_item

```python
def register_get_collection_item()
```

Register endpoint for getting a specific collection item (GET /collections/{collection_id}/items/{item_id}).

<a id="openeo_fastapi.api.app.OpenEOApi.register_get_processes"></a>

#### register\_get\_processes

```python
def register_get_processes()
```

Register endpoint for listing all predefined processes (GET /processes).

<a id="openeo_fastapi.api.app.OpenEOApi.register_list_user_process_graphs"></a>

#### register\_list\_user\_process\_graphs

```python
def register_list_user_process_graphs()
```

Register endpoint for listing user defined processes graphs (GET /processes_graphs).

<a id="openeo_fastapi.api.app.OpenEOApi.register_get_user_process_graph"></a>

#### register\_get\_user\_process\_graph

```python
def register_get_user_process_graph()
```

Register endpoint for getting a specific user defined processes graphs (GET /processes_graphs/{process_graph_id}).

<a id="openeo_fastapi.api.app.OpenEOApi.register_put_user_process_graph"></a>

#### register\_put\_user\_process\_graph

```python
def register_put_user_process_graph()
```

Register endpoint for creatings a user defined processes graph (PUT /processes_graphs/{process_graph_id}).

<a id="openeo_fastapi.api.app.OpenEOApi.register_delete_user_process_graph"></a>

#### register\_delete\_user\_process\_graph

```python
def register_delete_user_process_graph()
```

Register endpoint for deleting a user defined processes graph (DELETE /processes_graphs/{process_graph_id}).

<a id="openeo_fastapi.api.app.OpenEOApi.register_get_jobs"></a>

#### register\_get\_jobs

```python
def register_get_jobs()
```

Register endpoint for listing all jobs (GET /jobs).

<a id="openeo_fastapi.api.app.OpenEOApi.register_create_job"></a>

#### register\_create\_job

```python
def register_create_job()
```

Register endpoint for creating a new job (POST /jobs).

<a id="openeo_fastapi.api.app.OpenEOApi.register_update_job"></a>

#### register\_update\_job

```python
def register_update_job()
```

Register update jobs endpoint (POST /jobs/{job_id}).

<a id="openeo_fastapi.api.app.OpenEOApi.register_get_job"></a>

#### register\_get\_job

```python
def register_get_job()
```

Register endpoint for retreiving job metadata (GET /jobs/{job_id}).

<a id="openeo_fastapi.api.app.OpenEOApi.register_delete_job"></a>

#### register\_delete\_job

```python
def register_delete_job()
```

Register endpoint for deleting the record of a batch job (GET /jobs/{job_id}).

<a id="openeo_fastapi.api.app.OpenEOApi.register_get_estimate"></a>

#### register\_get\_estimate

```python
def register_get_estimate()
```

Register endpoint for estimating a batch job (GET /jobs/{job_id}).

<a id="openeo_fastapi.api.app.OpenEOApi.register_get_logs"></a>

#### register\_get\_logs

```python
def register_get_logs()
```

Register endpoint for retrieving job logs (GET /jobs/{job_id}).

<a id="openeo_fastapi.api.app.OpenEOApi.register_get_results"></a>

#### register\_get\_results

```python
def register_get_results()
```

Register endpoint for getting the results from a batch job (GET /jobs/{job_id}).

<a id="openeo_fastapi.api.app.OpenEOApi.register_start_job"></a>

#### register\_start\_job

```python
def register_start_job()
```

Register endpoint for starting batch job processing (GET /jobs/{job_id}).

<a id="openeo_fastapi.api.app.OpenEOApi.register_cancel_job"></a>

#### register\_cancel\_job

```python
def register_cancel_job()
```

Register endpoint for cancelling job processing (GET /jobs/{job_id}).

<a id="openeo_fastapi.api.app.OpenEOApi.register_list_files"></a>

#### register\_list\_files

```python
def register_list_files()
```

Register endpoint for listing a user's fils (GET /files).

<a id="openeo_fastapi.api.app.OpenEOApi.register_download_file"></a>

#### register\_download\_file

```python
def register_download_file()
```

Register endpoint for downloading a specific file (GET /files/{path}).

<a id="openeo_fastapi.api.app.OpenEOApi.register_upload_file"></a>

#### register\_upload\_file

```python
def register_upload_file()
```

Register endpoint for uploading a new file (PUT /files/{path}).

<a id="openeo_fastapi.api.app.OpenEOApi.register_delete_file"></a>

#### register\_delete\_file

```python
def register_delete_file()
```

Register endpoint for deleting a new file (DELETE /files/{path}).

<a id="openeo_fastapi.api.app.OpenEOApi.register_core"></a>

#### register\_core

```python
def register_core()
```

Add application logic to the API layer.

<a id="openeo_fastapi.api.app.OpenEOApi.http_exception_handler"></a>

#### http\_exception\_handler

```python
def http_exception_handler(request, exception)
```

Register exception handler to turn python exceptions into expected OpenEO error output.

<a id="openeo_fastapi.api.app.OpenEOApi.__attrs_post_init__"></a>

#### \_\_attrs\_post\_init\_\_

```python
def __attrs_post_init__()
```

Post-init hook responsible for setting up the application upon instantiation of the class.

