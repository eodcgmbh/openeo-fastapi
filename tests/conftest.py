import json
from unittest.mock import patch

import pytest
from fastapi import FastAPI
from requests import Response

from openeo_fastapi.api.app import OpenEOApi
from openeo_fastapi.client import auth, models
from openeo_fastapi.client.core import OpenEOCore


@pytest.fixture()
def core_api():
    client = OpenEOCore(
        api_dns="test.api.org",
        api_tls=True,
        title="Test Api",
        description="My Test Api",
        backend_version="1",
        links=[
            models.Link(
                href="https://eodc.eu/",
                rel="about",
                type="text/html",
                title="Homepage of the service provider",
            )
        ],
        billing=models.Billing(
            currency="credits",
            default_plan="a-cloud",
            plans=[
                models.Plan(name="user", description="Subscription plan.", paid=True)
            ],
        ),
        endpoints=[
            models.Endpoint(
                path="/",
                methods=["GET"],
            )
        ],
    )

    api = OpenEOApi(client=client, app=FastAPI())

    return api


@pytest.fixture()
def mocked_oidc_config():
    resp_content_bytes = json.dumps(
        {"userinfo_endpoint": "http://nothere.test"}
    ).encode("utf-8")

    mocked_response = Response()
    mocked_response.status_code = 200
    mocked_response._content = resp_content_bytes

    with patch("openeo_fastapi.client.auth.IssuerHandler._get_issuer_config") as mock:
        mock.return_value = mocked_response
        yield mock


@pytest.fixture()
def mocked_oidc_userinfo():
    resp_content_bytes = json.dumps(
        {
            "eduperson_entitlement": [
                "entitlment",
            ],
            "sub": "someuser@testing.test",
        }
    ).encode("utf-8")

    mocked_response = Response()
    mocked_response.status_code = 200
    mocked_response._content = resp_content_bytes

    with patch("openeo_fastapi.client.auth.IssuerHandler._get_user_info") as mock:
        mock.return_value = mocked_response
        yield mock


@pytest.fixture()
def mocked_bad_oidc_config():
    mocked_response = Response()
    mocked_response.status_code = 404

    with patch("openeo_fastapi.client.auth.IssuerHandler._get_issuer_config") as mock:
        mock.return_value = mocked_response
        yield mock


@pytest.fixture()
def mocked_bad_oidc_userinfo():
    mocked_response = Response()
    mocked_response.status_code = 404

    with patch("openeo_fastapi.client.auth.IssuerHandler._get_user_info") as mock:
        mock.return_value = mocked_response
        yield mock


@pytest.fixture()
def mocked_issuer():
    return auth.IssuerHandler(
        issuer_url="http://issuer.mycloud/",
        organisation="mycloud",
        roles=["admin", "user"],
    )
