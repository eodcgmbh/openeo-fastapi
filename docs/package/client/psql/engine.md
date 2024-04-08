# Table of Contents

* [openeo\_fastapi.client.psql.engine](#openeo_fastapi.client.psql.engine)
  * [get\_engine](#openeo_fastapi.client.psql.engine.get_engine)
  * [Filter](#openeo_fastapi.client.psql.engine.Filter)
  * [create](#openeo_fastapi.client.psql.engine.create)
  * [get](#openeo_fastapi.client.psql.engine.get)
  * [modify](#openeo_fastapi.client.psql.engine.modify)
  * [delete](#openeo_fastapi.client.psql.engine.delete)
  * [get\_first\_or\_default](#openeo_fastapi.client.psql.engine.get_first_or_default)

<a id="openeo_fastapi.client.psql.engine"></a>

# openeo\_fastapi.client.psql.engine

Standardisation of common functionality to interact with the ORMs and the database.

<a id="openeo_fastapi.client.psql.engine.get_engine"></a>

#### get\_engine

```python
def get_engine()
```

Get the engine using config from pydantic settings.

**Returns**:

- `Engine` - The engine instance that was created.

<a id="openeo_fastapi.client.psql.engine.Filter"></a>

## Filter Objects

```python
class Filter(BaseModel)
```

Filter class to assist with providing a filter by funciton with values across different cases.

<a id="openeo_fastapi.client.psql.engine.create"></a>

#### create

```python
def create(create_object: BaseModel) -> bool
```

Add the values from a pydantic model to the database using its respective object relational mapping.

<a id="openeo_fastapi.client.psql.engine.get"></a>

#### get

```python
def get(get_model: BaseModel, primary_key: Any) -> Union[None, BaseModel]
```

Get the relevant entry for a given model using the provided primary key value.

**Arguments**:

- `get_model` _BaseModel_ - The model that to get from the database.
- `primary_key` _Any_ - The primary key of the model instance to get.
  

**Returns**:

  Union[None, BaseModel]: None, or the found model

<a id="openeo_fastapi.client.psql.engine.modify"></a>

#### modify

```python
def modify(modify_object: BaseModel) -> bool
```

Modify the relevant entries for a given model instance

**Arguments**:

- `modify_object` _BaseModel_ - An instance of a pydantic model that reflects a change to make in the database.
  

**Returns**:

- `bool` - Whether the change was successful.

<a id="openeo_fastapi.client.psql.engine.delete"></a>

#### delete

```python
def delete(delete_model: BaseModel, primary_key: Any) -> bool
```

Delete the values from a pydantic model in the database using its respective object relational mapping.

**Arguments**:

- `delete_model` _BaseModel_ - The model that to delete from the database.
- `primary_key` _Any_ - The primary key of the model instance to delete.
  

**Returns**:

- `bool` - Whether the change was successful.

<a id="openeo_fastapi.client.psql.engine.get_first_or_default"></a>

#### get\_first\_or\_default

```python
def get_first_or_default(get_model: BaseModel,
                         filter_with: Filter) -> BaseModel
```

Perform a list operation and return the first found instance.

**Arguments**:

- `get_model` _BaseModel_ - The model that to get from the database.
- `filter_with` _Filter_ - Filter of a Key/Value pair to apply to the model.
  

**Returns**:

  Union[None, BaseModel]: Return the model if found, else return None.

