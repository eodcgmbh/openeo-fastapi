from typing import Any, Optional

from pydantic import BaseSettings, HttpUrl


class AppSettings(BaseSettings):
    """Place to store application settings."""

    API_DNS = HttpUrl
    API_TLS: str = "True"

    API_TITLE: str
    API_DESCRIPTION: str

    OPENEO_VERSION: str = "1.1.0"
    OPENEO_PREFIX = f"/{OPENEO_VERSION}"

    # External APIs
    STAC_VERSION: str = "1.0.0"
    STAC_API_URL: Optional[HttpUrl]
    STAC_COLLECTIONS_WHITELIST: Optional[list[str]] = []

    class Config:
        @classmethod
        def parse_env_var(cls, field_name: str, raw_val: str) -> Any:
            if field_name == "STAC_COLLECTIONS_WHITELIST":
                return [x for x in raw_val.split(",")]
            return cls.json_loads(raw_val)
