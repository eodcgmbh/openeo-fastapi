#  Getting Started

Everything on this page is all you need to go from 0 to having your OpenEO Api server running locally. 

## Environment Setup

The openeo-fastapi package comes with a couple of assumptions. The first assumption, is the package is used to build a server side application. The second assumption is that the user is able to provide a connection to a psql database. The final assumption, is the user has provided the set of required environment variables which are needed for the application to run.

The following steps will explain how the user can get the application skeleton to run.

## Installation

Prior to installation, configure and activate a virtual environment for your new project, I can recommend using [poetry](https://python-poetry.org/docs/basic-usage/) for this. Once the environment is activate continue with installing openeo-fastapi.


    pip install openeo-fastapi

## Command line interface

The openeo-fastapi CLI can be used to set up a quick source directory for your deployment.

    openeo_fastapi new /path/to/source/directory

The command line interface will create the following directory tree.

    src/
        __init__.py
        app.py
        revise.py
        /psql
            alembic.ini
            models.py
            alembic/
                env.py
                README
                script.py.mako
                versions/


The **app.py** file defines the minimal code to define the FastApi application to deploy the API.

The **revise.py** file defines steps that can be used to generate and apply
alembic revisions to the database deployment. This file is intended to be used after a new release of your deployment, but before your release has been deployed, i.e. as part of an initialization container. This file is optional and can be deleted if you want to complete these steps in a different way.

The **/psql** directory is used for housing the alembic directory to record the alembic revision history and connectivity to the database. All files ( apart from models.py ) are generated from the alembic init command, so refer to the [alembic docs](https://alembic.sqlalchemy.org/en/latest/) for more information on those files.

The **/psql/models.py** file defines the basis for importing the orm models from the OpenEO FastApi and defining the metadata class that can then be imported and used in the alembic *env.py* file.

The **/psql/alembic/env.py** file needs a couple of edits.

Set the main option for the psql connection.

    config.set_main_option(
        "sqlalchemy.url",
        f"postgresql://{environ.get('POSTGRES_USER')}:{environ.get('POSTGRES_PASSWORD')}"
        f"@{environ.get('POSTGRESQL_HOST')}:{environ.get('POSTGRESQL_PORT')}"
        f"/{environ.get('POSTGRES_DB')}",
    )

Set the target metadata. In this example, I am importing from the **/psql/models.py** file.

    from openeo_api.psql.models import metadata
    target_metadata = metadata


## Set the environment variables

These variables need to be set in the environment of the deployment. Those marked required need to be set, and those set False, have some default value that only needs to be provided 

| Variable    | Description | Required |
| -------- | ------- | ------- |
| API_DNS  | The domain name hosting the API. | True | 
| API_TLS  | Whether the API http scheme should be http or https.  | True |
| API_TITLE  | The API title to be provided to FastAPI. | True | 
| API_DESCRIPTION  | The API description to be provided to FastAPI. | True |
| OPENEO_VERSION  | The OpenEO Api specification version supported in this deployment of the API. Defaults to "1.1.0". | False |
| OPENEO_PREFIX  | The OpenEO prefix to be used when creating the endpoint urls. Defaults to the value of the openeo_version | True |
| OIDC_URL  | The URL of the OIDC provider used to authenticate tokens against. | True |
| OIDC_ORGANISATION  | The abbreviation of the OIDC provider's organisation name. | True |
| OIDC_ROLES  | The OIDC roles to check against when authenticating a user. | False |
| STAC_VERSION  | The STAC Version that is being supported by this deployments data discovery endpoints. Defaults to "1.0.0". | False |
| STAC_API_URL  | The STAC URL of the catalogue that the application deployment will proxy to. | True |
| STAC_COLLECTIONS_WHITELIST  | The collection ids to filter by when proxying to the Stac catalogue. | False |
| POSTGRES_USER  | The name of the postgres user. | True |
| POSTGRES_PASSWORD  | The pasword for the postgres user. | True |
| POSTGRESQL_HOST  | The host the database runs on. | True |
| POSTGRESQL_PORT  | The post on the host the database is available on. | True |
| POSTGRES_DB  | The name of the databse being used on the host. | True |
| ALEMBIC_DIR  | The path to the alembic directory for applying revisions. | True |

## Deploy the application.

1. Revise the database.

        python -m revise.py

2. Deploy the uvicorn server

        uvicorn openeo_app.main:app --reload
