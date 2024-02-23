import json
import os
from unittest import mock
from unittest.mock import patch

import pytest
from fastapi import FastAPI
from requests import Response

from openeo_fastapi.api.app import OpenEOApi
from openeo_fastapi.client import auth, models, settings
from openeo_fastapi.client.core import CollectionRegister, OpenEOCore

pytestmark = pytest.mark.unit
path_to_current_file = os.path.realpath(__file__)
current_directory = os.path.split(path_to_current_file)[0]


@pytest.fixture(autouse=True)
def mock_settings_env_vars():
    with mock.patch.dict(
        os.environ,
        {
            "API_DNS": "test.api.org",
            "API_TLS": "False",
            "API_TITLE": "Test Api",
            "API_DESCRIPTION": "My Test Api",
            "STAC_API_URL": "http://test-stac-api.mock.com/api/",
        },
    ):
        yield


@pytest.fixture()
def app_settings():
    return settings.AppSettings()


@pytest.fixture()
def core_api():
    client = OpenEOCore(
        settings=settings.AppSettings(),
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
    )

    api = OpenEOApi(client=client, app=FastAPI())

    return api


@pytest.fixture()
def collections_core():
    return CollectionRegister(settings.AppSettings())


@pytest.fixture()
def collections():
    with open(os.path.join(current_directory, "collections.json")) as f_in:
        return json.load(f_in)


@pytest.fixture
def s2a_collection(collections):
    return collections["collections"][0]


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
