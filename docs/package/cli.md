# Table of Contents

* [openeo\_fastapi.cli](#openeo_fastapi.cli)
  * [get\_app\_template](#openeo_fastapi.cli.get_app_template)
  * [get\_models\_template](#openeo_fastapi.cli.get_models_template)
  * [get\_revision\_template](#openeo_fastapi.cli.get_revision_template)
  * [cli](#openeo_fastapi.cli.cli)
  * [new](#openeo_fastapi.cli.new)

<a id="openeo_fastapi.cli"></a>

# openeo\_fastapi.cli

CLI to support quick initialisation of the project source directory.

<a id="openeo_fastapi.cli.get_app_template"></a>

#### get\_app\_template

```python
def get_app_template()
```

Generate the default app file for an openeo api app.

<a id="openeo_fastapi.cli.get_models_template"></a>

#### get\_models\_template

```python
def get_models_template()
```

Generate the default models file for an openeo api app.

<a id="openeo_fastapi.cli.get_revision_template"></a>

#### get\_revision\_template

```python
def get_revision_template()
```

Generate the default revision file for the openeo api app.

<a id="openeo_fastapi.cli.cli"></a>

#### cli

```python
@click.group()
def cli()
```

Defining group for executor CLI.

<a id="openeo_fastapi.cli.new"></a>

#### new

```python
@click.command()
@click.option('--path', default=None, type=str)
def new(path)
```

Initialize a source directory for an openeo_fastapi api project at the specified location.

