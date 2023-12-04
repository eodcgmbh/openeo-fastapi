from fastapi import FastAPI
from fastapi.testclient import TestClient

from openeo_fastapi.api.app import OpenEOApi


def test_api_core(core_api):
    """Test the OpenEOApi and OpenEOCore classes interact as intended."""

    assert isinstance(core_api, OpenEOApi)
    assert isinstance(core_api.app, FastAPI)


def test_get_capabilities(core_api):
    """Test the OpenEOApi and OpenEOCore classes interact as intended."""

    core_api.register_get_capabilities()

    test_app = TestClient(core_api.app)

    response = test_app.get("/")

    assert response.status_code == 200
    assert response.text == '{"version": "1"}'
