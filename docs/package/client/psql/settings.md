# Table of Contents

* [openeo\_fastapi.client.psql.settings](#openeo_fastapi.client.psql.settings)
  * [DataBaseSettings](#openeo_fastapi.client.psql.settings.DataBaseSettings)
    * [POSTGRES\_USER](#openeo_fastapi.client.psql.settings.DataBaseSettings.POSTGRES_USER)
    * [POSTGRES\_PASSWORD](#openeo_fastapi.client.psql.settings.DataBaseSettings.POSTGRES_PASSWORD)
    * [POSTGRESQL\_HOST](#openeo_fastapi.client.psql.settings.DataBaseSettings.POSTGRESQL_HOST)
    * [POSTGRESQL\_PORT](#openeo_fastapi.client.psql.settings.DataBaseSettings.POSTGRESQL_PORT)
    * [POSTGRES\_DB](#openeo_fastapi.client.psql.settings.DataBaseSettings.POSTGRES_DB)
    * [ALEMBIC\_DIR](#openeo_fastapi.client.psql.settings.DataBaseSettings.ALEMBIC_DIR)

<a id="openeo_fastapi.client.psql.settings"></a>

# openeo\_fastapi.client.psql.settings

Defining the settings to be used at the application layer of the API for database interaction.

<a id="openeo_fastapi.client.psql.settings.DataBaseSettings"></a>

## DataBaseSettings Objects

```python
class DataBaseSettings(BaseSettings)
```

Appliction DataBase settings to interact with PSQL.

<a id="openeo_fastapi.client.psql.settings.DataBaseSettings.POSTGRES_USER"></a>

#### POSTGRES\_USER

The name of the postgres user.

<a id="openeo_fastapi.client.psql.settings.DataBaseSettings.POSTGRES_PASSWORD"></a>

#### POSTGRES\_PASSWORD

The pasword for the postgres user.

<a id="openeo_fastapi.client.psql.settings.DataBaseSettings.POSTGRESQL_HOST"></a>

#### POSTGRESQL\_HOST

The host the database runs on.

<a id="openeo_fastapi.client.psql.settings.DataBaseSettings.POSTGRESQL_PORT"></a>

#### POSTGRESQL\_PORT

The post on the host the database is available on.

<a id="openeo_fastapi.client.psql.settings.DataBaseSettings.POSTGRES_DB"></a>

#### POSTGRES\_DB

The name of the databse being used on the host.

<a id="openeo_fastapi.client.psql.settings.DataBaseSettings.ALEMBIC_DIR"></a>

#### ALEMBIC\_DIR

The path to the alembic directory for applying revisions.

