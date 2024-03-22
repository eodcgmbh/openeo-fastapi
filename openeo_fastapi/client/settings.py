from pathlib import Path
from typing import Any, Optional

from pydantic import BaseSettings, HttpUrl, validator


class AppSettings(BaseSettings):
    """Place to store application settings."""

    API_DNS: HttpUrl
    API_TLS: bool = True

    ALEMBIC_DIR: Path

    API_TITLE: str
    API_DESCRIPTION: str

    OPENEO_VERSION: str = "1.1.0"
    OPENEO_PREFIX = f"/{OPENEO_VERSION}"

    OIDC_URL: HttpUrl
    OIDC_ORGANISATION: str
    OIDC_ROLES: list[str]

    # External APIs
    STAC_VERSION: str = "1.0.0"
    STAC_API_URL: HttpUrl
    STAC_COLLECTIONS_WHITELIST: Optional[list[str]]

    @validator("STAC_API_URL")
    def name_must_contain_space(cls, v: str) -> str:
        if v.endswith("/"):
            return v
        return v.__add__("/")

    class Config:
        @classmethod
        def parse_env_var(cls, field_name: str, raw_val: str) -> Any:
            if field_name == "STAC_COLLECTIONS_WHITELIST":
                return [str(x) for x in raw_val.split(",")]
            elif field_name == "OIDC_ROLES":
                return [str(x) for x in raw_val.split(",")]
            return cls.json_loads(raw_val)
