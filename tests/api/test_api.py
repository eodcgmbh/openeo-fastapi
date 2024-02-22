import os
from unittest import mock

import pytest
from aioresponses import aioresponses
from fastapi import FastAPI
from fastapi.testclient import TestClient

from openeo_fastapi.api.app import OpenEOApi
from openeo_fastapi.client.models import Collection


def test_api_core(core_api):
    """Test the OpenEOApi and OpenEOCore classes interact as intended."""

    assert isinstance(core_api, OpenEOApi)
    assert isinstance(core_api.app, FastAPI)


def test_get_capabilities(core_api, app_settings):
    """Test the OpenEOApi and OpenEOCore classes interact as intended."""

    test_app = TestClient(core_api.app)

    response = test_app.get(f"/{app_settings.OPENEO_VERSION}/")

    assert response.status_code == 200
    assert response.json()["title"] == "Test Api"


def test_get_conformance(core_api, app_settings):
    """Test the /conformance endpoint as intended."""

    from openeo_fastapi.client.conformance import BASIC_CONFORMANCE_CLASSES

    test_app = TestClient(core_api.app)

    response = test_app.get(f"/{app_settings.OPENEO_VERSION}/conformance")

    assert response.status_code == 200
    assert len(BASIC_CONFORMANCE_CLASSES) == len(response.json()["conformsTo"])


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
    with mock.patch.dict(os.environ, {"STAC_COLLECTIONS_WHITELIST": "Sentinel-2A"}):
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


def test_get_processes(core_api, app_settings):
    """Test the /processes endpoint as intended."""

    test_app = TestClient(core_api.app)

    response = test_app.get(f"/{app_settings.OPENEO_VERSION}/processes")

    assert response.status_code == 200
    assert "processes" in response.json().keys()
