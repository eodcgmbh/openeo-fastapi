from openeo_fastapi.api.responses import Endpoint


class EndpointRegister:
    def __init__(self):
        self.endpoints = self._initialize_endpoints()

    def _initialize_endpoints(self) -> list[Endpoint]:
        pass
