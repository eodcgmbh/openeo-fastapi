"""Defining the settings to be used at the application layer of the API."""
from typing import Any, Optional

from pydantic import BaseSettings, HttpUrl, validator


class AppSettings(BaseSettings):
    """The application settings that need to be defined when the app is initialised."""

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
    OPENEO_PREFIX = f"/openeo/{OPENEO_VERSION}"
    """The OpenEO prefix to be used when creating the endpoint urls."""
    OIDC_URL: HttpUrl
    """The policies to be used for authenticated users with the backend, if not set, any usser with a valid token from the issuer is accepted."""
    OIDC_ORGANISATION: str
    """The abbreviation of the OIDC provider's organisation name, e.g. egi."""
    OIDC_POLICIES: Optional[list[str]]
    """The OIDC policies to check against when authorizing a user. If not provided, all users with a valid token from the issuer will be admitted.

    "&&" Is used to denote the addition of another policy.
    Policies in the list should be structures as "key, value".
    The key referers to some value that is expected to be found in the OIDC userinfo request.
    The value referes to some value that is then checked for presence in the values found at the key location.

    Example:
    ```
    {
        "email": user@test.org,
        "groups" : [ "/staff" ]
    }

    A valid policy to allow members from the group staff would be, "groups, /staff". This would be the value provided to OIDC_POLICIES.

    If you wanted to include users from another group called "/trial", the updated value to OIDC_POLICIES would be, "groups, /staff && groups, /trial"
    ```
    """
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

    @validator("OIDC_POLICIES", pre=True)
    def split_oidc_policies_str_to_list(cls, v: list) -> str:
        """Ensure the OIDC_POLICIES are split and formatted correctly."""

        if isinstance(v, str):
            # We shouldn't have a string here. But in some cases where the settings where taken from code and not an env variable
            # the config function parse_env_var will not execute. Reclean the value here if that is the case.
            v = [str(x) for x in v.split("&&") if x != ""]

        if not v:
            return v

        cleaned_policies = []
        for policy in v:
            try:
                # TODO Could add a class to handle each oidc policy and return that list instead of just checking value unpacking.
                no_spaces = policy.replace(" ", "")
                key, value = no_spaces.split(",")
            except ValueError:
                raise ValueError(
                    f"Policy '{policy}' contains too many comma seperated values."
                )

            cleaned_policies.append(no_spaces)
        return cleaned_policies

    class Config:
        """Pydantic model class config."""

        @classmethod
        def parse_env_var(cls, field_name: str, raw_val: str) -> Any:
            """Parse any variables and handle and csv lists into python list type."""
            if field_name == "STAC_COLLECTIONS_WHITELIST":
                return [str(x) for x in raw_val.split(",")]
            elif field_name == "OIDC_POLICIES":
                return [str(x) for x in raw_val.split("&&") if x != ""]
            return cls.json_loads(raw_val)
