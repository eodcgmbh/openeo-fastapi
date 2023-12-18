from typing import Type

import attr
from attrs import Factory, define, field
from fastapi import APIRouter, FastAPI, Response
from starlette.responses import JSONResponse

from openeo_fastapi.client import models


@define
class OpenEOApi:
    """Factory for creating FastApi applications conformant to the OpenEO Api specification."""

    client: field()
    app: field(default=Factory(lambda self: FastAPI))
    router: APIRouter = attr.ib(default=attr.Factory(APIRouter))
    response_class: type[Response] = attr.ib(default=JSONResponse)

    def _route_filter(self):
        """ """
        pass

    def register_get_capabilities(self):
        """Register landing page (GET /).

        Returns:
            None
        """
        self.router.add_api_route(
            name="capabilities",
            path="/",
            response_model=models.Capabilities,
            response_model_exclude_unset=False,
            response_model_exclude_none=True,
            methods=["GET"],
            endpoint=self.client.get_capabilities,
        )

    def register_get_collections(self):
        """Register collection Endpoint (GET /collections).

        Returns:
            None
        """
        self.router.add_api_route(
            name="collections",
            path="/collections",
            response_model=models.Collections,
            response_model_exclude_unset=False,
            response_model_exclude_none=True,
            methods=["GET"],
            endpoint=self.client.get_collections,
        )

    def register_get_collection(self):
        """Register Endpoint for Individual Collection (GET /collections/{collection_id}).

        Returns:
            None
        """
        self.router.add_api_route(
            name="collection",
            path="/collections/{collection_id}",
            response_model=models.Collection,
            response_model_exclude_unset=False,
            response_model_exclude_none=True,
            methods=["GET"],
            endpoint=self.client.get_collection,
        )

    def register_core(self):
        """Register core OpenEO endpoints.

            GET /
            GET /capabilities
            GET /collections
            GET /collections/{collection_id}
            GET /processes


        Injects application logic (OpenEOApi.client) into the API layer.

        Returns:
            None
        """

        self.register_get_capabilities()
        self.register_get_collections()
        self.register_get_collection()

    def __attrs_post_init__(self):
        """Post-init hook.

        Responsible for setting up the application upon instantiation of the class.

        Returns:
            None
        """

        # Register core STAC endpoints
        self.register_core()
        self.app.include_router(router=self.router)
