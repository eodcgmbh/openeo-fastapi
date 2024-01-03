import functools
import importlib
import inspect
import os

from fastapi import APIRouter
from odc.stac import stac_load
from openeo_pg_parser_networkx import ProcessRegistry
from openeo_pg_parser_networkx.process_registry import Process
from openeo_processes_dask.process_implementations.core import process
from openeo_processes_dask.specs import load_collection as load_collection_spec
from openeo_processes_dask.specs import save_result as save_result_spec
from pystac_client import Client
from starlette.responses import FileResponse

router_processes = APIRouter()


def load_collection(
    max_items=None,
    limit=None,
    ids=None,
    collections=None,
    bbox=None,
    intersects=None,
    datetime=None,
    query=None,
    filter=None,
    filter_lang=None,
    sortby=None,
    fields=None,
    bands=None,
    crs=None,
    resolution=None,
):
    catalog = Client.open(os.getenv("STAC_API_URL"))
    query = catalog.search(
        max_items=max_items,
        limit=limit,
        ids=ids,
        collections=collections,
        bbox=bbox,
        intersects=intersects,
        datetime=datetime,
        query=query,
        filter=filter,
        filter_lang=filter_lang,
        sortby=sortby,
        fields=fields,
    )
    items = list(query.get_items())
    ods = stac_load(items, bands=bands, crs=crs, resolution=resolution)
    od = ods.to_array()
    return od


def save_result(data, filename="output.nc"):
    data.to_netcdf(filename)
    return FileResponse(
        filename, media_type="application/octet-stream", filename=filename
    )


@functools.cache
async def get_processes():
    """
    Basic metadata for all datasets
    """

    process_registry = ProcessRegistry(wrap_funcs=[process])

    processes_from_module = [
        func
        for _, func in inspect.getmembers(
            importlib.import_module("openeo_processes_dask.process_implementations"),
            inspect.isfunction,
        )
    ]

    specs_module = importlib.import_module("openeo_processes_dask.specs")
    specs = {
        func.__name__: getattr(specs_module, func.__name__)
        for func in processes_from_module
    }

    for func in processes_from_module:
        process_registry[func.__name__] = Process(
            spec=specs[func.__name__], implementation=func
        )

    process_registry["load_collection"] = Process(
        spec=load_collection_spec, implementation=load_collection
    )
    process_registry["save_result"] = Process(
        spec=save_result_spec, implementation=save_result
    )

    return process_registry["predefined", None]
