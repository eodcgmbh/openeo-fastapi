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


@pytest.mark.asyncio
async def test_get_collection_items(collections_core, s1_collection_items):
    with aioresponses() as m:
        get_items_url = (
            f"http://test-stac-api.mock.com/api/collections/SENTINEL1_GRD/items"
        )
        m.get(
            get_items_url,
            payload=s1_collection_items,
        )

        data = await collections_core.get_collection_items("SENTINEL1_GRD")

        assert data == s1_collection_items
        m.assert_called_once_with(get_items_url)


@pytest.mark.asyncio
async def test_get_collection_item(collections_core, s1_collection_item):
    with aioresponses() as m:
        get_item_url = f"http://test-stac-api.mock.com/api/collections/SENTINEL1_GRD/items/S1A_IW_GRDH_1SDV_20240309T125931_20240309T125956_052905_06674B"
        m.get(
            get_item_url,
            payload=s1_collection_item,
        )

        data = await collections_core.get_collection_item(
            "SENTINEL1_GRD",
            "S1A_IW_GRDH_1SDV_20240309T125931_20240309T125956_052905_06674B",
        )

        assert data == s1_collection_item
        m.assert_called_once_with(get_item_url)
