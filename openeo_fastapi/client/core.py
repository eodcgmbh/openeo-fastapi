import abc
from collections import namedtuple
from urllib.parse import urlunparse

from attrs import define, field

from openeo_fastapi.client import conformance, models
from openeo_fastapi.client.collections import CollectionRegister
from openeo_fastapi.client.processes import ProcessRegister
from openeo_fastapi.client.settings import AppSettings


@define
class OpenEOCore:
    """Base client for the OpenEO Api."""

    billing: str = field()
    links: list = field()

    settings = AppSettings()

    _id: str = field(default="OpenEOApi")

    _collections = CollectionRegister(settings)
    _processes = ProcessRegister()

    def _combine_endpoints(self):
        """For the various registers that hold endpoint functions, concat those endpoints to register in get_capabilities."""
        registers = [self._collections, self._processes]

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

    @abc.abstractclassmethod
    async def get_collection(self, collection_id) -> models.Collection:
        collection = await self._collections.get_collection(collection_id)
        return collection

    @abc.abstractclassmethod
    async def get_collections(self) -> models.Collections:
        collections = await self._collections.get_collections()
        return collections

    @abc.abstractclassmethod
    def get_processes(self) -> dict:
        processes = self._processes.list_processes()
        return processes

    @abc.abstractclassmethod
    def get_conformance(self) -> models.ConformanceGetResponse:
        """ """
        return models.ConformanceGetResponse(
            conformsTo=conformance.BASIC_CONFORMANCE_CLASSES
        )
