from collections import namedtuple
from typing import Optional
from urllib.parse import urlunparse

from attrs import define, field
from fastapi import Depends, HTTPException, Response

from openeo_fastapi.api import responses, types
from openeo_fastapi.client import conformance
from openeo_fastapi.client.auth import Authenticator, User
from openeo_fastapi.client.collections import CollectionRegister
from openeo_fastapi.client.files import FilesRegister
from openeo_fastapi.client.jobs import JobsRegister
from openeo_fastapi.client.processes import ProcessRegister
from openeo_fastapi.client.settings import AppSettings


@define
class OpenEOCore:
    """Base client for the OpenEO Api."""

    billing: str = field()
    input_formats: list = field()
    output_formats: list = field()
    links: list = field()

    settings = AppSettings()

    _id: str = field(default="OpenEOApi")

    collections: Optional[CollectionRegister] = None
    files: Optional[FilesRegister] = None
    jobs: Optional[JobsRegister] = None
    processes: Optional[ProcessRegister] = None

    def __attrs_post_init__(self):
        """
        Post init hook to set the register objects for the class if none where provided by the user!
        """
        self.collections = self.collections or CollectionRegister(self.settings)
        self.files = self.files or FilesRegister(self.settings, self.links)
        self.jobs = self.jobs or JobsRegister(self.settings, self.links)
        self.processes = self.processes or ProcessRegister(self.links)

    def _combine_endpoints(self):
        """For the various registers that hold endpoint functions, concat those endpoints to register in get_capabilities."""
        registers = [self.collections, self.files, self.jobs, self.processes]

        endpoints = []
        for register in registers:
            if register:
                endpoints.extend(register.endpoints)
        return endpoints

    def get_well_known(self) -> responses.WellKnownOpeneoGetResponse:
        """ """

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

        return responses.WellKnownOpeneoGetResponse(
            versions=[
                responses.Version(
                    url=url, production=False, api_version=self.settings.OPENEO_VERSION
                )
            ]
        )

    def get_capabilities(self) -> responses.Capabilities:
        """ """
        return responses.Capabilities(
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

    def get_conformance(self) -> responses.ConformanceGetResponse:
        """ """
        return responses.ConformanceGetResponse(
            conformsTo=conformance.BASIC_CONFORMANCE_CLASSES
        )

    def get_file_formats(self) -> responses.FileFormatsGetResponse:
        """ """
        return responses.FileFormatsGetResponse(
            input={_format.title: _format for _format in self.input_formats},
            output={_format.title: _format for _format in self.output_formats},
        )

    def get_user_info(
        self, user: User = Depends(Authenticator.validate)
    ) -> responses.MeGetResponse:
        """ """
        return responses.MeGetResponse(user_id=user.user_id.__str__())

    def get_health(self):
        """ """
        return Response(status_code=200, content="OK")

    def udf_runtimes(self) -> responses.UdfRuntimesGetResponse:
        """ """
        raise HTTPException(
            status_code=501,
            detail=types.Error(
                code="FeatureUnsupported", message="Feature not supported."
            ),
        )
