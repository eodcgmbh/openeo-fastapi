import uuid
from typing import Optional

import pytest
from fastapi import Depends, FastAPI, HTTPException, Response
from fastapi.testclient import TestClient
from sqlalchemy import Column
from sqlalchemy.exc import IntegrityError
from sqlalchemy.types import BOOLEAN

from openeo_fastapi.api.app import OpenEOApi
from openeo_fastapi.api.models import FilesGetResponse
from openeo_fastapi.api.types import (
    Billing,
    Endpoint,
    File,
    FileFormat,
    GisDataType,
    Link,
    Plan,
)
from openeo_fastapi.client.auth import Authenticator, User
from openeo_fastapi.client.core import OpenEOCore
from openeo_fastapi.client.files import FILE_ENDPOINTS, FilesRegister
from openeo_fastapi.client.psql.models import UserORM


def test_api_core(core_api):
    """Test the OpenEOApi and OpenEOCore classes interact as intended."""

    assert isinstance(core_api, OpenEOApi)
    assert isinstance(core_api.app, FastAPI)


def test_get_wellknown(core_api, app_settings):
    """Test the OpenEOApi and OpenEOCore classes interact as intended."""

    test_app = TestClient(core_api.app)

    response = test_app.get(f"/.well-known/openeo/")

    assert response.status_code == 200


def test_get_capabilities(core_api, app_settings):
    """Test the OpenEOApi and OpenEOCore classes interact as intended."""

    test_app = TestClient(core_api.app)

    response = test_app.get(f"/{app_settings.OPENEO_VERSION}/")

    assert response.status_code == 200
    assert response.json()["title"] == "Test Api"


def test_get_health(core_api, app_settings):
    """Test the health endpoint is available."""

    test_app = TestClient(core_api.app)

    response = test_app.get(f"/{app_settings.OPENEO_VERSION}/health")

    assert response.status_code == 200


def test_get_userinfo(mocked_oidc_config, mocked_oidc_userinfo, core_api, app_settings):
    """Test the user info is available."""

    test_app = TestClient(core_api.app)

    response = test_app.get(
        f"/{app_settings.OPENEO_VERSION}/me",
        headers={"Authorization": "Bearer /oidc/egi/not-real"},
    )

    assert response.status_code == 200
    assert "user_id" in response.json()


def test_get_udf_runtimes(core_api, app_settings):
    """Test the udf runtimes endpoint is registered."""

    test_app = TestClient(core_api.app)

    response = test_app.get(f"/{app_settings.OPENEO_VERSION}/udf_runtimes")

    assert response.status_code == 501


def test_get_conformance(core_api, app_settings):
    """Test the /conformance endpoint as intended."""

    test_app = TestClient(core_api.app)

    response = test_app.get(f"/{app_settings.OPENEO_VERSION}/conformance")

    assert response.status_code == 200
    assert 2 == len(response.json()["conformsTo"])


def test_get_file_formats(core_api, app_settings):
    """Test the /conformance endpoint as intended."""

    test_app = TestClient(core_api.app)

    response = test_app.get(f"/{app_settings.OPENEO_VERSION}/file_formats")

    assert response.status_code == 200


def test_exception_handler(core_api):
    test_client = TestClient(core_api.app)

    # Define a route that raises an exception
    @core_api.app.get("/test-exception")
    def test_exception():
        raise HTTPException(
            status_code=404,
            detail={"code": "NotFound", "message": "This is a test exception"},
        )

    response = test_client.get("/test-exception")

    assert response.status_code == 404

    # Assert that the response body matches the expected response generated by the exception handler
    expected_response = {"code": "NotFound", "message": "This is a test exception"}
    assert response.json() == expected_response


def test_overwriting_register(mocked_oidc_config, mocked_oidc_userinfo, app_settings):
    """Test we are able to over write the file register, and in turn the API endpoint."""

    class ExtendedFileRegister(FilesRegister):
        def __init__(self, settings, links) -> None:
            super().__init__(settings, links)

        def list_files(
            self,
            limit: Optional[int] = 10,
            user: User = Depends(Authenticator.validate),
        ):
            """ """
            return FilesGetResponse(
                files=[File(path="/somefile.txt", size=10)],
                links=[
                    Link(
                        href="https://eodc.eu/",
                        rel="about",
                        type="text/html",
                        title="Homepage of the service provider",
                    )
                ],
            )

    test_links = [
        Link(
            href="https://test.eu/",
            rel="about",
            type="text/html",
            title="Homepage of the service provider",
        )
    ]

    extended_register = ExtendedFileRegister(app_settings, test_links)

    formats = [
        FileFormat(
            title="json",
            gis_data_types=[GisDataType("vector")],
            parameters={},
        )
    ]

    client = OpenEOCore(
        input_formats=formats,
        output_formats=formats,
        links=[
            Link(
                href="https://eodc.eu/",
                rel="about",
                type="text/html",
                title="Homepage of the service provider",
            )
        ],
        billing=Billing(
            currency="credits",
            default_plan="a-cloud",
            plans=[Plan(name="user", description="Subscription plan.", paid=True)],
        ),
        files=extended_register,
    )

    api = OpenEOApi(client=client, app=FastAPI())

    test_client = test_client = TestClient(api.app)
    response = test_client.get(
        f"/{app_settings.OPENEO_VERSION}/files",
        headers={"Authorization": "Bearer /oidc/egi/not-real"},
    )

    assert response.status_code == 200


def test_extending_register(mocked_oidc_config, mocked_oidc_userinfo, app_settings):
    """Test we are able to extend the file register, and in turn the API."""

    new_endpoint = Endpoint(
        path="/files/{path}",
        methods=["HEAD"],
    )

    class ExtendedFileRegister(FilesRegister):
        def __init__(self, settings, links) -> None:
            super().__init__(settings, links)
            self.endpoints = self._initialize_endpoints()

        def _initialize_endpoints(self) -> list[Endpoint]:
            endpoints = list(FILE_ENDPOINTS)
            endpoints.append(new_endpoint)
            return endpoints

        def get_file_headers(
            self, path: str, user: User = Depends(Authenticator.validate)
        ):
            """ """
            return Response(
                status_code=200,
                headers={
                    "Accept-Ranges": "bytes",
                },
            )

    test_links = [
        Link(
            href="https://test.eu/",
            rel="about",
            type="text/html",
            title="Homepage of the service provider",
        )
    ]

    extended_register = ExtendedFileRegister(app_settings, test_links)

    # Asser the new endpoint has been added to the register endpoints
    assert len(extended_register.endpoints) == 5
    assert new_endpoint in extended_register.endpoints

    formats = [
        FileFormat(
            title="json",
            gis_data_types=[GisDataType("vector")],
            parameters={},
        )
    ]

    client = OpenEOCore(
        input_formats=formats,
        output_formats=formats,
        links=[
            Link(
                href="https://eodc.eu/",
                rel="about",
                type="text/html",
                title="Homepage of the service provider",
            )
        ],
        billing=Billing(
            currency="credits",
            default_plan="a-cloud",
            plans=[Plan(name="user", description="Subscription plan.", paid=True)],
        ),
        files=extended_register,
    )

    api = OpenEOApi(client=client, app=FastAPI())

    # Assert we have not brokebn the api initialisation
    assert api

    # Add the new route from the api to the app router
    api.app.router.add_api_route(
        name="file_headers",
        path=f"/{api.client.settings.OPENEO_VERSION}/files" + "/{path}",
        response_model=None,
        response_model_exclude_unset=False,
        response_model_exclude_none=True,
        methods=["HEAD"],
        endpoint=api.client.files.get_file_headers,
    )

    test_client = test_client = TestClient(api.app)
    response = test_client.head(
        f"/{app_settings.OPENEO_VERSION}/files/somefile.txt",
        headers={"Authorization": "Bearer /oidc/egi/not-real"},
    )

    assert response.status_code == 200


def test_overwrite_authenticator_validate(
    mocked_oidc_config, mocked_oidc_userinfo, core_api, app_settings
):
    """Test the user info is available."""

    test_app = TestClient(core_api.app)

    specific_uuid = uuid.uuid4()

    def my_new_cool_auth():
        return User(user_id=specific_uuid, oidc_sub="the-real-user")

    core_api.override_authentication(my_new_cool_auth)

    response = test_app.get(
        f"/{app_settings.OPENEO_VERSION}/me",
        headers={"Authorization": "Bearer /oidc/egi/not-real"},
    )

    assert response.status_code == 200
    assert "user_id" in response.json()
    assert response.json()["user_id"] == str(specific_uuid)


@pytest.mark.skip(
    reason="Can only be run independently, as it revisions the database and will break the tests which run after."
)
def test_extending_the_usermodel(
    mocked_oidc_config, mocked_oidc_userinfo, core_api, app_settings
):
    """Test the user model can be extended in the api available."""

    # Extend the UserORM class
    class ExtendedUserORM(UserORM):
        """ORM for the UserORM table."""

        new_value = Column(BOOLEAN, nullable=False)

    # Try to revise the database using the extended UserORM
    import os
    from pathlib import Path

    from alembic import command
    from alembic.config import Config

    from tests.conftest import ALEMBIC_DIR

    os.chdir(Path(ALEMBIC_DIR))
    alembic_cfg = Config("alembic.ini")

    command.revision(
        alembic_cfg, f"openeo-fastapi-extended", rev_id="downgrademe", autogenerate=True
    )
    command.upgrade(alembic_cfg, revision="downgrademe")

    test_app = TestClient(core_api.app)

    with pytest.raises(IntegrityError):
        test_app.get(
            f"/{app_settings.OPENEO_VERSION}/me",
            headers={"Authorization": "Bearer /oidc/egi/not-real"},
        )

    def my_new_cool_auth():
        return User(user_id=uuid.uuid4(), oidc_sub="the-real-user", new_value=True)

    core_api.override_authentication(my_new_cool_auth)

    response = test_app.get(
        f"/{app_settings.OPENEO_VERSION}/me",
        headers={"Authorization": "Bearer /oidc/egi/not-real"},
    )

    # Downgrade to remove the use of the ExtendedUserORM
    # Doesnt seem to work
    command.downgrade(alembic_cfg, revision="downgrademe")

    assert response.status_code == 200
