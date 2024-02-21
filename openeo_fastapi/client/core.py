import abc
from collections import namedtuple
from urllib.parse import urlunparse

from attrs import define, field

from openeo_fastapi.client import conformance, models
from openeo_fastapi.client.collections import CollectionCore
from openeo_fastapi.client.processes import ProcessCore
from openeo_fastapi.client.settings import AppSettings


@define
class OpenEOCore:
    """Base client for the OpenEO Api."""

    billing: str = field()
    endpoints: list = field()
    links: list = field()

    settings: AppSettings = field()

    _id: str = field(default="OpenEOApi")

    _collections = CollectionCore(settings)
    _processes = ProcessCore()

    @abc.abstractmethod
    def get_well_know(self) -> models.WellKnownOpeneoGetResponse:
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

    @abc.abstractmethod
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
            endpoints=self.endpoints,
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

    @abc.abstractmethod
    def get_conformance(self) -> models.ConformanceGetResponse:
        """ """
        return models.ConformanceGetResponse(
            conformsTo=conformance.BASIC_CONFORMANCE_CLASSES
        )
