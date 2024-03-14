import abc

from openeo_fastapi.client.models import Endpoint


class EndpointRegister(abc.ABC):
    def __init__(self):
        self.endpoints = self._initialize_endpoints()

    @abc.abstractmethod
    def _initialize_endpoints(self) -> list[Endpoint]:
        pass
