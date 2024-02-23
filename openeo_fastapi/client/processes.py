import functools
from typing import List, Union

import openeo_pg_parser_networkx
import openeo_processes_dask.specs
from openeo_pg_parser_networkx import ProcessRegistry

from openeo_fastapi.client.models import Endpoint, Error, Process, ProcessesGetResponse
from openeo_fastapi.client.register import EndpointRegister


class ProcessRegister(EndpointRegister):
    def __init__(self) -> None:
        super().__init__()
        self.endpoints = self._initialize_endpoints()
        self.process_registry = self._create_process_registry()
        pass

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
            process_registry[
                ("predefined", process_id)
            ] = openeo_pg_parser_networkx.Process(spec)

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
                links=[],
            )
            return resp
        except Exception as e:
            raise Exception(f"Error while getting available Processes: {e}")
