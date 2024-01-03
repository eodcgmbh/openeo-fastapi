import os

import aiohttp
from fastapi import APIRouter
from starlette.responses import JSONResponse
from yurl import URL

from openeo_fastapi.client.models import Collection, Collections

router_collections = APIRouter()


async def get_collections():
    """
    Basic metadata for all datasets
    """

    async with aiohttp.ClientSession() as client:
        async with client.get(os.getenv("STAC_API_URL") + "collections") as response:
            resp = await response.json()
            if response.status == 200 and resp.get("collections"):
                return Collections(collections=resp["collections"], links=resp["links"])
            else:
                return resp


async def get_collection(collection_id):
    """
    Metadata for specific dataset
    """

    async with aiohttp.ClientSession() as client:
        async with client.get(
            os.getenv("STAC_API_URL") + f"collections/{collection_id}"
        ) as response:
            resp = await response.json()
            if response.status == 200 and resp.get("id"):
                return Collection(**resp)
            else:
                return resp
