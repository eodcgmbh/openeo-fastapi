"""Class define the basic framework for an EndpointRegister.

Classes:
    - EndpointRegister: Framework for defining and extending the logic for working with an EndpointRegister.
"""
from openeo_fastapi.api.types import Endpoint

class EndpointRegister:
    """The ProcessRegister to regulate the application logic for the API behaviour.
    """
    
    def __init__(self):
        """Initialize the EndpointRegister.
        """
        self.endpoints = self._initialize_endpoints()

    def _initialize_endpoints(self) -> list[Endpoint]:
        """Initialize the endpoints for the register.

        Returns:
            list[Endpoint]: The default list of job endpoints which are packaged with the module.
        """
        pass
