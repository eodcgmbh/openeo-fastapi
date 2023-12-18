from fastapi import FastAPI
from fastapi.testclient import TestClient

from openeo_fastapi.api.app import OpenEOApi


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


def test_get_collections(core_api):
    """Test the OpenEOApi and OpenEOCore classes interact as intended."""

    test_app = TestClient(core_api.app)

    response = test_app.get("/collections")

    assert response.status_code == 200
    assert isinstance(response.json()["collections"], list)


def test_get_collection(core_api):
    """Test the OpenEOApi and OpenEOCore classes interact as intended."""

    test_app = TestClient(core_api.app)

    response = test_app.get("/collections/viirs-15a2h-001")

    assert response.status_code == 200
    assert response.json()["id"] == "viirs-15a2h-001"
