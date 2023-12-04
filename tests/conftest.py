import pytest
from fastapi import FastAPI

from openeo_fastapi.api.app import OpenEOApi
from openeo_fastapi.client.core import OpenEOCore


@pytest.fixture()
def core_api():
    client = OpenEOCore()

    api = OpenEOApi(client=client, app=FastAPI())

    return api
