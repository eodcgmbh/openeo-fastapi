import json
import os

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from openeo_fastapi.api.app import OpenEOApi
from openeo_fastapi.client.collections import get_collection, get_collections
from openeo_fastapi.client.models import Collection

path_to_current_file = os.path.realpath(__file__)
current_directory = os.path.split(path_to_current_file)[0]


from aioresponses import aioresponses


@pytest.mark.asyncio
async def test_get_collections():
    with open(os.path.join(current_directory, "collections.json")) as f_in:
        collections = json.load(f_in)
    with aioresponses() as m:
        m.get("http://test-stac-api.mock.com/api/collections", payload=collections)

        data = await get_collections()

        assert data == collections
        m.assert_called_once_with("http://test-stac-api.mock.com/api/collections")


@pytest.mark.asyncio
async def test_get_collection():
    with open(os.path.join(current_directory, "collections.json")) as f_in:
        collection = json.load(f_in)["collections"][0]
    with aioresponses() as m:
        m.get(
            "http://test-stac-api.mock.com/api/collections/Sentinel-2A",
            payload=collection,
        )

        data = await get_collection("Sentinel-2A")

        assert data == Collection(**collection)
        m.assert_called_once_with(
            "http://test-stac-api.mock.com/api/collections/Sentinel-2A"
        )


def test_api_core(core_api):
    """Test the OpenEOApi and OpenEOCore classes interact as intended."""

    assert isinstance(core_api, OpenEOApi)
    assert isinstance(core_api.app, FastAPI)


def test_get_capabilities(core_api):
    """Test the OpenEOApi and OpenEOCore classes interact as intended."""

    test_app = TestClient(core_api.app)

    response = test_app.get("/")

    assert response.status_code == 200
    assert response.json()["title"] == "Test Api"


# def test_get_collections(core_api):
#    """Test the OpenEOApi and OpenEOCore classes interact as intended."""
#
#    test_app = TestClient(core_api.app)
#
#    response = test_app.get("/collections")
#
#    assert response.status_code == 200
#    assert isinstance(response.json()["collections"], list)
#
#
# def test_get_collection(core_api):
#    """Test the OpenEOApi and OpenEOCore classes interact as intended."""
#
#    test_app = TestClient(core_api.app)
#
#    response = test_app.get("/collections/viirs-15a2h-001")
#
#    assert response.status_code == 200
#    assert response.json()["id"] == "viirs-15a2h-001"
