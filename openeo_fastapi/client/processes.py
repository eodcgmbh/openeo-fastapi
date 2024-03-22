import datetime
import functools
import uuid
from typing import Union

import openeo_processes_dask.specs
from openeo_pg_parser_networkx import Process as pgProcess
from openeo_pg_parser_networkx import ProcessRegistry
from pydantic import BaseModel, Extra

from openeo_fastapi.api.responses import ProcessesGetResponse
from openeo_fastapi.api.types import Endpoint, Error, Process
from openeo_fastapi.client.psql.models import ProcessGraphORM
from openeo_fastapi.client.register import EndpointRegister


class ProcessGraph(BaseModel):
    process_graph_id: str
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
        return [
            Endpoint(
                path="/processes",
                methods=["GET"],
            )
        ]

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

    def list_processes(self) -> Union[ProcessesGetResponse, Error]:
        """
        Returns Supported predefined processes defined by openeo-processes-dask
        """
        try:
            processes = self.get_available_processes()
            resp = ProcessesGetResponse(
                processes=processes,
                links=self.links,
            )
            return resp
        except Exception as e:
            raise Exception(f"Error while getting available Processes: {e}")
