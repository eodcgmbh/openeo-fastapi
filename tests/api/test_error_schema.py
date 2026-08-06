from fastapi import HTTPException
from fastapi.testclient import TestClient

import pytest

from openeo_fastapi.api.app import DEFAULT_ERROR_CODES, OpenEOApi, to_openeo_error
from openeo_fastapi.api.types import Error
from openeo_fastapi.client.auth import AuthToken, IssuerHandler


@pytest.fixture()
def postgresql():
    """Connect to an externally-managed PostgreSQL (dockerized) instead of spawning one."""

    import psycopg2

    conn = psycopg2.connect(
        host="localhost", port=55432, user="postgres", password="postgres"
    )
    conn.autocommit = True
    cur = conn.cursor()
    cur.execute("DROP DATABASE IF EXISTS openeo_fastapi_test")
    cur.execute("CREATE DATABASE openeo_fastapi_test")
    conn.close()

    class Info:
        user = "postgres"
        password = "postgres"
        host = "localhost"
        port = 55432
        dbname = "openeo_fastapi_test"

    class _Fake:
        info = Info()

    return _Fake()



def test_to_openeo_error_wraps_string_detail():
    assert to_openeo_error(404, "Not found") == {
        "code": "NotFound",
        "message": "Not found",
    }


def test_to_openeo_error_preserves_error_object():
    error = Error(code="CustomCode", message="A message")
    assert to_openeo_error(404, error) == error.dict(exclude_none=True)


def test_to_openeo_error_preserves_code_message_dict():
    assert to_openeo_error(404, {"code": "Custom", "message": "msg"}) == {
        "code": "Custom",
        "message": "msg",
    }


def test_to_openeo_error_unknown_status_uses_bad_request():
    assert to_openeo_error(599, "something")["code"] == "BadRequest"


def test_http_exception_with_string_detail_is_wrapped(core_api):
    test_client = TestClient(core_api.app)

    @core_api.app.get("/test-string-error")
    def test_string_error():
        raise HTTPException(status_code=400, detail="Job is already finished.")

    response = test_client.get("/test-string-error")

    assert response.status_code == 400
    assert response.json() == {
        "code": "BadRequest",
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

    # A JSON body that fails model validation, e.g. wrong type for a field.
    response = test_client.post(
        "/openeo/1.1.0/jobs", json={"process": "not-a-dict"}
    )

    assert response.status_code == 422
    body = response.json()
    assert body["code"] == "InvalidRequest"
    assert body["message"]


def test_error_code_defaults_cover_spec_statuses():
    for status in (400, 401, 403, 404, 405, 422, 429, 500):
        assert DEFAULT_ERROR_CODES[status]


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
    """HTTPException headers (e.g. WWW-Authenticate on 401) must be passed through."""

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



def test_auth_token_from_none_raises_value_error():
    try:
        AuthToken.from_token(None)
    except ValueError as e:
        assert "Token is required" in str(e)
    else:
        raise AssertionError("from_token(None) should raise ValueError")


def test_validate_token_none_raises_authentication_required():
    handler = IssuerHandler(issuer_uri="https://issuer.example.com")
    try:
        handler.validate_token(None)
    except HTTPException as e:
        assert e.status_code == 401
        detail = e.detail
        assert detail.code == "AuthenticationRequired"
    else:
        raise AssertionError("validate_token(None) should raise HTTPException 401")
