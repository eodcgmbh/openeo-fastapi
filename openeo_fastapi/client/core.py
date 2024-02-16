import abc

from attrs import define, field

from openeo_fastapi.client import conformance, models
from openeo_fastapi.client.collections import get_collection, get_collections
from openeo_fastapi.client.processes import list_processes

from collections import namedtuple
from urllib.parse import urlunparse






@define
class OpenEOCore:
    """Base client for the OpenEO Api."""

    # TODO. Improve. Not quite sure about setting these here.

    api_dns: str = field()
    backend_version: str = field()
    billing: str = field()
    endpoints: list = field()
    links: list = field()
    api_tls: bool = field(default=True)
    _id: str = field(default="OpenEOApi")
    title: str = field(default="OpenEO FastApi")
    description: str = field(default="Implemented from the OpenEO FastAPi package.")
    stac_version: str = field(default="1.0.0")
    api_version: str = field(default="1.1.0")

    @abc.abstractmethod
    def get_well_know(self) -> models.WellKnownOpeneoGetResponse:
        """ """

        prefix = "https" if self.api_tls else "http"

        Components = namedtuple(
            typename="Components",
            field_names=["scheme", "netloc", "url", "path", "query", "fragment"],
        )

        # TODO Supporting multiple versions should be possible here. But would change how we get the api version.
        url = urlunparse(
            Components(
                scheme=prefix,
                netloc=self.api_dns,
                query=None,
                path="",
                url=f"/openeo/{self.api_version}/",
                fragment=None,
            )
        )

        return models.WellKnownOpeneoGetResponse(
            versions=[
                models.Version(url=url, production=False, api_version=self.api_version)
            ]
        )

    @abc.abstractmethod
    def get_capabilities(self) -> models.Capabilities:
        """ """
        return models.Capabilities(
            id=self._id,
            title=self.title,
            stac_version=self.stac_version,
            api_version=self.api_version,
            description=self.description,
            backend_version=self.backend_version,
            billing=self.billing,
            links=self.links,
            endpoints=self.endpoints,
        )


    @abc.abstractclassmethod
    async def get_collection(self, collection_id) -> models.Collection:
        collection = await get_collection(collection_id)
        return collection

    @abc.abstractclassmethod
    async def get_collections(self) -> models.Collections:
        collections = await get_collections()
        return collections

    @abc.abstractclassmethod
    def get_processes(self) -> dict:
        processes = list_processes()
        return processes

    @abc.abstractmethod
    def get_conformance(self) -> models.ConformanceGetResponse:
        """ """
        return models.ConformanceGetResponse(
            conformsTo=conformance.BASIC_CONFORMANCE_CLASSES
        )

