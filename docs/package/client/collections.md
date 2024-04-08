# Table of Contents

* [openeo\_fastapi.client.collections](#openeo_fastapi.client.collections)
  * [CollectionRegister](#openeo_fastapi.client.collections.CollectionRegister)
    * [\_\_init\_\_](#openeo_fastapi.client.collections.CollectionRegister.__init__)
    * [get\_collection](#openeo_fastapi.client.collections.CollectionRegister.get_collection)
    * [get\_collections](#openeo_fastapi.client.collections.CollectionRegister.get_collections)
    * [get\_collection\_items](#openeo_fastapi.client.collections.CollectionRegister.get_collection_items)
    * [get\_collection\_item](#openeo_fastapi.client.collections.CollectionRegister.get_collection_item)

<a id="openeo_fastapi.client.collections"></a>

# openeo\_fastapi.client.collections

Class and model to define the framework and partial application logic for interacting with Collections.

Classes:
    - CollectionRegister: Framework for defining and extending the logic for working with Collections.

<a id="openeo_fastapi.client.collections.CollectionRegister"></a>

## CollectionRegister Objects

```python
class CollectionRegister(EndpointRegister)
```

The CollectionRegister to regulate the application logic for the API behaviour.

<a id="openeo_fastapi.client.collections.CollectionRegister.__init__"></a>

#### \_\_init\_\_

```python
def __init__(settings) -> None
```

Initialize the CollectionRegister.

**Arguments**:

- `settings` _AppSettings_ - The AppSettings that the application will use.

<a id="openeo_fastapi.client.collections.CollectionRegister.get_collection"></a>

#### get\_collection

```python
async def get_collection(collection_id)
```

Returns Metadata for specific datasetsbased on collection_id (str).

**Arguments**:

- `collection_id` _str_ - The collection id to request from the proxy.
  

**Raises**:

- `HTTPException` - Raises an exception with relevant status code and descriptive message of failure.
  

**Returns**:

- `Collection` - The proxied request returned as a Collection.

<a id="openeo_fastapi.client.collections.CollectionRegister.get_collections"></a>

#### get\_collections

```python
async def get_collections()
```

Returns Basic metadata for all datasets

**Raises**:

- `HTTPException` - Raises an exception with relevant status code and descriptive message of failure.
  

**Returns**:

- `Collections` - The proxied request returned as a Collections object.

<a id="openeo_fastapi.client.collections.CollectionRegister.get_collection_items"></a>

#### get\_collection\_items

```python
async def get_collection_items(collection_id)
```

Returns Basic metadata for all datasets.

**Arguments**:

- `collection_id` _str_ - The collection id to request from the proxy.
  

**Raises**:

- `HTTPException` - Raises an exception with relevant status code and descriptive message of failure.
  

**Returns**:

  The direct response from the request to the stac catalogue.

<a id="openeo_fastapi.client.collections.CollectionRegister.get_collection_item"></a>

#### get\_collection\_item

```python
async def get_collection_item(collection_id, item_id)
```

Returns Basic metadata for all datasets

**Arguments**:

- `collection_id` _str_ - The collection id to request from the proxy.
- `item_id` _str_ - The item id to request from the proxy.
  

**Raises**:

- `HTTPException` - Raises an exception with relevant status code and descriptive message of failure.
  

**Returns**:

  The direct response from the request to the stac catalogue.

