"""CLI to support quick initialisation of the project source directory."""
from pathlib import Path

import click
import fsspec
from alembic import command
from alembic.config import Config

from openeo_fastapi.templates import (
    get_app_template,
    get_models_template,
    get_revision_template,
)


@click.group()
def cli():
    """Defining group for executor CLI."""
    pass


@click.command()
@click.option("--path", default=None, type=str)
def new(path):
    """Initialize a source directory for an openeo_fastapi api project at the specified location."""
    fs = fsspec.filesystem(protocol="file")

    if path:
        path = Path(path)
    else:
        path = Path(fs.get_mapper("").root)

    openeo_dir = path
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
    with fs.open(alembic_models, "w") as f:
        f.write(get_models_template())

    alembic_cfg = Config(alembic_ini)

    command.init(alembic_cfg, directory=alembic_dir)

    fs.touch(init_file)

    fs.touch(app_file)
    with fs.open(app_file, "w") as f:
        f.write(get_app_template())

    revise_file = openeo_dir / "revise.py"
    fs.touch(revise_file)
    with fs.open(revise_file, "w") as f:
        f.write(get_revision_template())

    pass


cli.add_command(new)

if __name__ == "__main__":
    cli()
