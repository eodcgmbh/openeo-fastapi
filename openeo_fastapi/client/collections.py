import aiohttp

from openeo_fastapi.client.models import Collection, Collections
from openeo_fastapi.client.settings import AppSettings


class CollectionCore:
    def __init__(self, settings) -> None:
        self.settings: AppSettings = settings
        pass

    async def get_collections(self):
        """
        Returns Basic metadata for all datasets
        """
        stac_url = (
            self.settings.STAC_API_URL
            if self.settings.STAC_API_URL.endswith("/")
            else self.settings.STAC_API_URL + "/"
        )

        try:
            async with aiohttp.ClientSession() as client:
                async with client.get(stac_url + "collections") as response:
                    resp = await response.json()
                    if response.status == 200 and resp.get("collections"):
                        collections_list = []
                        for collection_json in resp["collections"]:
                            if (
                                not self.settings.STAC_COLLECTIONS_WHITELIST
                                or collection_json["id"]
                                in self.settings.STAC_COLLECTIONS_WHITELIST
                            ):
                                collections_list.append(collection_json)

                        return Collections(
                            collections=collections_list, links=resp["links"]
                        )
                    else:
                        return {"Error": "No Collections found."}
        except Exception as e:
            raise Exception("Ran into: ", e)

    async def get_collection(self, collection_id):
        """
        Returns Metadata for specific datasetsbased on collection_id (str).
        """
        stac_url = (
            self.settings.STAC_API_URL
            if self.settings.STAC_API_URL.endswith("/")
            else self.settings.STAC_API_URL + "/"
        )

        try:
            async with aiohttp.ClientSession() as client:
                async with client.get(
                    stac_url + f"collections/{collection_id}"
                ) as response:
                    resp = await response.json()
                    if response.status == 200 and resp.get("id"):
                        if (
                            not self.settings.STAC_COLLECTIONS_WHITELIST
                            or resp["id"] in self.settings.STAC_COLLECTIONS_WHITELIST
                        ):
                            return Collection(**resp)
                    else:
                        return {"Error": "Collection not found."}

        except Exception as e:
            raise Exception("Ran into: ", e)
