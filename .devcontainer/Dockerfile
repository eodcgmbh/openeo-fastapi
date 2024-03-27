ARG VARIANT="3.10-bullseye"
FROM mcr.microsoft.com/vscode/devcontainers/python:0-${VARIANT} as devcontainer

ENV POETRY_VIRTUALENVS_IN_PROJECT 1

# Poetry
ARG POETRY_VERSION="1.7.1"
RUN if [ "${POETRY_VERSION}" != "none" ]; then su vscode -c "umask 0002 && pip3 install poetry==${POETRY_VERSION}"; fi

RUN apt update -qy && \
    apt install -qy --no-install-recommends \
        postgresql-13 \
        git

WORKDIR /openeo-fastapi
