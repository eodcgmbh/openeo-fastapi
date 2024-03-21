import importlib.metadata
import json
import os
from pathlib import Path
from unittest import mock
from unittest.mock import patch

import fsspec
import pytest
from fastapi import FastAPI
from requests import Response

pytestmark = pytest.mark.unit
path_to_current_file = os.path.realpath(__file__)
current_directory = os.path.split(path_to_current_file)[0]

# Have the version ready for using as an autorevision name
__version__ = importlib.metadata.version("openeo_fastapi")

# A user needs to have an alembic directory for the auto generated revisions to be added to.
ALEMBIC_DIR = Path(__file__).parent.parent / "tests/alembic/"

fs = fsspec.filesystem(protocol="file")

SETTINGS_DICT = {
    "API_DNS": "http://test.api.org",
    "API_TLS": "False",
    "API_TITLE": "Test Api",
    "API_DESCRIPTION": "My Test Api",
    "STAC_API_URL": "http://test-stac-api.mock.com/api/",
    "ALEMBIC_DIR": str(ALEMBIC_DIR),
    "OIDC_URL": "http://test-oidc-api.mock.com/api/",
    "OIDC_ORGANISATION": "issuer",
}
os.environ["ALEMBIC_DIR"] = str(ALEMBIC_DIR)
os.environ["API_DNS"] = "http://test.api.org"
os.environ["API_TLS"] = "False"
os.environ["API_TITLE"] = "Test Api"
os.environ["API_DESCRIPTION"] = "My Test Api"
os.environ["STAC_API_URL"] = "http://test-stac-api.mock.com/api/"
os.environ["OIDC_URL"] = "http://test-oidc-api.mock.com/api/"
os.environ["OIDC_ORGANISATION"] = "issuer"
os.environ["OIDC_ROLES"] = "tester,developer"

from openeo_fastapi.api.app import OpenEOApi
from openeo_fastapi.client import auth, models, settings
from openeo_fastapi.client.core import CollectionRegister, OpenEOCore


@pytest.fixture()
def app_settings():
    return settings.AppSettings(**SETTINGS_DICT)


@pytest.fixture()
def core_api():
    client = OpenEOCore(
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
def job_post():
    with open(os.path.join(current_directory, "data/fake-job-post.json")) as f_in:
        return json.load(f_in)


@pytest.fixture()
def collections():
    with open(os.path.join(current_directory, "data/collections.json")) as f_in:
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


@pytest.fixture(autouse=True)
def mock_engine(postgresql):
    """Postgresql engine for SQLAlchemy."""
    import os
    from pathlib import Path

    from alembic import command
    from alembic.config import Config

    from openeo_fastapi.client.psql.engine import get_engine

    os.chdir(Path(ALEMBIC_DIR))

    # Set the env vars that alembic will use for DB connection and run alembic engine from CLI!
    os.environ["POSTGRES_USER"] = postgresql.info.user
    os.environ["POSTGRES_PASSWORD"] = "postgres"
    os.environ["POSTGRESQL_HOST"] = postgresql.info.host
    os.environ["POSTGRESQL_PORT"] = str(postgresql.info.port)
    os.environ["POSTGRES_DB"] = postgresql.info.dbname

    alembic_cfg = Config("alembic.ini")

    command.revision(alembic_cfg, f"openeo-fastapi-{__version__}", autogenerate=True)
    command.upgrade(alembic_cfg, "head")

    engine = get_engine()

    return engine


@pytest.fixture(scope="function", autouse=True)
def cleanup_out_folder():
    # Path to test alembic versions folder
    alembic_version_dir = str(ALEMBIC_DIR / "alembic/versions")
    alembic_pycache = str(ALEMBIC_DIR / "__pycache__")
    alembic_cache_dir = str(ALEMBIC_DIR / "alembic/__pycache__")
    alembic_ver_cache_dir = str(ALEMBIC_DIR / "alembic/versions/__pycache__")

    if not fs.exists(alembic_version_dir):
        fs.mkdir(alembic_version_dir)

    yield  # Yield to the running tests

    # Teardown: Delete the output folder,
    if fs.exists(alembic_version_dir):
        for file in fs.ls(alembic_version_dir):
            fs.rm(file, recursive=True)
        fs.rmdir(alembic_version_dir)

    # Remove alembic pycaches
    if fs.exists(alembic_pycache):
        fs.rm(alembic_pycache, recursive=True)

    if fs.exists(alembic_ver_cache_dir):
        fs.rm(alembic_ver_cache_dir, recursive=True)

    if fs.exists(alembic_cache_dir):
        fs.rm(alembic_cache_dir, recursive=True)
