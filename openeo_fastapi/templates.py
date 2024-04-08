def get_app_template():
    """
        Generate the default app file for an openeo api app.
    """
    return """
from fastapi import FastAPI

from openeo_fastapi.api.app import OpenEOApi
from openeo_fastapi.api.types import Billing, FileFormat, GisDataType, Link, Plan
from openeo_fastapi.client.core import OpenEOCore

formats = []

links = []

client = OpenEOCore(
    input_formats=formats,
    output_formats=formats,
    links=links,
    billing=Billing(
        currency="credits",
        default_plan="a-cloud",
        plans=[Plan(name="user", description="Subscription plan.", paid=True)],
    )
)

api = OpenEOApi(client=client, app=FastAPI())

app = api.app
"""

def get_models_template():
    """
        Generate the default models file for an openeo api app.
    """
    return """from openeo_fastapi.client.psql.settings import BASE
from openeo_fastapi.client.psql.models import *

metadata = BASE.metadata
"""

def get_revision_template():
    """
        Generate the default revision file for the openeo api app.
    """
    return """import os
from alembic import command
from alembic.config import Config
from pathlib import Path

from openeo_fastapi.client.psql.settings import DataBaseSettings

settings=DataBaseSettings()

os.chdir(Path(settings.ALEMBIC_DIR))
alembic_cfg = Config("alembic.ini")

command.revision(alembic_cfg, autogenerate=True)
command.upgrade(alembic_cfg, "head")
"""
            