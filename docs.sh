#!/bin/bash

pydoc-markdown -m openeo_fastapi.cli --render-toc >docs/package/cli.md

pydoc-markdown -m openeo_fastapi.api.app --render-toc >docs/package/api/app.md
pydoc-markdown -m openeo_fastapi.api.models --render-toc >docs/package/api/models.md
pydoc-markdown -m openeo_fastapi.api.types --render-toc >docs/package/api/types.md

pydoc-markdown -m openeo_fastapi.client.auth --render-toc >docs/package/client/auth.md
pydoc-markdown -m openeo_fastapi.client.collections --render-toc >docs/package/client/collections.md
pydoc-markdown -m openeo_fastapi.client.files --render-toc >docs/package/client/files.md
pydoc-markdown -m openeo_fastapi.client.jobs --render-toc >docs/package/client/jobs.md
pydoc-markdown -m openeo_fastapi.client.processes --render-toc >docs/package/client/processes.md
pydoc-markdown -m openeo_fastapi.client.register --render-toc >docs/package/client/register.md
pydoc-markdown -m openeo_fastapi.client.settings --render-toc >docs/package/client/settings.md

pydoc-markdown -m openeo_fastapi.client.psql.engine --render-toc >docs/package/client/psql/engine.md
pydoc-markdown -m openeo_fastapi.client.psql.models --render-toc >docs/package/client/psql/models.md
pydoc-markdown -m openeo_fastapi.client.psql.settings --render-toc >docs/package/client/psql/settings.md
