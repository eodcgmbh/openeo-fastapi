import aiohttp
from fastapi import HTTPException

from openeo_fastapi.api.responses import Collection, Collections
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
]


class CollectionRegister(EndpointRegister):
    def __init__(self, settings) -> None:
        super().__init__()
        self.endpoints = self._initialize_endpoints()
        self.settings = settings

    def _initialize_endpoints(self) -> list[Endpoint]:
        return COLLECTIONS_ENDPOINTS

    async def _proxy_request(self, path):
        """
        Proxy the request with aiohttp.
        """
        async with aiohttp.ClientSession() as client:
            async with client.get(self.settings.STAC_API_URL + path) as response:
                resp = await response.json()
                if response.status == 200:
                    return resp

    async def get_collection(self, collection_id):
        """
        Returns Metadata for specific datasetsbased on collection_id (str).
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
            path = f"collections/{collection_id}"
            resp = await self._proxy_request(path)

            if resp:
                return Collection(**resp)
            raise not_found
        raise not_found

    async def get_collections(self):
        """
        Returns Basic metadata for all datasets
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
