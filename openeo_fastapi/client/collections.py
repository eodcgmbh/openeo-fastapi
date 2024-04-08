"""Class and model to define the framework and partial application logic for interacting with Collections.

Classes:
    - CollectionRegister: Framework for defining and extending the logic for working with Collections.
"""
import aiohttp
from fastapi import HTTPException

from openeo_fastapi.api.models import Collection, Collections
from openeo_fastapi.api.types import Endpoint, Error
from openeo_fastapi.client.register import EndpointRegister

COLLECTIONS_ENDPOINTS = [
    Endpoint(
        path="/collections",
        methods=["GET"],
    ),
    Endpoint(
        path="/collections/{collection_id}",
        methods=["GET"],
    ),
    Endpoint(
        path="/collections/{collection_id}/items",
        methods=["GET"],
    ),
    Endpoint(
        path="/collections/{collection_id}/items/{item_id}",
        methods=["GET"],
    ),
]


class CollectionRegister(EndpointRegister):
    """The CollectionRegister to regulate the application logic for the API behaviour.
    """
    
    def __init__(self, settings) -> None:
        """Initialize the CollectionRegister.

        Args:
            settings (AppSettings): The AppSettings that the application will use.
        """
        super().__init__()
        self.endpoints = self._initialize_endpoints()
        self.settings = settings

    def _initialize_endpoints(self) -> list[Endpoint]:
        """Initialize the endpoints for the register.

        Returns:
            list[Endpoint]: The default list of job endpoints which are packaged with the module.
        """
        return COLLECTIONS_ENDPOINTS

    async def _proxy_request(self, path):
        """Proxy the request with aiohttp.

        Args:
            path (str): The path to proxy to the STAC catalogue.

        Raises:
            HTTPException: Raises an exception with relevant status code and descriptive message of failure.

        Returns:
            The response dictionary from the request.
        """
        async with aiohttp.ClientSession() as client:
            async with client.get(self.settings.STAC_API_URL + path) as response:
                resp = await response.json()
                if response.status == 200:
                    return resp

    async def get_collection(self, collection_id):
        """
        Returns Metadata for specific datasetsbased on collection_id (str).
        
        Args:
            collection_id (str): The collection id to request from the proxy.

        Raises:
            HTTPException: Raises an exception with relevant status code and descriptive message of failure.

        Returns:
            Collection: The proxied request returned as a Collection.
        """
        not_found = Error(
                code="NotFound", message=f"Collection {collection_id} not found."
            )

        if (
            not self.settings.STAC_COLLECTIONS_WHITELIST
            or collection_id in self.settings.STAC_COLLECTIONS_WHITELIST
        ):
            path = f"collections/{collection_id}"
            resp = await self._proxy_request(path)

            if resp:
                return Collection(**resp)
            raise HTTPException(
                status_code=404,
                detail=not_found
            )
        raise HTTPException(
            status_code=404,
            detail=not_found
        )

    async def get_collections(self):
        """
        Returns Basic metadata for all datasets

        Raises:
            HTTPException: Raises an exception with relevant status code and descriptive message of failure.

        Returns:
            Collections: The proxied request returned as a Collections object.
        """
        path = "collections"
        resp = await self._proxy_request(path)

        if resp:
            collections_list = [
                collection
                for collection in resp["collections"]
                if (
                    not self.settings.STAC_COLLECTIONS_WHITELIST
                    or collection["id"] in self.settings.STAC_COLLECTIONS_WHITELIST
                )
            ]

            return Collections(collections=collections_list, links=resp["links"])
        else:
            raise HTTPException(
                status_code=404,
                detail=Error(code="NotFound", message="No Collections found."),
            )

    async def get_collection_items(self, collection_id):
        """
        Returns Basic metadata for all datasets.
        
        Args:
            collection_id (str): The collection id to request from the proxy.

        Raises:
            HTTPException: Raises an exception with relevant status code and descriptive message of failure.

        Returns:
            The direct response from the request to the stac catalogue.
        """
        not_found = HTTPException(
            status_code=404,
            detail=Error(
                code="NotFound", message=f"Collection {collection_id} not found."
            ),
        )

        if (
            not self.settings.STAC_COLLECTIONS_WHITELIST
            or collection_id in self.settings.STAC_COLLECTIONS_WHITELIST
        ):
            path = f"collections/{collection_id}/items"
            resp = await self._proxy_request(path)

            if resp:
                return resp
            raise not_found
        raise not_found

    async def get_collection_item(self, collection_id, item_id):
        """
        Returns Basic metadata for all datasets
        
        Args:
            collection_id (str): The collection id to request from the proxy.
            item_id (str): The item id to request from the proxy.

        Raises:
            HTTPException: Raises an exception with relevant status code and descriptive message of failure.

        Returns:
            The direct response from the request to the stac catalogue.
        """
        not_found = HTTPException(
            status_code=404,
            detail=Error(
                code="NotFound",
                message=f"Item {item_id} not found in collection {collection_id}.",
            ),
        )

        if (
            not self.settings.STAC_COLLECTIONS_WHITELIST
            or collection_id in self.settings.STAC_COLLECTIONS_WHITELIST
        ):
            path = f"collections/{collection_id}/items/{item_id}"
            resp = await self._proxy_request(path)

            if resp:
                return resp
            raise not_found
        raise not_found
