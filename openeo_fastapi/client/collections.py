import os

import aiohttp
from fastapi import APIRouter

from openeo_fastapi.client.models import Collection, Collections
from openeo_fastapi.client.settings import app_settings

router_collections = APIRouter()
from urllib.parse import urljoin


async def get_collections():
    """
    Basic metadata for all datasets
    """
    stac_url = (
        app_settings.STAC_API_URL
        if app_settings.STAC_API_URL.endswith("/")
        else app_settings.STAC_API_URL + "/"
    )

    try:
        async with aiohttp.ClientSession() as client:
            async with client.get(stac_url + "collections") as response:
                resp = await response.json()
                if response.status == 200 and resp.get("collections"):
                    collections_list = []
                    for collection_json in resp["collections"]:
                        # For the collections from STAC, only let them through if they're on the whitelist
                        # This has to be before the legacy collections are added.
                        if (
                            len(app_settings.STAC_COLLECTIONS_WHITELIST) < 1
                            or collection_json["id"]
                            in app_settings.STAC_COLLECTIONS_WHITELIST
                        ):
                            collections_list.append(collection_json)

                    return Collections(
                        collections=collections_list, links=resp["links"]
                    )
                else:
                    return {"Error": "No Collections found."}
    except Exception as e:
        raise Exception("Ran into: ", e)


async def get_collection(collection_id):
    """
    Metadata for specific datasets
    """
    stac_url = (
        app_settings.STAC_API_URL
        if app_settings.STAC_API_URL.endswith("/")
        else app_settings.STAC_API_URL + "/"
    )

    try:
        async with aiohttp.ClientSession() as client:
            async with client.get(
                stac_url + f"collections/{collection_id}"
            ) as response:
                resp = await response.json()
                if response.status == 200 and resp.get("id"):
                    if (
                        len(app_settings.STAC_COLLECTIONS_WHITELIST) < 1
                        or resp["id"] in app_settings.STAC_COLLECTIONS_WHITELIST
                    ):
                        return Collection(**resp)
                else:
                    return {"Error": "Collection not found."}

    except Exception as e:
        raise Exception("Ran into: ", e)
