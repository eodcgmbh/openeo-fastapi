# Table of Contents

* [openeo\_fastapi.cli](#openeo_fastapi.cli)
  * [cli](#openeo_fastapi.cli.cli)
  * [new](#openeo_fastapi.cli.new)

<a id="openeo_fastapi.cli"></a>

# openeo\_fastapi.cli

CLI to support quick initialisation of the project source directory.

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
@click.option("--path", default=None, type=str)
def new(path)
```

Initialize a source directory for an openeo_fastapi api project at the specified location.
