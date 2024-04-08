"""Defining the settings to be used at the application layer of the API."""
from pathlib import Path
from typing import Any, Optional

from pydantic import BaseSettings, HttpUrl, validator


class AppSettings(BaseSettings):
    """The application settings that need to be defined when the app is initialised. """

    API_DNS: str
    """The domain name hosting the API."""
    API_TLS: bool = True
    """Whether the API http scheme should be http or https."""
    API_TITLE: str
    """The API title to be provided to FastAPI."""
    API_DESCRIPTION: str
    """The API description to be provided to FastAPI."""
    OPENEO_VERSION: str = "1.1.0"
    """The OpenEO Api specification version supported in this deployment of the API."""
    OPENEO_PREFIX = f"/{OPENEO_VERSION}"
    """The OpenEO prefix to be used when creating the endpoint urls."""
    OIDC_URL: HttpUrl
    """The URL of the OIDC provider used to authenticate tokens against."""
    OIDC_ORGANISATION: str
    """The abbreviation of the OIDC provider's organisation name, e.g. egi."""
    OIDC_ROLES: list[str]
    """The OIDC roles to check against when authenticating a user."""
    STAC_VERSION: str = "1.0.0"
    """The STAC Version that is being supported by this deployments data discovery endpoints."""
    STAC_API_URL: HttpUrl
    """The STAC URL of the catalogue that the application deployment will proxy to."""
    STAC_COLLECTIONS_WHITELIST: Optional[list[str]]
    """The collection ids to filter by when proxying to the Stac catalogue."""

    @validator("STAC_API_URL")
    def ensure_endswith_slash(cls, v: str) -> str:
        """Ensure the STAC_API_URL ends with a trailing slash."""
        if v.endswith("/"):
            return v
        return v.__add__("/")

    class Config:
        """Pydantic model class config."""

        @classmethod
        def parse_env_var(cls, field_name: str, raw_val: str) -> Any:
            """Parse any variables and handle and csv lists into python list type."""
            if field_name == "STAC_COLLECTIONS_WHITELIST":
                return [str(x) for x in raw_val.split(",")]
            elif field_name == "OIDC_ROLES":
                return [str(x) for x in raw_val.split(",")]
            return cls.json_loads(raw_val)
