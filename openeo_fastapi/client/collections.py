import os

import aiohttp
from fastapi import APIRouter

from openeo_fastapi.client.models import Collection, Collections

router_collections = APIRouter()


async def get_collections():
    """
    Basic metadata for all datasets
    """
    try:
        async with aiohttp.ClientSession() as client:
            async with client.get(
                os.getenv("STAC_API_URL") + "collections"
            ) as response:
                resp = await response.json()

    except Exception as e:
        raise Exception("Ran into: ", e)

    return Collections(collections=resp["collections"], links=resp["links"])


async def get_collection(collection_id):
    try:
        async with aiohttp.ClientSession() as client:
            async with client.get(
                os.getenv("STAC_API_URL") + f"collections/{collection_id}"
            ) as response:
                resp = await response.json()

    except Exception as e:
        raise Exception("Ran into: ", e)

    return Collection(**resp)
