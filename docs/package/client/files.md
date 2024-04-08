# Table of Contents

* [openeo\_fastapi.client.files](#openeo_fastapi.client.files)
  * [FilesRegister](#openeo_fastapi.client.files.FilesRegister)
    * [list\_files](#openeo_fastapi.client.files.FilesRegister.list_files)
    * [download\_file](#openeo_fastapi.client.files.FilesRegister.download_file)
    * [upload\_file](#openeo_fastapi.client.files.FilesRegister.upload_file)
    * [delete\_file](#openeo_fastapi.client.files.FilesRegister.delete_file)

<a id="openeo_fastapi.client.files"></a>

# openeo\_fastapi.client.files

Class and model to define the framework and partial application logic for interacting with Files.

Classes:
    - FilesRegister: Framework for defining and extending the logic for working with Files.

<a id="openeo_fastapi.client.files.FilesRegister"></a>

## FilesRegister Objects

```python
class FilesRegister(EndpointRegister)
```

<a id="openeo_fastapi.client.files.FilesRegister.list_files"></a>

#### list\_files

```python
def list_files(limit: Optional[int] = 10,
               user: User = Depends(Authenticator.validate))
```

List the  files in the user workspace.

**Arguments**:

- `limit` _int_ - The limit to apply to the length of the list.
- `user` _User_ - The User returned from the Authenticator.
  

**Raises**:

- `HTTPException` - Raises an exception with relevant status code and descriptive message of failure.

<a id="openeo_fastapi.client.files.FilesRegister.download_file"></a>

#### download\_file

```python
def download_file(path: str, user: User = Depends(Authenticator.validate))
```

Download the file from the user's workspace.

**Arguments**:

- `path` _str_ - The path leading to the file.
- `user` _User_ - The User returned from the Authenticator.
  

**Raises**:

- `HTTPException` - Raises an exception with relevant status code and descriptive message of failure.

<a id="openeo_fastapi.client.files.FilesRegister.upload_file"></a>

#### upload\_file

```python
def upload_file(path: str, user: User = Depends(Authenticator.validate))
```

Upload the file from the user's workspace.

**Arguments**:

- `path` _str_ - The path leading to the file.
- `user` _User_ - The User returned from the Authenticator.
  

**Raises**:

- `HTTPException` - Raises an exception with relevant status code and descriptive message of failure.

<a id="openeo_fastapi.client.files.FilesRegister.delete_file"></a>

#### delete\_file

```python
def delete_file(path: str, user: User = Depends(Authenticator.validate))
```

Delete the file from the user's workspace.

**Arguments**:

- `path` _str_ - The path leading to the file.
- `user` _User_ - The User returned from the Authenticator.
  

**Raises**:

- `HTTPException` - Raises an exception with relevant status code and descriptive message of failure.

