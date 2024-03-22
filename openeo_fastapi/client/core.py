from collections import namedtuple
from typing import Optional
from urllib.parse import urlunparse

from attrs import define, field

from openeo_fastapi.client import conformance, models
from openeo_fastapi.client.collections import CollectionRegister
from openeo_fastapi.client.jobs import JobsRegister
from openeo_fastapi.client.processes import ProcessRegister
from openeo_fastapi.client.settings import AppSettings


@define
class OpenEOCore:
    """Base client for the OpenEO Api."""

    billing: str = field()
    links: list = field()

    settings = AppSettings()

    _id: str = field(default="OpenEOApi")

    _collections: Optional[CollectionRegister] = None
    _jobs: Optional[JobsRegister] = None
    _processes: Optional[ProcessRegister] = None

    def __attrs_post_init__(self):
        """
        Post init hook to set the register objects for the class if none where provided by the user!
        """
        self._collections = self._collections or CollectionRegister(self.settings)
        self._jobs = self._jobs or JobsRegister(self.settings, self.links)
        self._processes = self._processes or ProcessRegister(self.links)

    def _combine_endpoints(self):
        """For the various registers that hold endpoint functions, concat those endpoints to register in get_capabilities."""
        registers = [self._collections, self._processes, self._jobs]

        endpoints = []
        for register in registers:
            if register:
                endpoints.extend(register.endpoints)
        return endpoints

    def get_well_known(self) -> models.WellKnownOpeneoGetResponse:
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

        return models.WellKnownOpeneoGetResponse(
            versions=[
                models.Version(
                    url=url, production=False, api_version=self.settings.OPENEO_VERSION
                )
            ]
        )

    def get_capabilities(self) -> models.Capabilities:
        """ """
        return models.Capabilities(
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

    def get_conformance(self) -> models.ConformanceGetResponse:
        """ """
        return models.ConformanceGetResponse(
            conformsTo=conformance.BASIC_CONFORMANCE_CLASSES
        )
