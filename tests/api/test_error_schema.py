from fastapi import HTTPException
from fastapi.testclient import TestClient

import pytest

from openeo_fastapi.api.app import OpenEOApi, to_openeo_error
from openeo_fastapi.api.types import Error


def test_to_openeo_error_wraps_string_detail():
    assert to_openeo_error("Not found", "NotFound") == {
        "code": "NotFound",
        "message": "Not found",
    }


def test_to_openeo_error_preserves_error_object():
    error = Error(code="CustomCode", message="A message")
    assert to_openeo_error(error, "SomeDefault") == error.dict(exclude_none=True)


def test_to_openeo_error_preserves_code_message_dict():
    assert to_openeo_error({"code": "Custom", "message": "msg"}, "SomeDefault") == {
        "code": "Custom",
        "message": "msg",
    }


def test_http_exception_with_string_detail_is_wrapped(core_api):
    test_client = TestClient(core_api.app)

    @core_api.app.get("/test-string-error")
    def test_string_error():
        raise HTTPException(status_code=400, detail="Job is already finished.")

    response = test_client.get("/test-string-error")

    assert response.status_code == 400
    assert response.json() == {
        "code": "Internal",
        "message": "Job is already finished.",
    }


def test_unknown_route_returns_openeo_error(core_api):
    test_client = TestClient(core_api.app)

    response = test_client.get("/this-does-not-exist")

    assert response.status_code == 404
    body = response.json()
    assert body["code"] == "NotFound"
    assert body["message"]


def test_wrong_method_returns_openeo_error(core_api):
    test_client = TestClient(core_api.app)

    response = test_client.post("/.well-known/openeo/")

    assert response.status_code == 405
    body = response.json()
    assert body["code"] == "MethodNotAllowed"
    assert body["message"]


def test_validation_error_returns_openeo_error(core_api):
    test_client = TestClient(core_api.app)

    response = test_client.post(
        "/openeo/1.1.0/jobs", json={"process": "not-a-dict"}
    )

    assert response.status_code == 422
    body = response.json()
    assert body["code"] == "InvalidRequest"
    assert body["message"]


def test_unhandled_exception_returns_500_openeo_error(core_api):
    test_client = TestClient(core_api.app, raise_server_exceptions=False)

    @core_api.app.get("/test-unhandled-error")
    def unhandled_error():
        raise RuntimeError("something went wrong")

    response = test_client.get("/test-unhandled-error")
    assert response.status_code == 500
    body = response.json()
    assert body == {
        "code": "Internal",
        "message": "Server error: An internal server error occurred.",
    }
    assert "something went wrong" not in response.text


def test_http_exception_headers_are_preserved(core_api):
    test_client = TestClient(core_api.app)

    @core_api.app.get("/test-www-authenticate")
    def www_authenticate():
        raise HTTPException(
            status_code=401,
            detail=Error(
                code="AuthenticationRequired",
                message="Authentication is required for this endpoint.",
            ),
            headers={"WWW-Authenticate": "Bearer"},
        )

    response = test_client.get("/test-www-authenticate")
    assert response.status_code == 401
    assert response.headers["www-authenticate"] == "Bearer"
    assert response.json()["code"] == "AuthenticationRequired"
