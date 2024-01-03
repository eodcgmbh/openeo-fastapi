from enum import Enum
from pathlib import Path

import requests
from pydantic import BaseModel

# TODO Basic classes for handling OIDC token validation. Need to test this on keycloak.


class AuthMethod(Enum):
    """Enum defining known auth methods."""

    BASIC = "basic"
    OIDC = "oidc"


class AuthProvider(Enum):
    """Enum defining known oidc providers."""

    EGI = "egi"
    NONE = ""


class AuthToken(BaseModel):
    """ """

    provider: AuthProvider
    token: str

    def validate_token(self, oidc_url) -> bool:
        """Try to validate the token against the give OIDC provider."""
        egi_config = requests.get(oidc_url + "/.well-known/openid-configuration")
        userinfo_url = egi_config.json()["userinfo_endpoint"]
        resp = requests.get(
            userinfo_url,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.token}",
            },
        )
        return resp
