import click
import fsspec

from alembic import command
from alembic.config import Config
from pathlib import Path

def get_app_template():
    """
        Generate the default app file for an openeo api app.
    """
    # You can load the template content from a file or define it inline here
    # For simplicity, let's define inline templates
    return """# Your main Python code goes here
from fastapi import FastAPI

from openeo_fastapi.api.app import OpenEOApi
from openeo_fastapi.api.types import Billing, FileFormat, GisDataType, Link, Plan
from openeo_fastapi.client.core import OpenEOCore

formats = [
    FileFormat(
        title="json",
        gis_data_types=[GisDataType("vector")],
        parameters={}
    )
]

links = [
    Link(
        href="https://eodc.eu/",
        rel="about",
        type="text/html",
        title="Homepage of the service provider",
    )
]

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
    pass

@click.group()
def cli():
    """Defining group for executor CLI."""
    pass

@click.command()
@click.option('--path', default=None, type=str)
def new(path):
    """Initialize a new openeo_fastapi api project at the specified directory."""
    fs = fsspec.filesystem(protocol="file")
        
    if path:
        path = Path(path)
        if not path.exists():
            raise ValueError("Provided path does not exist.")
    else:
        path = Path(fs.get_mapper("").root)
    
    
    openeo_dir = path / "openeo_api"
    db_dir = openeo_dir / "psql"
    init_file = openeo_dir / "__init__.py"
    app_file = openeo_dir / "app.py"
    revise_file = openeo_dir / "revise.py"


    alembic_dir = db_dir / "alembic"
    alembic_models = db_dir / "models.py"
    alembic_ini = db_dir / "alembic.ini"

    fs.mkdir(openeo_dir)

    fs.mkdir(db_dir)
    
    fs.mkdir(alembic_dir)

    fs.touch(alembic_models)
    with fs.open(alembic_models, 'w') as f:
        f.write(get_models_template())
    
    alembic_cfg = Config(alembic_ini)
    
    command.init(
        alembic_cfg,
        directory=alembic_dir
    )
    
    fs.touch(init_file)
    
    fs.touch(app_file)
    with fs.open(app_file, 'w') as f:
        f.write(get_app_template())

    revise_file = openeo_dir / "revise.py"
    fs.touch(revise_file)

    pass

cli.add_command(new)

if __name__ == '__main__':
    cli()
