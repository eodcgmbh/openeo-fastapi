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

    core_api.register_get_capabilities()

    response = test_app.get("/")

    assert response.status_code == 200
    assert response.json()["title"] == "Test Api"


def test_get_conformance(core_api):
    """Test the OpenEOApi capabilities endpoint is activate."""

    test_app = TestClient(core_api.app)

    core_api.register_get_conformance()

    response = test_app.get("/conformance")

    assert response.status_code == 200


def test_get_conformance(core_api):
    """Test the OpenEOApi capabilities endpoint is activate."""

    test_app = TestClient(core_api.app)

    core_api.register_get_conformance()

    response = test_app.get("/.well-known/openeo")

    assert response.status_code == 200
