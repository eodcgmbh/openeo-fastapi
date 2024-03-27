import datetime
import functools
import uuid
from typing import Optional, Union

import openeo_processes_dask.specs
from fastapi import Depends, HTTPException, Response
from openeo_pg_parser_networkx import Process as pgProcess
from openeo_pg_parser_networkx import ProcessRegistry
from pydantic import BaseModel, Extra, Field

from openeo_fastapi.api.responses import (
    ProcessesGetResponse,
    ProcessGraphsGetResponse,
    ProcessGraphWithMetadata,
    ValidationPostResponse,
)
from openeo_fastapi.api.types import Endpoint, Error, Process
from openeo_fastapi.client.auth import Authenticator, User
from openeo_fastapi.client.psql.engine import Filter, _list, create, delete, get
from openeo_fastapi.client.psql.models import ProcessGraphORM, UdpORM
from openeo_fastapi.client.register import EndpointRegister

PROCESSES_ENDPOINTS = [
    Endpoint(
        path="/processes",
        methods=["GET"],
    ),
    Endpoint(
        path="/process_graphs",
        methods=["GET"],
    ),
    Endpoint(
        path="/process_graphs/{process_graph_id}",
        methods=["GET"],
    ),
    Endpoint(
        path="/process_graphs/{process_graph_id}",
        methods=["PUT"],
    ),
    Endpoint(
        path="/process_graphs/{process_graph_id}",
        methods=["DELETE"],
    ),
]


class UserDefinedProcessGraph(BaseModel):
    """Model for some incoming requests to the api."""

    id: str
    user_id: uuid.UUID
    process_graph: dict = None
    created: datetime.datetime
    summary: Optional[str] = None
    description: Optional[str] = None
    parameters: Optional[list] = None
    returns: Optional[dict] = None

    @classmethod
    def get_orm(cls):
        return UdpORM

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        extra = "ignore"


class ProcessGraph(BaseModel):
    id: str
    process_graph: dict
    user_id: uuid.UUID
    created: datetime.datetime

    @classmethod
    def get_orm(cls):
        return ProcessGraphORM

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
        extra = Extra.ignore


class ProcessRegister(EndpointRegister):
    def __init__(self, links) -> None:
        super().__init__()
        self.endpoints = self._initialize_endpoints()
        self.process_registry = self._create_process_registry()
        self.links = links

    def _initialize_endpoints(self) -> list[Endpoint]:
        return PROCESSES_ENDPOINTS

    def _create_process_registry(self):
        """
        Returns the process registry based on the predefinied specifications from the openeo_processes_dask module.
        """
        process_registry = ProcessRegistry()

        predefined_processes_specs = {
            process_id: getattr(openeo_processes_dask.specs, process_id)
            for process_id in openeo_processes_dask.specs.__all__
        }

        for process_id, spec in predefined_processes_specs.items():
            process_registry[("predefined", process_id)] = pgProcess(spec)

        return process_registry

    @functools.cache
    def get_available_processes(self):
        return [
            Process.parse_obj(process.spec)
            for process in self.process_registry["predefined", None].values()
        ]

    def list_processes(self) -> Union[ProcessesGetResponse, None]:
        """
        Returns Supported predefined processes defined by openeo-processes-dask
        """
        processes = self.get_available_processes()
        resp = ProcessesGetResponse(
            processes=processes,
            links=self.links,
        )
        return resp

    def list_user_process_graphs(
        self, limit: Optional[int] = 10, user: User = Depends(Authenticator.validate)
    ) -> Union[ProcessGraphsGetResponse, None]:
        """
        Lists all user-defined processes (process graphs) of the authenticated user that are stored at the back-end.
        """
        # Invoke list function from handler
        _filter = Filter(column_name="user_id", value=user.user_id)

        udp_list = _list(list_model=UserDefinedProcessGraph, filter_with=_filter)

        udps = [ProcessGraphWithMetadata(**graph.dict()) for graph in udp_list]

        return ProcessGraphsGetResponse(processes=udps, links=self.links)

    def get_user_process_graph(
        self, process_graph_id: str, user: User = Depends(Authenticator.validate)
    ) -> Union[ProcessGraphWithMetadata, None]:
        """
        Lists all information about a user-defined process, including its process graph.
        """
        graph = get(
            get_model=UserDefinedProcessGraph,
            primary_key=[process_graph_id, user.user_id],
        )

        if not graph:
            raise HTTPException(
                status_code=404,
                detail=f"No user defined process graph found with id: {process_graph_id}",
            )

        return ProcessGraphWithMetadata(**graph.dict())

    def put_user_process_graph(
        self,
        process_graph_id: str,
        body: ProcessGraphWithMetadata,
        user: User = Depends(Authenticator.validate),
    ):
        """
        Stores a provided user-defined process with process graph that can be reused in other processes.
        """
        udp = UserDefinedProcessGraph(
            id=process_graph_id,
            user_id=user.user_id,
            process_graph=body.process_graph,
            created=datetime.datetime.now(),
            description=body.description,
            parameters=body.parameters,
            returns=body.returns,
        )

        create(create_object=udp)

        return Response(
            status_code=201,
            content="The user-defined process has been stored successfully. ",
        )

    def delete_user_process_graph(
        self, process_graph_id: str, user: User = Depends(Authenticator.validate)
    ):
        """
        Deletes the data related to this user-defined process, including its process graph.
        """
        if get(
            get_model=UserDefinedProcessGraph,
            primary_key=[process_graph_id, user.user_id],
        ):
            delete(
                delete_model=UserDefinedProcessGraph,
                primary_key=[process_graph_id, user.user_id],
            )
            return Response(
                status_code=204,
                content="The user-defined process has been successfully deleted.",
            )
        raise HTTPException(
            status_code=404,
            detail=Error(
                code="NotFound",
                message=f"The requested resource {process_graph_id} was not found.",
            ),
        )

    def validate_user_process_graph(
        self,
        body: ProcessGraphWithMetadata,
        user: User = Depends(Authenticator.validate),
    ) -> ValidationPostResponse:
        """ """
        from openeo_pg_parser_networkx.graph import OpenEOProcessGraph
        from openeo_pg_parser_networkx.resolving_utils import resolve_process_graph

        def get_udp_spec(process_id: str, namespace: str):
            """
            Get UDP spec
            """
            if not namespace:
                raise PermissionError("No namespace given for UDP.")

            udp = get(
                get_model=UserDefinedProcessGraph,
                primary_key=[process_id, namespace],
            )
            return udp.dict()

        try:
            OpenEOProcessGraph(pg_data=body.process_graph)
            resolve_process_graph(
                process_graph=body.process_graph,
                process_registry=self.process_registry,
                get_udp_spec=get_udp_spec,
                namespace=user.user_id if user else "user",
            )
        except Exception as e:
            return Response(
                status_code=201,
                content=ValidationPostResponse(
                    errors=[Error(code="Graph validation failed", message=f"{str(e)}")]
                ).json(),
            )
        return ValidationPostResponse(errors=[])
