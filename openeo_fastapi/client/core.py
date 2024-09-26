"""Class and model to define the framework and partial application logic for interacting with Jobs.

Classes:
    - OpenEOCore: Framework for defining the application logic that will passed onto the OpenEO Api.
"""
from collections import namedtuple
from typing import Optional
from urllib.parse import urlunparse

from attrs import define, field
from fastapi import Depends, HTTPException, Response

from openeo_fastapi.api.models import (
    Capabilities,
    ConformanceGetResponse,
    CredentialsOidcGetResponse,
    DefaultClient,
    FileFormatsGetResponse,
    GrantType,
    MeGetResponse,
    Provider,
    UdfRuntimesGetResponse,
    WellKnownOpeneoGetResponse,
)
from openeo_fastapi.api.types import Error, STACConformanceClasses, Version
from openeo_fastapi.client.auth import Authenticator, User
from openeo_fastapi.client.collections import CollectionRegister
from openeo_fastapi.client.files import FilesRegister
from openeo_fastapi.client.jobs import JobsRegister
from openeo_fastapi.client.processes import ProcessRegister
from openeo_fastapi.client.settings import AppSettings


@define
class OpenEOCore:
    """Client for defining the application logic for the OpenEO Api."""

    billing: str = field()
    input_formats: list = field()
    output_formats: list = field()
    links: list = field()

    settings: AppSettings = None

    _id: str = field(default="OpenEOApi")

    collections: Optional[CollectionRegister] = None
    files: Optional[FilesRegister] = None
    jobs: Optional[JobsRegister] = None
    processes: Optional[ProcessRegister] = None

    def __attrs_post_init__(self):
        """Post init hook to set the client registers, if none where provided by the user set to the defaults!"""
        self.settings = AppSettings()

        self.collections = self.collections or CollectionRegister(self.settings)
        self.files = self.files or FilesRegister(self.settings, self.links)
        self.jobs = self.jobs or JobsRegister(self.settings, self.links)
        self.processes = self.processes or ProcessRegister(self.links)

    def _combine_endpoints(self):
        """For the various registers that hold endpoint functions, concat those endpoints to register in get_capabilities.

        Returns:
            List: A list of all the endpoints that will be supported by this api deployment.
        """
        registers = [self.collections, self.files, self.jobs, self.processes]

        endpoints = []
        for register in registers:
            if register:
                endpoints.extend(register.endpoints)
        return endpoints

    def get_capabilities(self) -> Capabilities:
        """Get the capabilities of the api.

        Returns:
            Capabilities: The capabilities of the api based off what the user provided.
        """
        return Capabilities(
            id=self._id,
            title=self.settings.API_TITLE,
            stac_version=self.settings.STAC_VERSION,
            api_version=self.settings.OPENEO_VERSION,
            description=self.settings.API_DESCRIPTION,
            backend_version=self.settings.OPENEO_VERSION,
            billing=self.billing,
            links=self.links,
            endpoints=self._combine_endpoints(),
        )

    def get_credentials_oidc(self) -> CredentialsOidcGetResponse:
        """Get the capabilities of the api.

        Returns:
            Capabilities: The capabilities of the api based off what the user provided.
        """
        return CredentialsOidcGetResponse(
            providers=[
                Provider(
                    id=self.settings.OIDC_ORGANISATION,
                    title="EGI Check-in",
                    issuer=self.settings.OIDC_URL,
                    scopes=[
                        "openid",
                        "email",
                        "eduperson_entitlement",
                        "eduperson_scoped_affiliation",
                    ],
                    default_clients=[
                        DefaultClient(
                            id="openeo-platform-default-client",
                            redirect_urls=[
                                "https://editor.openeo.cloud",
                                "https://editor.openeo.org",
                                "http://localhost:1410/",
                            ],
                            grant_types=[
                                GrantType.authorization_code_pkce,
                                GrantType.urn_ietf_params_oauth_grant_type_device_code_pkce,
                                GrantType.refresh_token,
                            ],
                        )
                    ],
                )
            ]
        )

    def get_conformance(self) -> ConformanceGetResponse:
        """Get the capabilities of the api.

        Returns:
            ConformanceGetResponse: The conformance classes that this Api wil of the api based off what the user provided.
        """
        return ConformanceGetResponse(
            conformsTo=[
                STACConformanceClasses.CORE.value,
                STACConformanceClasses.COLLECTIONS.value,
            ]
        )

    def get_file_formats(self) -> FileFormatsGetResponse:
        """Get the supported file formats for processing input and output.

        Returns:
            FileFormatsGetResponse: The response defining the input and output formats.
        """
        return FileFormatsGetResponse(
            input={_format.title: _format for _format in self.input_formats},
            output={_format.title: _format for _format in self.output_formats},
        )

    def get_health(self):
        """Basic health endpoint expected to return status code 200.

        Returns:
            Response: Status code 200.
        """
        return Response(status_code=200, content="OK")

    def get_user_info(
        self, user: User = Depends(Authenticator.validate)
    ) -> MeGetResponse:
        """Get the supported file formats for processing input and output.

        Returns:
            MeGetResponse: The user information for the validated user.
        """
        return MeGetResponse(user_id=user.user_id)

    def get_well_known(self) -> WellKnownOpeneoGetResponse:
        """Get the supported file formats for processing input and output.

        Returns:
            WellKnownOpeneoGetResponse: The api/s which are exposed at this server.
        """
        prefix = "https" if self.settings.API_TLS else "http"

        Components = namedtuple(
            typename="Components",
            field_names=["scheme", "netloc", "url", "path", "query", "fragment"],
        )

        # TODO Supporting multiple versions should be possible here. But would change how we get the api version.
        url = urlunparse(
            Components(
                scheme=prefix,
                netloc=self.settings.API_DNS,
                query=None,
                path="",
                url=f"/openeo/{self.settings.OPENEO_VERSION}/",
                fragment=None,
            )
        )

        return WellKnownOpeneoGetResponse(
            versions=[
                Version(
                    url=url, production=False, api_version=self.settings.OPENEO_VERSION
                )
            ]
        )

    def get_udf_runtimes(self) -> UdfRuntimesGetResponse:
        """Get the supported file formats for processing input and output.

        Raises:
            HTTPException: Raises an exception with relevant status code and descriptive message of failure.

        Returns:
            UdfRuntimesGetResponse: The metadata for the requested BatchJob.
        """
        raise HTTPException(
            status_code=501,
            detail=Error(code="FeatureUnsupported", message="Feature not supported."),
        )
