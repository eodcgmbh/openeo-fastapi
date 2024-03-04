# OpenEO FastAPI
![PyPI - Status](https://img.shields.io/pypi/status/openeo-fastapi)
![PyPI](https://img.shields.io/pypi/v/openeo-fastapi)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/openeo-fastapi)


A FastAPI implementation of the OpenEO Api specification.

## Install

Install using pip
```
pip install openeo-fastapi
```

### Use

The openeo fastapi repo has been set up to work with alembic. When you use this package to to prepare your api, you will need to create an alembic directory. In this directory, you can optionally add a models.py file and extend and of the models from openeo_fastapi.client.models.

The env.py file in the alembic directory, needs to be edited in the following way.
```
from openeo_fastapi.settings import BASE

target_metadata = BASE.metadata
```

You can now create auto revisions for a psql database using the alembic python commands.

```
alembic_cfg = Config("alembic.ini")

command.revision(alembic_cfg, f"openeo-fastapi-{__version__}", autogenerate=True)
command.upgrade(alembic_cfg, "head")

engine = get_engine()
```

Check how it is configured for the tests to see more.

## Contribute

Included is a vscode dev container which is intended to be used as the development environment for this package. A virtual environment needs to be set up inside the dev container, this is managed by poetry.

#### Setup

1. In VSCode `Ctrl + shift + p` and select "Dev Containers: Rebuild Container" to open the development environment for the first time.

2. Once the development environment is ready, run the following commands.
    ```
    # From /openeo-fastapi

    poetry config virtualenvs.path "<I tend to set this to the repo. I.e, ~/openeo-fastapi/.venv>"

    poetry lock

    poetry install --all-extras

    poetry run pre-commit install
    ```

    If you want to add a new dependency. Add it to the pyproject.toml and rerun the two commands again.

    Git is available in the container, so you can commit and push directy to your development branch.

3. You are now ready to write code and run tests!

    Either
    ```
    poetry run python -m pytest
    ```

    Or, run them directly from the testing section of vscode.
