import abc

from attrs import define, field

from openeo_fastapi.client import models


@define
class OpenEOCore:
    """Base client for the OpenEO Api."""

    # TODO. Improve. Not quite sure about setting these here.
    backend_version: str = field()
    billing: str = field()
    endpoints: list = field()
    links: list = field()
    _id: str = field(default="OpenEOApi")
    title: str = field(default="OpenEO FastApi")
    description: str = field(default="Implemented from the OpenEO FastAPi package.")
    stac_version: str = field(default="1.0.0")
    api_version: str = field(default="1.1.0")

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
