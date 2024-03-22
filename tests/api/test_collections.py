import os
from unittest.mock import patch

import pytest
from aioresponses import aioresponses

from openeo_fastapi.client.collections import Collection


@pytest.mark.asyncio
async def test_get_collections(collections_core, collections):
    with aioresponses() as m:
        get_collections_url = f"http://test-stac-api.mock.com/api/collections"
        m.get(get_collections_url, payload=collections)

        data = await collections_core.get_collections()

        assert data == collections
        m.assert_called_once_with(get_collections_url)


@pytest.mark.asyncio
async def test_get_collections_whitelist(collections_core, collections, s2a_collection):
    with patch.dict(os.environ, {"STAC_COLLECTIONS_WHITELIST": "Sentinel-2A"}):
        with aioresponses() as m:
            get_collections_url = f"http://test-stac-api.mock.com/api/collections"
            m.get(
                get_collections_url,
                payload={
                    "collections": [s2a_collection],
                    "links": collections["links"],
                },
            )

            data = await collections_core.get_collections()

            col = data["collections"][0]

            assert col == s2a_collection
            m.assert_called_once_with(get_collections_url)


@pytest.mark.asyncio
async def test_get_collection(collections_core, s2a_collection):
    with aioresponses() as m:
        get_collection_url = (
            f"http://test-stac-api.mock.com/api/collections/Sentinel-2A"
        )
        m.get(
            get_collection_url,
            payload=s2a_collection,
        )

        data = await collections_core.get_collection("Sentinel-2A")

        assert data == Collection(**s2a_collection)
        m.assert_called_once_with(get_collection_url)
