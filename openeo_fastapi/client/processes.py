import functools
from typing import Optional, Union

import openeo_pg_parser_networkx
import openeo_processes_dask
import openeo_processes_dask.specs
from fastapi import APIRouter
from openeo_pg_parser_networkx import ProcessRegistry
from pydantic import conint

import openeo_fastapi
from openeo_fastapi.client.models import Error, Link, ProcessesGetResponse

router_processes = APIRouter()
process_registry = ProcessRegistry()

predefined_processes_specs = {
    process_id: getattr(openeo_processes_dask.specs, process_id)
    for process_id in openeo_processes_dask.specs.__all__
}

for process_id, spec in predefined_processes_specs.items():
    process_registry[("predefined", process_id)] = openeo_pg_parser_networkx.Process(
        spec
    )


@functools.cache
def get_available_processes():
    return [
        openeo_fastapi.client.models.Process.parse_obj(process.spec)
        for process in process_registry["predefined", None].values()
    ]


def list_processes() -> Union[ProcessesGetResponse, Error]:
    """
    Supported predefined processes
    """
    try:
        processes = get_available_processes()
        resp = ProcessesGetResponse(
            processes=processes,
            links=[
                Link(
                    href="https://eodc.eu/",
                    rel="about",
                    type="text/html",
                    title="Homepage of the service provider",
                )
            ],
        )
        return resp
    except Exception as e:
        raise Exception(f"Error while getting available Processes: {e}")
